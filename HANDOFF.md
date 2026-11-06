# A²-MEAS 网站交接

## 最新前端同步至GitHub的提交内容（2026-11-05）

用户在字体稳定后明确恢复并授权将已确认前端更新提交、推送至a2-meas/a2-meas.github.io的main。此前“同步暂停”已解除。本次版本包含v6完整封面、原生循环、整画面首尾0.6s纯黑淡出/淡入、2px虚化、标题/机构/按钮开场即显示、Google Sans 700内嵌子集防止字体切换、五张方法图矢量连接层、Household Tasks更名及两组论文说明。原始renew.pdf、未使用JPEG、demo/和本地output/不纳入；字体许可证与复现脚本纳入。

同步采用普通新增提交，不重写历史、不force push；仓库保持Private、Pages关闭，Cloudflare Access及邮箱权限不改。本轮不重新部署Cloudflare，因此其私密预览仍为3f3f450b且尚无最后的字体内嵌修复。公开和启用Pages由用户后续执行，不因本次git push自动启用。

公开前检查：现有10个可达提交、393个可达blob版本，以及当前候选文本未匹配常见私钥、GitHub/API令牌、AWS访问键和密码字面量；142项静态运行资产均已纳入Git候选，HTML资源、脚本语法和git diff --check通过。检查为模式匹配，不构成全部媒体/PDF内容保证。历史交接文档包含私密预览个人邮箱/白名单记录，公开仓库会同时公开这些历史；如果不希望披露，应在改Public前另行处理。本轮保留历史，不擅自删除或重写。完整本地审计及同步结果/提交SHA记录在output/github-sync-20261105/，同步后应以远程main与result.json核验为准。

## 封面开场字体切换修复（2026-11-05，仅本地；GitHub同步已按用户要求暂停）

用户在GitHub同步检查期间要求“停一下”，先修复淡入淡出开场标题从替代字体切换的问题。当前未执行git add/commit/push，远程仍76fbb0c，仓库Private、Pages关闭。只读核验曾发现交接文档含私密预览邮箱白名单；完整历史公开前检查尚未完成，不能声称仓库已可安全公开。未经用户恢复指令，不继续GitHub同步。

标题仍为原Google Sans 700；通过scripts/prepare_cover_font.py从现有OFL字体生成15,744字节WOFF2子集（原2,017,168字节），嵌入render-blocking的site.css，font-display:block，消除独立字体下载造成的fallback→Google Sans切换。保留原TTF和OFL许可证，所有标题字符的glyph轮廓、advance和字重均与原字体一致，重复生成字节稳定。机构/按钮字体和样式未改。生成脚本仅在重建字体时需要fonttools/brotli，已安装至本地output/font-tools；网页运行无需依赖。

浏览器首屏0.22s已确认document.fonts.status=loaded、目标字体check=true、标题opacity1；标题宽953.6875px（1098px视口）。循环视频、整画面0.6s淡入/淡出、2px虚化保持不变，未重新编码视频。核验和截图：output/cover-font-stability-20261105/。本地预览：http://127.0.0.1:4173/?review=stable-cover-font#top 。本轮未部署到Cloudflare、未推送GitHub；线上仍3f3f450b。

## 最新v6封面与循环转场已同步（2026-11-05，覆盖下方仅本地状态）

用户已明确授权本轮私密预览同步。部署为 https://3f3f450b.a2meas-preview-laihh88.pages.dev/ ，正式入口 https://a2meas-preview-laihh88.pages.dev/ 已更新。包含完整16.5s/30fps v6封面、原生循环、首尾各0.6s整画面统一淡入淡出，实际首/末帧逐像素RGB均为0；不分格转场。标题/机构/三个按钮开场即显示，2px虚化，按钮名称/链接和80%尺寸保留。首帧海报为黑场，减少动态/失败回退保留未淡出的源末帧九宫格。

