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

建议：**私有 GitHub 仓库存档 + 有身份验证的网页预览**。

- 团队已有内网 / VPN 服务器：将 `dist/` 交给管理员，通过团队现有访问权限提供网页。
- 没有内部服务器：可配置 Cloudflare Access 的指定邮箱登录，部署方式和域名另行确定。
  若通过本机 Tunnel 提供网页，本机及预览服务必须一直在线；长期交接应使用持续运行的服务器。
- 如果组织已有 GitHub Enterprise Cloud：可以评估组织私有仓库的私有 GitHub Pages。

普通 GitHub Pages 即使源仓库私有，网页也通常对互联网公开。请不要为内部预览直接开启普通 Pages。
`noindex`、不告诉别人链接、网页 JavaScript 密码都不能代替服务端访问控制。
需要验证 HTML、PDF、视频及其他资源的直接地址均受保护。

当前咖啡 MP4 约61MiB，抽屉 MP4 约31MiB；均低于 Git 常规文件100MiB上限，
但超过 Cloudflare Pages 的单文件25MiB上限。因此不能原样拖入 Cloudflare Pages；
应使用受保护的服务器 / Tunnel，或在选定托管方案后另行处理媒体。

现在另有 Cloudflare 专用打包脚本 `scripts/prepare_cloudflare.py`：只为上述两条视频
生成约20MiB的托管副本，输出到 `output/cloudflare-private/site/`，主网站文件与视频原件不变。
`dist/` 仍保留适合以后 GitHub Pages 使用的原网页视频。

源码已备份至私有仓库 `https://github.com/laihh88/a2meas-homepage`。
Cloudflare 空项目名为 `a2meas-preview-laihh88`；只有完成 Access 的正式域名及预览域名保护
并检查 PDF/视频直接地址后，才能上传论文内容。登录授权不等同于访问保护已配置完成。

参考：[GitHub Pages 私密访问](https://docs.github.com/en/enterprise-cloud%40latest/pages/getting-started-with-github-pages/changing-the-visibility-of-your-github-pages-site)、
[Cloudflare 邮箱验证](https://developers.cloudflare.com/cloudflare-one/integrations/identity-providers/one-time-pin/)、
[Cloudflare Pages 文件限制](https://developers.cloudflare.com/pages/platform/limits/)。

## 上传到 GitHub

目标仓库必须先确定为 Private。当前文件夹还没有初始化 Git；不要将5.5GB原始 `demo/`
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

已有13条视频用于页面：10条短任务、2条纠错、1条咖啡全流程。
短任务列表共12项，其中2条包裹操作仍未提供；花絮也待补。
Framework 与 Method 每步1.5秒；Method 走完后全部高亮10秒；悬停进入手动模式。
新增视频后重新打包，运行文件的 SHA-256 清单见 `package-manifest.json`。
