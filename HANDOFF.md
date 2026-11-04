# A²-MEAS 网站交接

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
当前白名单包含负责人邮箱及通讯作者邮箱，同事需要逐个加入白名单，不能直接转发验证码。
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

源码已备份至私有仓库 `https://github.com/laihh88/a2meas-homepage`。
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
静音自动循环播放，8 秒开始在九宫格转场中淡入半透明白色气泡描边标题（全幅视频透明蒙版），每轮播完后立即从头循环播放。
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
封面视频原生静音循环，播完立即重播，不再停留；首行 A²-MEAS 无冒号且居中。

封面现采用全幅视频蒙版，A²-MEAS 单独居中，完整论文标题在下一行不换行。
蒙版与标题仍从九宫格转场时淡入，视频立即循环，机构和三个入口仍在视频下方。