发布包源文件哈希与已核验本地版本一致，仅封面相关资产及HTML/CSS/JS/清单和Worker的封面字节长度变化，其他视频/方法图/报告未变。Wrangler上传8文件、复用134，Worker及_routes.json同步；原始demo/封面-en-v6.mp4和未跟踪renew原PDF均未上传，源视频哈希未变。正式及新部署域名的首页、视频/海报、PDF、CSS/JS、字体、任务列表/预览和连线图等34项匿名GET均302至原aged-night-fb23.cloudflareaccess.com。未读取或修改Access应用、策略、邮箱白名单和登录设置；邮箱访问权限保持不变。GitHub Private/Pages未改，未提交或推送Git。

日志/包哈希/访问核验：output/v6-fade-preview-deploy-20261105/。本地浏览器已验证循环跨接点、标题常显、2px虚化；像素核验在output/cover-loop-fade-20261105/。本轮未进行登录后线上视觉复核，上传包与已验证资产一致。下方“仅本地/未上传”及旧封面播放设置均为历史记录；此次授权仅对应本轮同步，后续更改仍按用户要求处理。

## 封面循环首尾整画面淡入淡出（2026-11-05，仅本地，未上传）

用户要求循环接点平滑，所有像素同时变暗/变亮，不能按格子或区域分开处理。prepare_cover_media.py现在对完整1280×720画面应用统一FFmpeg fade：前0.6s从黑渐亮，最后0.6s渐暗到黑；按解码495帧/30fps计算，淡入n18，淡出start_frame476/n18，使实际第494帧达到纯黑。没有裁格、遮罩、分区、交错或扫描转场，原始v6文件哈希未变，时长仍16.5s，原生loop保持开启。背景遮罩改为中性rgba(0,0,0,.38)，确保黑帧不会被染成绿色；标题/机构/三个按钮始终显示，2px虚化保留。

首帧poster与视频黑场一致；减少动态效果/自动播放失败使用的cover-mosaic.jpg仍取未淡出的源末帧，保留有内容的静态九宫格。逐像素检查首/末帧RGB最大值均为0；前后半程过渡对9个区域测得亮度比约0.48–0.50，确认整画面同步。备份与像素测试在output/cover-loop-fade-20261105/；原视频未更改。网页本地预览：http://127.0.0.1:4173/?review=v6-uniform-fade#top 。本轮不部署、不推送、不修改邮箱权限；线上仍7edfb560。

## 封面v6循环播放（2026-11-05，仅本地，未上传）

用户最新要求封面循环播放，覆盖下方“播放一次停末帧”的历史设置。#cover-video已开启原生loop，site.js移除coverVideo.ended停止守卫，data/videos.json与prepare_cover_media.py同步loop=true。继续使用完整16.5s v6视频，无重新裁切或转码；2px虚化、标题/机构/三个按钮开场即显示均保留。离开封面或切入后台时仍暂停，返回继续播放；减少动态效果偏好仍使用静态海报。未部署/推送/提交，线上仍7edfb560；邮箱访问权限未修改。

本地预览：http://127.0.0.1:4173/?review=v6-cover-loop#top 。浏览器核验及截图见output/cover-v6-local-20261105/loop-verification.json和cover-loop.jpg。

## 最新封面v6（2026-11-05，仅本地，用户明确先不上传）

封面来源已换为demo/封面-en-v6.mp4；原文件哈希核验未变。网页派生视频1280×720、保留源30fps和完整16.50s，静音faststart约3MiB。首帧/末帧海报均从新网页视频生成，末帧通过片尾短段reverse取实际最后一帧。标题、机构和既有Tech Report / Code & releases / BibTeX三个按钮从首屏直接显示，CSS默认opacity1/visibility:visible/transition:none；移除8s计时属性、事件和syncCoverTitle。字号/Google Sans字体/80%机构与按钮/链接不变。用户连续调整虚化值，最终明确为2px（覆盖此前6/4/3px）；视频和海报回退共用该值。

