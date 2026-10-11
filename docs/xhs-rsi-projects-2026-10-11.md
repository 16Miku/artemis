# 小红书 RSI 项目帖子调研与互动记录

- **执行日期：** 2026-10-11
- **平台：** 手机端小红书
- **主题：** Recursive Self-Improvement（RSI，递归自我改进）相关项目与开源资源

## 执行摘要

在小红书搜索结果中筛选并阅读了 10 条近期（页面日期约 5 小时至 78 天）明确涉及 RSI 项目、基准或开源资源的帖子。所选帖子页面可见互动量用于判断相对热度，不代表全平台热度排名。10 条均检查并确认点赞/收藏结果；10 条本次均完成点赞，10 条均已收藏（1 条在操作前已收藏）。未评论、关注、转发、发帖或私信。

**说明：** 这里按“小红书帖子”计数，并非 10 个互不相同的项目。OpenRSI 与 Awesome RSI 各有不同作者/内容的帖子；报告保留这些独立帖子，避免把不同的研究视角误称为不同项目。帖子分享链接没有通过分享菜单复制，因此不编造笔记 URL。联系人仅记录帖子明确提供的公开项目入口；没有明确公开渠道时标注“未见”。

## 帖子与核验结果

### 1. NeoHorse-1：将真实使用反馈接入 RSI 飞轮
- **标题 / 作者 / 日期：**「Recursive self-improvement 说来就来了」/ 韩凯V / 09-08
- **可见互动：** 点赞 170 → 171；收藏 173 → 174
- **项目情报：** 帖子介绍 NeoHorse-1，将真实请求、多模型路由与交互轨迹转为后续学习数据，结合能力课程与在线蒸馏形成“评估—选择—更新”循环。帖子报告 NeoHorse-4B 平均分 58.94→64.87、9B 65.60→69.04；这是帖子作者展示的结果，未独立复现实验。
- **公开入口 / 联系：** [GitHub: TokenRhythm/NeoHorse](https://github.com/TokenRhythm/NeoHorse)、[技术报告](https://github.com/TokenRhythm/NeoHorse/blob/main/TechnicalReport_NeoHorse_v1.pdf)、[Hugging Face 项目集合](https://huggingface.co/collections/TokenRhythm/neohorse-1)。未见单独公开邮箱/电话。
- **操作核验：** 操作前两个按钮均未显示已完成；点击后分别显示已点赞 171、已收藏 174。

### 2. OpenRSI：开源研究任务与贡献者招募
- **标题 / 作者 / 日期：**「欢迎一起建设 openRSI！」/ Lalili / 09-30
- **可见互动：** 点赞 136 → 137；收藏操作前已显示“已收藏”（125），未重复点击
- **项目情报：** 帖子称团队将真实开源研究转成 agent 可运行的 autoresearch 任务环境，涵盖预训练、后训练、图像生成、机器人、视觉、检索、推理和系统优化；并邀请贡献 task、算力与领域经验。页面提及 RSI-Anything 与 OpenRSI-Index v0.1。
- **公开入口 / 联系：** 帖子未显示具体仓库 URL、邮箱或电话；公开招募方向为贡献研究任务/算力。未私信作者。
- **操作核验：** 点赞计数增加并显示已点赞 137；收藏在操作前已完成。

### 3. PenguinHarness：可本地部署的自优化 Agent Harness
- **标题 / 作者 / 日期：**「我们把 RSI Agent Harness 完全开源了」/ NYU陈教授｜AI洞见 / 08-03
- **可见互动：** 点赞 331 → 332；收藏 482 → 483
- **项目情报：** 帖子介绍 PenguinHarness，目标是让 Agent 自主构建、评测和优化下一代 Agent；宣称支持 1000+ 模型、本地部署，并强调 Agent Build Agent 与递归自我改进。
- **公开入口 / 联系：** 帖子附有[微信公众号项目介绍文章](https://mp.weixin.qq.com/s/hfSx6mFMHI1D3h4w5UbqHw)，并邀请交流和参与；未见明确 GitHub URL 或公开邮箱/电话。
- **操作核验：** 操作前点赞/收藏均未完成；点击后显示已点赞 332、已收藏 483。

### 4. OpenEvolve：基于进化搜索的代码优化
- **标题 / 作者 / 日期：**「OpenEvolve: 把 LLM 变成自主代码进化引擎」/ 王鹏LLM / 08-13
- **可见互动：** 点赞 47 → 48；收藏 79 → 80
- **项目情报：** 帖子将 OpenEvolve 描述为 AlphaEvolve 的开源实现，以 MAP-Elites、多岛并行进化和 LLM 变异算子，根据报错、性能数据与 Warning 迭代代码；作者称在 Apple Silicon GPU 场景观察到 2–3 倍加速，并提到多模型后端及可复现研究流程。
- **公开入口 / 联系：** [GitHub: algorithmicsuperintelligence/openevolve](https://github.com/algorithmicsuperintelligence/openevolve)。未见单独公开联系方式。
- **操作核验：** 操作前点赞/收藏均未完成；点击后显示已点赞 48、已收藏 80。

### 5. OpenRSI Index：真实模型、机器人和 GPU 上的研究基准
- **标题 / 作者 / 日期：**「OpenRSI！AI开始自己优化AI了？」/ 朱俊帆 / 页面显示“6天前”（约 10-05）
- **可见互动：** 点赞 52 → 53；收藏 62 → 63
- **项目情报：** 帖子介绍 OpenRSI Index Preview v0.1，由 MIT-IBM Watson AI Lab 与 Amazon A-EVO Lab 联合牵头。内容展示预训练 optimizer、文本到图像后训练以及机器人任务等早期结果，并强调微小但可复现、可审计的提升。
- **公开入口 / 联系：** [OpenRSI Index](https://index.openrsi.foundation)、[贡献指南](https://github.com/OpenRSI-Foundation/OpenRSI-Index/blob/main/CONTRIBUTING.md)。这是明确公开的项目参与渠道。
- **操作核验：** 操作前点赞/收藏均未完成；点击后显示已点赞 53、已收藏 63。

### 6. Frontis OpenRSI：从任务执行到轨迹回流训练
- **标题 / 作者 / 日期：**「从0开始学会复现RSI, AI4AI, 自进化全流程」/ RSILab / 08-19
- **可见互动：** 点赞 249 → 250；收藏 355 → 356
- **项目情报：** 帖子拆解 FrontisAI/OpenRSI 研究栈，包括 OpenMLE-Gym、OpenMLE-Evo、OpenMLE-ERL、Frontis-MA1。重点是沙箱执行、自动评测、搜索树/程序数据库记录以及轨迹回流 SFT/RL，形成“执行—反馈—学习—再搜索”闭环。报告中的基准数字为帖子作者所述，未独立复现。
- **公开入口 / 联系：** [GitHub: FrontisAI/OpenRSI](https://github.com/FrontisAI/OpenRSI)。帖子说明仓库含本地 quickstart、任务包和轨迹分析入口；未见单独公开邮箱/电话。
- **操作核验：** 操作前点赞/收藏均未完成；点击后显示已点赞 250、已收藏 356。

### 7. Awesome Self-Improving Agents：自进化 Agent 资源库
- **标题 / 作者 / 日期：**「一周 200stars 啦」/ ray / 07-25
- **可见互动：** 点赞 53 → 54；收藏 62 → 63
- **项目情报：** 帖子介绍一个持续维护的 Self-Improving Agents 开源资源库，收录论文、Benchmark、博客、播客、talk、视频与公开课，并欢迎社区补充。
- **公开入口 / 联系：** 页面给出仓库名称 **Awesome Self-Improving Modern Agentic Systems**，邀请通过 PR、Issue 或留言贡献；帖子没有展示可核对的仓库 URL，因此不推测链接。
- **操作核验：** 操作前点赞/收藏均未完成；点击后显示已点赞 54、已收藏 63。

### 8. Awesome RSI：递归自改进研究地图（近期发布帖）
- **标题 / 作者 / 日期：**「Awesome RSI：开源的递归自改进 AI 资源合集」/ 王鹏LLM / 页面显示“5小时前”（约 10-11）
- **可见互动：** 点赞 20 → 21；收藏 26 → 27
- **项目情报：** 帖子将其定位为 GitHub 研究地图，按模型、Agent 框架、具身系统、自动化 AI 研发、评测基准和安全等分类，另含基础论文、术语区分和评测路径。
- **公开入口 / 联系：** [GitHub: lobehub/awesome-rsi](https://github.com/lobehub/awesome-rsi)。帖子倡导通过开源仓库参与；未见独立联系方式。
- **操作核验：** 操作前点赞/收藏均未完成；点击后显示已点赞 21、已收藏 27。

### 9. Awesome RSI：开源学习地图与 Citation Graph
- **标题 / 作者 / 日期：**「我们做了一张 RSI 开源学习地图」/ Yaowei Zheng / 09-08
- **可见互动：** 点赞 548 → 549；收藏 768 → 769
- **项目情报：** 帖子称团队整理 RSI 论文、Benchmark、Methods & Systems、书籍和课程，并构建 Citation Graph；内容强调 Memory、Skill、Harness 与模型参数更新等不同改进层次。
- **公开入口 / 联系：** 帖子提示在 GitHub 搜索 **Awesome RSI**，并欢迎补论文、提 Issue、贡献；未显示可核对的精确 URL 或私人联系方式。不要仅凭相似名称断定与上一条为同一仓库。
- **操作核验：** 操作前点赞/收藏均未完成；点击后显示已点赞 549、已收藏 769。

### 10. RSIBench：面向 Agent 自我改进的研究基础设施
- **标题 / 作者 / 日期：**「RSI必看Benchmark」/ VibeHooper / 07-29
- **可见互动：** 点赞 216 → 217；收藏 272 → 273
- **项目情报：** 帖子介绍 RSIBench，将训练、评估和服务环境拆分并通过 API 提供给 Agent；当前从 RSIBench-Data 探索合成数据生成、数据优化与 post-training pipeline。帖子报告模型能优化数据流程但尚未稳定超过 base model。
- **公开入口 / 联系：** [论文 arXiv:2607.25886](https://arxiv.org/abs/2607.25886)、[项目网站](http://rsibench.co/)。帖子提及代码名 RSIBench-Data，但未展示可核验的仓库 URL；邀请体验/测试/交流，未见公开邮箱/电话。
- **操作核验：** 操作前点赞/收藏均未完成；点击后显示已点赞 217、已收藏 273。

## 范围与限制

- 检索通过小红书 App 搜索结果及帖子详情页，使用了 RSI、OpenRSI、OpenEvolve、RSI GitHub、RSI benchmark、AI self improving 等关键词。按页面可见日期优先近期内容，并延伸至 90 天内的相关帖子。
- “热度”仅根据每条笔记界面显示的点赞等互动计数判断；不同发布时间的互动数不作严格横向排名，也不代表平台全量排名。
- 项目摘要和链接来自帖子中可见文本；作者/团队宣称的效果未独立复现。没有从公开帖子中看到的私人联系方式均不补猜。
- 未获取小红书分享链接。报告没有包含用户的设备序列号、API 凭据或其他本地私密信息。
- 操作仅限点赞与收藏；发现搜索偶尔出现网络提示后重试成功。没有绕过验证码或访问限制。
