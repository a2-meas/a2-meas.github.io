# A²-MEAS 网站交接

**最新状态（2026-11-04）：主页原生迁移和改名已完成，当前仓库为 `a2-meas/a2-meas.github.io`（ID `1443768725`），origin fetch/push已更新。本轮按用户“帮我更新一下”同步已确认的前端更新，使用普通提交和推送；原始新版报告、未使用JPEG、原始视频与本地备份不上传，两张小型派生裁切PDF和生成脚本纳入。仓库保持Private，GitHub Pages仍关闭，未更新Cloudflare部署，算法仓库及Code入口不变。组织为GitHub Free，不支持Private仓库Pages；升级Team可以保留源码私有但网页公开，组织主页不支持Pages私密访问控制。尚未授权付费升级或网页公开，继续保留现有Cloudflare Access私密预览。下方未提交状态和迁移基线SHA为历史记录，以当前Git/API为准。**

**当前优先任务：迁移和改名已完成，保持Private、Pages关闭，禁止自动部署/公开。** 最新状态见 MIGRATION_HANDOFF.md，详细计划见 MIGRATION_PLAN.md。当前仓库为 `a2-meas/a2-meas.github.io`，origin已更新；算法仓库及Code入口独立保留。下方旧状态与部署记录仅用于追溯。

**最新部署（2026-11-04）：https://5e740d43.a2meas-preview-laihh88.pages.dev/，原私密预览入口同步更新。** Infra两段图注已统筹润色，第二段添加论文正文的427.1对106 demonstration samples/s（π下标0.5参考、4.03×）。用户要求删除比较条件句及single-/eight-GPU独立配置句，已从可见图注删除；原测量条件留在data/site-copy-notes.json供溯源。标题、图形与整体样式保留。桌面/手机及放大图注已检查；线上核验最终文案，正式与部署域名仍受Access保护。截图output/infra-deployed-5e740d43.png；Git仍未提交/推送。

**当前部署（2026-11-04）：https://1575a85d.a2meas-preview-laihh88.pages.dev/，原正式预览入口同步更新。用户已授权上传，此前所有“仅本地、未上传”改动现已发布；下方对应描述为历史。** 已保留Access保护，并核验生产/部署首页、PDF、视频、CSS和图片匿名请求均跳转登录。Git仍未提交/推送。截图output/frontend-deployed-1575a85d.png；发布状态output/deployment-status.json。

最新本地标题维护（未上传）：统一六个章节红大/黑小的字号层级，桌面56/28px，390px手机38/24px，≤380px红色30–34px自适应。Authors红/黑标题使用同一套规则与居中，已移除单独的小字号、大字距覆盖；研究问题、Citation不变，4×绿色强调保留。见site.css的 --section-primary-size / --section-secondary-size。截图 output/heading-hierarchy-system-local.jpg、output/heading-hierarchy-authors-local.jpg。继续不上传。

最新本地维护（2026-11-04，未上传）：A²-WLA 的 Observation history 原图组和绿色底板下移12图坐标单位，拉开与上方青色框的距离；同步调整Qwen3-VL、Current context及Full task instruction入口。收窄绿色和token底板，出箭头从边界外开始，跨模块连线只在共享连接层绘制，编码器/Qwen/token统一水平中心轴。实现见 scripts/action_model_layout.py（由extract_method_modules.py调用）；原报告PDF保留不变。桌面整图及390px手机左右横滑/放大已检查，仍遵守用户先审阅、不上传要求。截图 output/history-row-aligned-local.jpg。

这是可以直接运行的静态网站，不需要 Node、npm、数据库或构建框架。
包含当前网页、原图导出的 SVG、所用视频、封面、论文 PDF 和维护脚本。
打包或下载不会自动开启公开网站。

## 同事本地浏览

1. 解压整个 `a2meas-homepage.zip`，保持文件结构。
2. 电脑需要 Python 3；macOS 双击 `Preview.command`，Windows 双击 `Preview.bat`（使用 Python Launcher）。
3. 浏览器访问 `http://127.0.0.1:4173`。关闭终端或按 Ctrl+C 停止服务。