播放仍为原生非loop、播放一次停最后一帧；保留coverVideo.ended守卫，避免离开/返回封面自动重播。prepare_cover_media.py更新为新源与配套编码；optimize_playback.py不再处理cover，避免其旧备份把新版视频覆盖。桌面开场0.23s实测文字与按钮已全显示、2px虚化、无渐入；同一16.5s视频播放结束已验证ended=true/paused=true/loop=false。390px手机文字与按钮均在封面内，无页面横向溢出。Python/JS语法、git diff --check通过。

备份、源哈希、截图和实测：output/cover-v6-local-20261105/。本地预览：http://127.0.0.1:4173/?review=v6-cover-local#top ，本地服务已重启（仅127.0.0.1:4173）。当前线上仍为7edfb560，本轮未部署/提交/推送，Access邮箱权限未动，GitHub仍Private且Pages关闭。后续未经用户明确授权不得上传。

## 最新线条与箭头调整已同步（2026-11-05，覆盖下方仅本地状态）

用户明确授权同步本轮连线调整，现已部署 https://7edfb560.a2meas-preview-laihh88.pages.dev/ ，正式私密入口 https://a2meas-preview-laihh88.pages.dev/ 同步更新。五张Framework/Method图使用统一矢量连线层，Framework线身/箭头中心与跨线桥接点已对齐；放大SVG保留连接线。发布包仅图形SVG/WebP、五个新连接层、index.html、site.css和figure-previews清单变动，共46项新/改资产；Wrangler另包含包清单，上传47文件、复用95。发布包源文件哈希核验一致，JS/任务JSON/原PDF/视频/Worker/routes未变。

正式与新部署域名的首页、五个新连接层、放大SVG、PDF、视频、字体、CSS/JS、任务JSON/海报/预览等30项匿名GET均302至原aged-night-fb23.cloudflareaccess.com。未读取或修改Access应用/策略/邮箱白名单/登录方式，邮箱访问权限保持原样。登录后线上视觉本轮未复核，桌面/390px本地画面、阶段切换、横滑、放大已在部署前完成核验。Git未提交/推送，仓库名称不变且保持Private、Pages关闭。日志与核验：output/connector-preview-deploy-20261105/；状态：output/deployment-status.json。下方“仅本地/未上传”描述为历史。

## 最新连线对齐（2026-11-05，仅本地，未上传）

按用户截图对齐Framework跨模块线条，并检查其余方法图。五张图现有独立的小型SVG连接层（总计约8.3KiB），跨模块线身和箭头在同一完整坐标系内绘制，不再切分至不同缩放/虚化裁片。Framework黑色Observation连接线身与箭头统一到源y530.35，恢复指令跨线桥接点和右侧箭头中心同步对齐；其余纠错接口、训练、执行恢复回路及A²-WLA共享连接同样保留矢量。图形含义、模块位置和原始PDF未改。放大SVG保留zoom-connectors组，WebP生成时只移除该组以避免与页面连接层重绘。两张Infra统计图和咖啡纠错图另已检查，无此类裁片接缝，保持原图。

实现入口scripts/align_diagram_connectors.py，已接入Framework/Method裁切与布局脚本；prepare_figure_previews.cjs保留连接层为SVG并生成25个WebP。可直接运行python3 scripts/align_diagram_connectors.py，再按既有命令运行prepare_figure_previews.cjs。桌面及390px手机五张图连接层与画布位置误差0，手机无页面横向溢出，框架横滑/键盘阶段切换和SVG放大验证通过。原始SVG重新生成与重复执行均逐字节稳定，Python/Node语法、HTML资源完整性和git diff --check通过。

本地审阅：http://127.0.0.1:4173/?review=aligned-connectors#framework-flow ；全亮校对页output/connector-review-20261105/review.html；截图与核验在同目录。线上仍为98e79a32，本轮未部署/推送/提交，邮箱权限未动。用户已撤回仓库改名，继续a2-meas/a2-meas.github.io。

