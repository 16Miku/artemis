"""Restricted ADB phone-control MCP server (stdio) for Codex and other MCP hosts.

The server exposes a fixed set of phone primitives. It never accepts arbitrary
shell commands. Read actions (devices, foreground app, screenshot, UI tree) are
always available. Write actions (tap, swipe, text, key, launch) fail closed unless
ADB_PHONE_ALLOWED_PACKAGES lists packages and the foreground app is one of them.

Environment variables:
    ADB_PATH                    optional path to adb (defaults to PATH lookup)
    ADB_PHONE_ALLOWED_PACKAGES  comma-separated Android package names allowed for writes
    ADB_PHONE_TIMEOUT           per-command timeout in seconds (default 30)
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import time
import xml.etree.ElementTree as ET

from mcp.server.fastmcp import FastMCP, Image

mcp = FastMCP(
    "adb-phone",
    instructions=(
        "Controls one Android phone through fixed ADB primitives. Read the screen first "
        "(phone_ui_tree or phone_screenshot), act, then verify. Write actions require "
        "ADB_PHONE_ALLOWED_PACKAGES and refuse when the foreground app is not allowed. "
        "Stop and ask the user before captchas, logins, payments, sending messages, or "
        "any irreversible action."
    ),
)

KEY_CODES = {"back": 4, "home": 3, "enter": 66, "tab": 61}
PACKAGE_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_]*(\.[A-Za-z0-9_]+)+$")
# No quotes, '?', '!', '&', '|', ';', '$' or other shell symbols: the text is passed
# through the device shell by `adb shell input text`.
TEXT_RE = re.compile(r"[A-Za-z0-9 .,_\-@:/]{1,200}")
UI_DUMP_PATH = "/sdcard/adb_phone_ui.xml"


def _timeout() -> float:
    try:
        return max(5.0, float(os.getenv("ADB_PHONE_TIMEOUT", "30")))
    except ValueError:
        return 30.0


def _adb() -> str:
    path = os.getenv("ADB_PATH") or shutil.which("adb")
    if not path:
        raise RuntimeError("adb was not found. Install Android Platform Tools or set ADB_PATH.")
    return path


def _run(args: list[str], *, serial: str | None = None, timeout: float | None = None):
    cmd = [_adb()]
    if serial:
        cmd += ["-s", serial]
    cmd += args
    try:
        proc = subprocess.run(cmd, capture_output=True, timeout=timeout or _timeout(), check=False)
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(f"adb timed out after {exc.timeout:.0f}s running: {args[0]}") from exc
    if proc.returncode != 0:
        detail = (
            proc.stderr.decode(errors="replace").strip()
            or proc.stdout.decode(errors="replace").strip()
        )
        raise RuntimeError(f"adb failed: {detail or 'no output'}")
    return proc


def _connected_devices() -> list[tuple[str, str]]:
    text = _run(["devices"]).stdout.decode(errors="replace")
    devices: list[tuple[str, str]] = []
    for line in text.splitlines():
        parts = line.split()
        if len(parts) < 2 or parts[0].startswith("*") or parts[0] == "List":
            continue
        devices.append((parts[0], parts[1]))
    return devices


def _resolve_serial(device_serial: str | None) -> str:
    ready = [serial for serial, state in _connected_devices() if state == "device"]
    if device_serial:
        if device_serial not in ready:
            raise ValueError("That device is not connected and authorized for USB debugging.")
        return device_serial
    if len(ready) == 1:
        return ready[0]
    if not ready:
        raise ValueError(
            "No authorized Android device is connected. Check USB mode, USB debugging, "
            "and the phone's authorization prompt."
        )
    raise ValueError("More than one device is connected; pass device_serial explicitly.")


def _foreground_package(serial: str) -> str | None:
    """Package of the focused app, or None when it cannot be determined (fails closed)."""
    window = _run(["shell", "dumpsys", "window", "windows"], serial=serial, timeout=20).stdout
    for line in window.decode(errors="replace").splitlines():
        if "mCurrentFocus" in line:
            match = re.search(r"\s([A-Za-z][\w.]*)/", line)
            if match:
                return match.group(1)
    # Some devices omit mCurrentFocus; the resumed activity line still names the package.
    activity = _run(["shell", "dumpsys", "activity", "activities"], serial=serial, timeout=20)
    for line in activity.stdout.decode(errors="replace").splitlines():
        if "topResumedActivity" in line or "mResumedActivity" in line:
            match = re.search(r"\s([A-Za-z][\w.]*)/", line)
            if match:
                return match.group(1)
    return None


def _allowed_packages() -> set[str]:
    raw = os.getenv("ADB_PHONE_ALLOWED_PACKAGES", "")
    return {package.strip() for package in raw.split(",") if package.strip()}


def _require_write_permission(serial: str) -> None:
    allowed = _allowed_packages()
    if not allowed:
        raise PermissionError(
            "Write actions are disabled. Set ADB_PHONE_ALLOWED_PACKAGES in the MCP server env."
        )
    current = _foreground_package(serial)
    if current not in allowed:
        raise PermissionError(
            f"Refusing write action: foreground app '{current or 'unknown'}' is not allowed."
        )


def _screen_size(serial: str) -> tuple[int, int]:
    text = _run(["shell", "wm", "size"], serial=serial).stdout.decode(errors="replace")
    match = re.search(r"Physical size:\s*(\d+)x(\d+)", text) or re.search(r"(\d+)x(\d+)", text)
    if not match:
        raise RuntimeError("Could not read the screen size from the device.")
    return int(match.group(1)), int(match.group(2))


def _check_point(x: int, y: int, width: int, height: int) -> None:
    if not (0 <= x < width and 0 <= y < height):
        raise ValueError(f"Point ({x},{y}) is outside the {width}x{height} screen.")


@mcp.tool()
def adb_list_devices() -> str:
    """List connected Android devices. Serials are masked. Read-only."""
    devices = _connected_devices()
    if not devices:
        return "No devices are listed by adb."
    lines = []
    for serial, state in devices:
        masked = serial if len(serial) <= 8 else f"{serial[:3]}***{serial[-3:]}"
        lines.append(f"{masked}  state={state}")
    return "\n".join(lines)


@mcp.tool()
def phone_current_app(device_serial: str | None = None) -> str:
    """Return the package name of the foreground app. Read-only."""
    serial = _resolve_serial(device_serial)
    return _foreground_package(serial) or "unknown"


@mcp.tool()
def phone_screenshot(device_serial: str | None = None) -> Image:
    """Capture the current screen as PNG. Read-only."""
    serial = _resolve_serial(device_serial)
    data = _run(["exec-out", "screencap", "-p"], serial=serial, timeout=30).stdout
    if not data.startswith(b"\x89PNG"):
        raise RuntimeError("screencap did not return a PNG image.")
    return Image(data=data, format="png")


@mcp.tool()
def phone_ui_tree(device_serial: str | None = None, max_items: int = 150) -> str:
    """List visible labelled or clickable UI elements with their tap centers. Read-only."""
    serial = _resolve_serial(device_serial)
    _run(["shell", "uiautomator", "dump", UI_DUMP_PATH], serial=serial, timeout=30)
    try:
        xml_bytes = _run(["exec-out", "cat", UI_DUMP_PATH], serial=serial).stdout
    finally:
        _run(["shell", "rm", "-f", UI_DUMP_PATH], serial=serial)
    root = ET.fromstring(xml_bytes)
    limit = min(max(1, max_items), 500)
    items: list[str] = []
    for node in root.iter("node"):
        text = (node.get("text") or "").strip()
        desc = (node.get("content-desc") or "").strip()
        clickable = node.get("clickable") == "true"
        if not (text or desc or clickable):
            continue
        match = re.match(r"\[(\d+),(\d+)\]\[(\d+),(\d+)\]", node.get("bounds") or "")
        if not match:
            continue
        left, top, right, bottom = (int(value) for value in match.groups())
        if right <= left or bottom <= top:
            continue
        label = (text or desc)[:80]
        cls = (node.get("class") or "").rsplit(".", 1)[-1]
        resource = (node.get("resource-id") or "").rsplit("/", 1)[-1]
        marker = "clickable " if clickable else ""
        items.append(
            f"[{len(items) + 1}] center=({(left + right) // 2},{(top + bottom) // 2}) "
            f"{marker}{cls} {label!r} {resource}".rstrip()
        )
        if len(items) >= limit:
            break
    return "\n".join(items) or "No labelled or clickable elements were found."


@mcp.tool()
def phone_tap(x: int, y: int, device_serial: str | None = None) -> str:
    """Tap a point in device pixels. Write action: foreground app must be allowed."""
    serial = _resolve_serial(device_serial)
    _require_write_permission(serial)
    width, height = _screen_size(serial)
    _check_point(x, y, width, height)
    _run(["shell", "input", "tap", str(x), str(y)], serial=serial)
    return f"Tapped ({x},{y})."


@mcp.tool()
def phone_swipe(
    x1: int,
    y1: int,
    x2: int,
    y2: int,
    duration_ms: int = 300,
    device_serial: str | None = None,
) -> str:
    """Swipe between two device-pixel points. Write action: foreground app must be allowed."""
    serial = _resolve_serial(device_serial)
    _require_write_permission(serial)
    width, height = _screen_size(serial)
    _check_point(x1, y1, width, height)
    _check_point(x2, y2, width, height)
    duration = min(max(50, duration_ms), 2000)
    _run(
        ["shell", "input", "swipe", str(x1), str(y1), str(x2), str(y2), str(duration)],
        serial=serial,
    )
    return f"Swiped ({x1},{y1}) to ({x2},{y2})."


@mcp.tool()
def phone_type_text(text: str, device_serial: str | None = None) -> str:
    """Type simple ASCII text into the focused field. Write action.

    Allowed characters: letters, digits, spaces and . , _ - @ : /  (max 200).
    Other text, including Chinese, must be entered manually on the phone.
    """
    if not TEXT_RE.fullmatch(text):
        raise ValueError(
            "Only letters, digits, spaces and . , _ - @ : / are allowed (max 200 characters)."
        )
    serial = _resolve_serial(device_serial)
    _require_write_permission(serial)
    _run(["shell", "input", "text", text.replace(" ", "%s")], serial=serial)
    return "Typed text."


@mcp.tool()
def phone_press_key(key: str, device_serial: str | None = None) -> str:
    """Press one of: back, home, enter, tab. Write action."""
    code = KEY_CODES.get(key.lower())
    if code is None:
        raise ValueError("Key must be one of: back, home, enter, tab.")
    serial = _resolve_serial(device_serial)
    _require_write_permission(serial)
    _run(["shell", "input", "keyevent", str(code)], serial=serial)
    return f"Pressed {key.lower()}."


@mcp.tool()
def phone_launch_app(package: str, device_serial: str | None = None) -> str:
    """Launch an app by package name. Only packages in ADB_PHONE_ALLOWED_PACKAGES."""
    if not PACKAGE_RE.fullmatch(package):
        raise ValueError("Package name is not valid.")
    if package not in _allowed_packages():
        raise PermissionError("That package is not listed in ADB_PHONE_ALLOWED_PACKAGES.")
    serial = _resolve_serial(device_serial)
    _run(
        [
            "shell",
            "monkey",
            "-p",
            package,
            "-c",
            "android.intent.category.LAUNCHER",
            "1",
        ],
        serial=serial,
    )
    time.sleep(2)
    return f"Launched {package}. Foreground is now {_foreground_package(serial) or 'unknown'}."


if __name__ == "__main__":
    mcp.run()