也可以在项目目录运行：

```sh
python3 scripts/serve.py --port 4173
```

端口已占用时换成 `--port 4175`，访问对应地址。不要双击 `index.html` 作为完整预览：
浏览器通常不允许本地文件读取视频 JSON。备用咖啡入口可以播放，但完整任务列表需要 HTTP 服务。
本地服务只监听本机，适合个人预览，不是给其他人访问的线上服务器。

## 私密在线浏览

网站已部署到 **https://a2meas-preview-laihh88.pages.dev/**，由 Cloudflare 托管，
不依赖制作者的电脑持续开机。源代码另存于 GitHub 私有仓库。

访问者输入白名单邮箱，接收一次性验证码后登录；会话有效期为24小时。
当前白名单包含负责人邮箱、通讯作者邮箱及 lfxxmaster@163.com，同事需要逐个加入白名单，不能直接转发验证码。
无需给予同事 GitHub 写权限，也无需为同事创建 Cloudflare 管理员账号。

在 Cloudflare Zero Trust → Access controls → Policies 中编辑 **Approved project viewers**，
将获准浏览的同事邮箱添加到现有 **Emails** 条件中。不要选择 Everyone 或放开整个 Gmail 域。
对应应用是 **A2-MEAS private preview**，保护范围包含正式域名及 `*.a2meas-preview-laihh88.pages.dev`。
路径留空以保护全部内容，包括 PDF、图片、视频和 JSON 数据。

普通 GitHub Pages 即使源仓库私有，网页也通常对互联网公开。请不要为内部预览直接开启普通 Pages。
`noindex`、不告诉别人链接、网页 JavaScript 密码都不能代替服务端访问控制。
需要验证 HTML、PDF、视频及其他资源的直接地址均受保护。

原网页咖啡 MP4 约61MiB，抽屉 MP4 约31MiB；均低于 Git 常规文件100MiB上限，
但超过 Cloudflare Pages 的单文件25MiB上限。

现在另有 Cloudflare 专用打包脚本 `scripts/prepare_cloudflare.py`：只为上述两条视频
生成约20MiB的托管副本，输出到 `output/cloudflare-private/site/`，主网站文件与视频原件不变。
`dist/` 仍保留适合以后 GitHub Pages 使用的原网页视频。

Cloudflare 专用包还会安装 `cloudflare/video-worker.mjs` 的视频分段读取适配器，
只处理 `/assets/videos/*`，让浏览器原生进度条可以前后拖动。
默认 Pages 静态响应不支持所需的206分段响应；不要从托管包中移除 `_worker.js`
或 `_routes.json`。后续重新编码后须重新运行打包脚本，更新适配器内的视频字节长度。
这两个托管文件不放入普通 `dist/`，本地与以后 GitHub Pages 仍为纯静态网站。
现有 Access 应用继续保护所有视频请求，不增加公开媒体入口。

当前源码私有仓库为 `https://github.com/a2-meas/a2-meas.github.io`；由原 `laihh88/a2meas-homepage` 原生转移并改名，尚未提交的本地更新另有本机快照备份。
Cloudflare 项目名为 `a2meas-preview-laihh88`。已先核验 Access 保护，再上传整站78个文件。
上线后再次核验：正式及部署预览域名、PDF和视频的直接地址，未登录时均跳转验证码登录。
Zero Trust Free 已由账号所有者本人完成开通；管理订阅和账单须由账号所有者自行处理。

更新网站时，先安装 `imageio-ffmpeg` 并运行 `python3 scripts/prepare_cloudflare.py`，
再通过已授权的官方 Wrangler 执行：

```sh
wrangler pages deploy output/cloudflare-private/site --project-name a2meas-preview-laihh88 --branch main
```

保持现有 Access 应用及白名单不变。推送 GitHub 仅备份源码，目前不会自动触发 Cloudflare 部署。
登录凭据不在仓库或 ZIP 内。