## 最新私密预览同步（2026-11-05，覆盖下方仅本地记录）

用户已授权将近期文案改动同步至现有私密预览。部署为 https://98e79a32.a2meas-preview-laihh88.pages.dev/ ，正式入口 https://a2meas-preview-laihh88.pages.dev/ 已同步。包含Household Tasks快捷入口/章节更名、咖啡纠错图下两段说明，以及家庭任务轮播下两句总结。较740ffbd9发布包仅index.html、site.css、data/site-copy-notes.json变化；Wrangler上传4文件/复用133，Worker和_routes.json已同步。正式及新部署域名下首页、报告、封面、CSS、JS、字体、任务JSON、任务预览视频及海报共18项匿名GET均302至原Access登录域名；邮箱白名单及Access配置未修改或重新读取。未提交/推送Git，GitHub保持Private、Pages关闭。已核验本地画面与发布包源文件哈希一致，未进行登录后线上视觉复核。日志和访问记录：output/household-preview-deploy-20261105/。

用户报告本地画廊曾显示加载失败；当前本地已有12项正常初始化，未复现具体异常。用户随后要求先完成同步，未添加重试逻辑，site.js未变。不要声称已修复该偶发错误，后续若重现需获取具体请求或初始化错误。

## 最新还原已部署（2026-11-05，优先于下方历史）

用户要求取消“直接九宫格循环、标题与链接立即显示”的改动。已从修改前备份逐字节恢复完整cover.mp4及海报，并恢复播放一次停末帧、8s统一淡入。保留Google Sans实心标题、80%机构与按钮、6px虚化及Tech Report名称。新私密部署 https://740ffbd9.a2meas-preview-laihh88.pages.dev/，正式入口同步；上传4文件/复用133，Worker已更新完整视频字节长度。12项匿名资源检查均302到Access；未修改Access/白名单、GitHub Private或Pages，未提交/推送Git。本地浏览器已验证开场隐藏、8s后显示、17.166667s结束暂停且loop=false；登录后线上视觉未复核。还原审计与临时旧版备份在output/mosaic-loop-cancel-20261105/，访问记录output/mosaic-cancel-access-after.json。此段覆盖此前e47f8956九宫格循环发布记录。用户后续询问A²-WLA tasks按钮名称，建议Everyday Tasks或Short-Horizon Tasks；尚未授权修改名称，未改。

## 最新私密预览已部署（2026-11-05）

用户要求“帮我推上预览”后，已仅部署output/cloudflare-private/site，版本 https://e47f8956.a2meas-preview-laihh88.pages.dev/，正式入口 https://a2meas-preview-laihh88.pages.dev/ 已同步。新封面从原片约9.1s到末尾、8.083s九宫格循环；标题/机构/图标/按钮直接显示；Google Sans实心白字、80%机构和按钮、6px虚化、Tech Report按钮均已发布。Wrangler上传11个文件、复用126个，Worker和_routes.json同步；发布包HTML/CSS/JS/字体/封面哈希与源文件一致。正式和新部署地址首页/PDF/封面/CSS/JS/字体共12项匿名GET均302至Access；未修改访问策略/白名单或GitHub Private/Pages。登录后线上画面核验未完成：精确绑定预览标签超时；读取当前Chrome窗口状态曾被自动审批拒绝，原因是焦点为无关GitHub页面，未继续读取该页面。部署及匿名保护核验均已完成。Git最新提交仍76fbb0c，本轮前端更改未提交/推送；本次仅授权此次私密预览部署。下方“仅本地/未部署”段落为历史。部署日志output/mosaic-preview-deploy-20261105.log，访问记录output/mosaic-preview-access-after.json，发布状态output/deployment-status.json。

## 九宫格直接循环（2026-11-05，最新本地覆盖，未提交/推送/部署）