参考：[GitHub Pages 私密访问](https://docs.github.com/en/enterprise-cloud%40latest/pages/getting-started-with-github-pages/changing-the-visibility-of-your-github-pages-site)、
[Cloudflare 邮箱验证](https://developers.cloudflare.com/cloudflare-one/integrations/identity-providers/one-time-pin/)、
[Cloudflare Pages 文件限制](https://developers.cloudflare.com/pages/platform/limits/)。

## 上传到 GitHub

当前文件夹已初始化 Git，并连接到上述 Private 仓库；不要将5.5GB原始 `demo/`
或 `Tech Report/` 视频、临时日志、截图、交接 ZIP 加入仓库。
交接 ZIP 内已排除上述内容；原始视频仍保留在制作者电脑。

通过 GitHub 官方登录流程授权即可，无需向他人发送密码、Token 或 SSH 私钥。
仓库中有大于25MiB的媒体，使用 Git 推送，不使用网页逐个上传。
网页只读访问不需要给同事仓库写权限。仓库内的代码备份和网页访问权限分别管理。

## 后续公开到 GitHub Pages

公开需由负责人另行确认。确定可公开后，在完整源码目录执行：

```sh
python3 scripts/package_site.py
```

将生成的 `dist/` **内容**放到选定的 Pages 发布分支根目录，或由 Actions 上传 `dist/`
作为 Pages artifact；不要把整个交接源码目录或原始素材作为发布目录。
发布目录有 `.nojekyll`，路径全部相对化，可用于 `https://OWNER.github.io/REPO/`。
打包命令不会改变仓库可见性，也不会部署或开启 Pages。

## 维护位置

| 内容 | 文件 |
| --- | --- |
| 正文、表格、作者、资源链接 | `index.html` |
| 配色、字号、布局 | `site.css` |
| 交互、弹窗、动画 | `site.js` |
| 视频与封面路径 | `data/videos.json` |
| 文献引用 | `data/citation.bib` 与 HTML 的 BibTeX 块 |
| 原图与裁剪脚本 | `figure/`、`scripts/extract_figures.py`、`scripts/extract_method_modules.py` |
| 重新生成交接包 | `python3 scripts/package_site.py --mode handoff` |

页面使用15条视频：12条已更新的短任务、2条纠错、1条咖啡全流程。
12条任务以当前 demo/ 原片为准，包含拆包与封箱；其余任务不展示。
放大短任务视频后，标题下方显示作者提供的英文 prompt，仍使用原生播放和拖动进度控件。
页面顺序：Question → System → Model → Infra → Simulation → Real World → Authors → Citation。
System 包含四阶段 Framework、纠错接口、纠错训练与执行恢复；Model 单独展示 A²-WLA 动作策略。
所有流程图每步1.5秒，走完后全部高亮10秒；进入对应区域后从头开始，悬停进入手动模式。
Framework 上图与下方四张卡片同步；诊断/纠错按恢复需要触发，正常控制仍直接执行与观察。
新增视频后重新打包，运行文件的 SHA-256 清单见 `package-manifest.json`。

## 封面与原片备份（2026-11-04）

封面原片为 `demo/封面-en.mp4`，网页采用优化后的 `assets/videos/cover.mp4`。
静音自动播放一次，8 秒开始在九宫格转场中淡入半透明白色气泡描边标题（全幅视频透明蒙版），播完停在最后一帧；滚离再返回封面也不会自动重播。
机构与 Paper / Code & releases / BibTeX 在视频下方。字体 Nunito 及开源许可证随包提供。
减少动态效果模式显示九宫格静态封面；浏览器阻止自动播放时可点击 Play film。

9 份重复或旧任务版本已移至本地 `output/demo-duplicates-2026-11-04/`，
其中 `manifest.json` 记录原路径、大小和 SHA-256，需恢复时移回即可。
这份备份和原始 demo 都不上传 GitHub / Cloudflare，也不放进交接压缩包。

## 新版报告与实验结果（2026-11-04）

Paper 入口已替换为作者提供的 renew 版本，保持原 URL。只无损压缩 PDF 内部结构以满足
Cloudflare 单文件上限，50 页文本和原始图像均保留，源 renew.pdf 不改动。
RoboTwin 完整系统的 Clean / Randomized / Average 更新为 95.08 / 95.02 / 95.05。
咖啡纠错图使用新版第 36 页内嵌的原始 1309×1202 PNG，直接提取，未截图。
封面视频静音自动播放一次，结束后保留末帧；首行 A²-MEAS 无冒号且居中。

封面现采用全幅视频蒙版，A²-MEAS 单独居中，完整论文标题在下一行不换行。
蒙版与标题仍从九宫格转场时淡入，视频播完停在末帧，机构和三个入口仍在视频下方。

## 加载与播放优化（2026-11-04）

流程图页面显示由原始 SVG 裁切生成的 WebP 轻量预览，原始 SVG 继续用于放大查看；
必须依次运行矢量裁切/布局脚本，再运行 `scripts/prepare_figure_previews.cjs`。后者需要 sharp，
已生成的预览随包提供，日常预览不需要安装依赖。
视频列表用 `assets/previews/` 内的低码率、完整时长版本，点击后换成 1280×720 全片；
独立播放器打开时暂停其余预览。封面和全片经过流式播放编码，原始文件和旧网页文件备份
均保留在 demo/、Tech Report/ 或 output/，不进入部署包。
Cloudflare 首次播放直接发送视频首段，同时在内部填充分段缓存，仍保留私密登录与拖动功能。

## 前端文案与封面更新（2026-11-04，当前本地）

Meet A²-MEAS 放大到桌面 22px / 手机 20px，与问题标题相距约 40px / 32px。
介绍区先提出 “What embodied systems co-evolve with foundation models?”，下方直接用 A²-MEAS 的控制/恢复能力作答（按用户最新要求删除 Introducing 标题）。System / Model / Infra 的红色标签分别改为：

- Distilling Foundation Model Capabilities into Action Policies
- Simple but Surprisingly Strong World-Language-Action Model
- 4× Training Throughput of Pi05 at a Similar Model Size

保留原有导航名称、锚点、绿黑主标题和图表。此次改动已部署，尚未提交或推送。

介绍区最新排版：问题与回答统一居中；桌面标题分两行，手机自然均衡换行。回答限宽 800px，只保留 A²-MEAS connects… 这一句，只加粗 A²-MEAS 名称。用户最新要求已删除 A compact action policy… 补充说明。

删段后的间距已同步收紧：问题到回答为桌面 20px / 手机 18px；回答到 System 红色标题约 69px / 61px。已在浏览器测量，无横向溢出。最新桌面截图：output/research-question-spacing-desktop.jpg。已部署，尚未提交/推送。

## 最新部署完成（2026-11-04）

部署版本：https://4a4503ad.a2meas-preview-laihh88.pages.dev/
正式入口：https://a2meas-preview-laihh88.pages.dev/ 。本轮全部前端调整已上线；Git 工作区尚未提交或推送。
已登录浏览器核验居中问题、单句回答、20px / 约69px 间距、三处长标题、封面 loop=false 和12条任务。
匿名 GET 核验正式域名、新部署域名、PDF 和封面视频均302跳转 Cloudflare Access 登录；未改访问设置或白名单。
线上截图：output/frontend-deployed-4a4503ad.jpg；访问检查：output/frontend-deploy-access-checks.json。

最新内容修正（2026-11-04）：三个红色标题使用 SYSTEM: / MODEL: / INFRASTRUCTURE: 加完整英文描述。介绍区仅保留居中的研究问题；用户已删除 A²-MEAS connects… 回答，不要恢复。对应空容器和段间距 CSS 已移除，问题与 System 间仍保留紧凑留白。

最新间距覆盖：研究问题至 SYSTEM 红色标题拉大为桌面 120px / 手机 88px；移除仅这两块之间的横向分隔线。三处标题前缀和删除回答的要求继续保留。

当前已上线版本（2026-11-04）：https://57aee81a.a2meas-preview-laihh88.pages.dev/。三处前缀、删除回答、问题至 SYSTEM 桌面120px / 手机88px留白以及去分隔线均已部署并核验。截图：output/frontend-deployed-57aee81a.jpg。

基础设施黑色主标题经用户确认改为 From data loading to distributed optimization；红色 INFRASTRUCTURE: 4×… 标题保留。已检查桌面及 390px 手机，无横向溢出。

## 当前仅本地修改，停止上传（用户明确要求，2026-11-04）

黑色基础设施标题已先部署到 https://bed7a5bc.a2meas-preview-laihh88.pages.dev/ 。随后用户要求 Meet 移至 What 问题下面，又明确要求“改了之后先别上传，我再看看”。
本地已将 Meet A²-MEAS ↓ 从封面移至研究问题下方，改用 .meet-link 并指向 #system；桌面问题到 Meet 24px、Meet 到 SYSTEM 56px，手机20px /52px，无分隔线和横向溢出。
**Meet 位置改动未部署；未经用户后续要求，不再上传。** 本地服务器4173保留用于审阅。预览：http://127.0.0.1:4173/?review=meet-local#research-question ，截图 output/meet-below-question-local.jpg。

最新本地调整（未上传）：封面下方两行机构名称放大到桌面22px / 手机17px。Meet 在 What 下方向 SYSTEM 靠近：桌面问题到Meet48px、Meet到SYSTEM32px；手机40px /32px。保持整体问题到SYSTEM的距离，无分隔线、无横向溢出。截图 output/meet-closer-system-local.jpg 与 output/affiliations-meet-local.jpg。继续遵守用户先审阅、不上传的要求。

最新本地调整（未上传）：INFRASTRUCTURE 标题的 Pi05 改为 π<sub>0.5</sub>；4× 放大到原字号1.55倍（桌面43.4px / 手机37.2px），采用 method 浅绿底板同色系的深鼠尾草绿 #557b49。其余标题维持原橙色。用户已撤回 Throughout 更正，保持 Throughput，不要替换。桌面及390px手机无横向溢出。截图 output/throughput-emphasis-local.jpg。继续不上传。

下标小数点显示修正（仅本地）：π 的 sub 文本仍为标准0.5，点为ASCII句点U+002E；用 Arial 下标数字并将句点轻微下移，避免视觉上像中点。截图 output/decimal-point-local.jpg。未上传。

## 两张新版原图裁切（仅本地，未上传）

已从用户指定 renew.pdf 第4页 Framework 与第16页 A²-WLA 内嵌 Form XObject 直接提取原始矢量图；无截图替代。派生原图为 figure/framework-renew.pdf、figure/action-model-renew.pdf，旧原图及用户报告均保留。
轮廓和位置逐项比对一致，沿用原裁切边界、色板、四阶段轮播、1.5秒阶段/10秒全亮、悬停手动、卡片联动和放大入口。新增任务指令连线及新版标注已进入页面。WebP 从新 SVG 生成。
复现顺序（Python需pypdf、PyMuPDF；Node需sharp）：
1. python3 scripts/extract_renewed_diagrams.py
2. python3 scripts/build_framework_flow.py
3. python3 scripts/extract_method_modules.py --group action-model
4. python3 scripts/build_method_layout.py --group action-model
5. node scripts/prepare_figure_previews.cjs

其他方法图保留原资产。已核验原图几何一致、裁片资产齐全、图/卡片联动、自动阶段切换、SVG放大，以及390px手机局部横滑且页面无横向溢出。脚本语法和git diff --check通过。
本地预览 http://127.0.0.1:4173/?review=renewed-diagrams#framework-flow 。A²-WLA截图 output/renewed-action-model-local.jpg。仍遵守用户“先别上传”的要求。