取消封面前半段及九宫格切换过程。从原片demo/封面-en.mp4约9.1s（边框已完全落定）截到最后一个视频帧，生成1280×720/24fps约8.083s、1.3MiB的静音循环版cover.mp4。首帧已是完整九宫格，两个海报都取该首帧；原片SHA核验未变，旧运行资产备份于output/cover-before-mosaic-loop-20261105/。HTML使用原生loop，JS移除ended暂停及标题时序；标题/机构/图标/资源链接从首屏直接显示（opacity1、transition0s），不再8秒淡入。保留6px虚化、Google Sans实心标题和80%机构/按钮尺寸。prepare_cover_media.py可复现，optimize_playback.py不再用旧整片备份覆盖新循环。保持Private、Pages关闭、Cloudflare及Access不变。此段覆盖下方“只播放一次/8秒标题淡入”的历史记录。

## 封面信息覆盖层（2026-11-05，仅本地，未提交/推送/部署）

按用户参考图配色，封面视频从首帧到结束全程6px虚化；静态海报/减少动态效果/加载失败回退也使用同样虚化背景。保留原视频文件、播放一次停末帧及8秒标题淡入时机。两行机构和Paper / Code & releases / BibTeX移入同一标题覆盖层，统一淡入；删除视频下方原hero-content及其空白。机构白字，按钮深灰#333333/白字，hover与focus-visible变蓝#287fbd；链接目的地不变。封面外任务演示视频保持清晰。手机封面最小360px，避免标题/机构/按钮拥挤；后续章节与Meet间距不变。当前只供本地预览，GitHub仍Private、Pages关闭，未更新Cloudflare或Access。


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

封面尺寸最新覆盖（2026-11-05，仅本地）：按用户要求，hero-details中的机构文字、按钮、图标及内部间距统一缩放为上一版本的60%（zoom: .6，参与布局以避免保留原占位）。标题大小、封面虚化、淡入时机、按钮配色/链接保持不变。未提交、推送或部署。

封面尺寸与字体最新覆盖（2026-11-05，仅本地）：机构与资源按钮改为最初版80%（hero-details zoom: .8，覆盖60%）。主标题采用参考站Robometer实际声明的Google Sans 700，字体自托管于assets/fonts/google-sans-bold.ttf，附GoogleSans-OFL.txt；纯白实心字，无描边、无文字阴影，保持既有标题字号/两行结构。封面虚化、8秒统一淡入及链接不变；未提交/推送/部署。

最新本地文案（2026-11-05，用户明确先不上传）：Real World快捷入口A²-WLA tasks改为Household Tasks（家庭任务），仍链接#task-demos；下方Short-Horizon Tasks章节标题不变。未部署该文案，线上仍为此前还原版。

最新本地文案补充（2026-11-05，未上传）：用户要求对应章节标题同步；#task-demos-title也改为Household Tasks，快捷入口与章节标题现已一致。锚点和视频不变。

本地新增咖啡纠错图说明（2026-11-05，未上传）：核对新版报告第35页§5.4.2及第36页Figure13，#figure-12下添加两段英文总结：漏抓后开爪调整/重抓/提起；原始起点Step2完成率71→98%、Step7为76→95%；失败回退后history-conditioned Adapter为94%/82%，base-policy retry为14%/8%，每条件每步骤100次。明确为步骤完成率，不是整项咖啡任务成功率；说明随现有放大弹窗同步。Household Tasks本地更名保留；不部署。

Household Tasks视频下方新增两句英文说明（2026-11-05，仅本地未上传）：依据用户指定renew.pdf第32页§5.4.1及第33页Tables9–10、第34页Figure12，概括五类家庭场景的12项桌面任务，考察抓取、放置、动作排序与接触控制；在关闭高层反馈和测试时纠错的条件下，每任务20次评测，完整A²-WLA宏平均整项任务成功率57.92%，π0.5为26.67%。位于轮播控制按钮之后，沿用上方咖啡纠错说明的17px字号/1.75行高/重点加粗。未提交、推送或部署。
