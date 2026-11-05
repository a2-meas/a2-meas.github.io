# A²-MEAS 私密组织迁移：检查结果与待确认计划

**最新状态（2026-11-04）：主页原生迁移和改名已完成，当前仓库为 `a2-meas/a2-meas.github.io`（ID `1443768725`），origin fetch/push已更新。本轮按用户“帮我更新一下”同步已确认的前端更新，使用普通提交和推送；原始新版报告、未使用JPEG、原始视频与本地备份不上传，两张小型派生裁切PDF和生成脚本纳入。仓库保持Private，GitHub Pages仍关闭，未更新Cloudflare部署，算法仓库及Code入口不变。组织为GitHub Free，不支持Private仓库Pages；升级Team可以保留源码私有但网页公开，组织主页不支持Pages私密访问控制。尚未授权付费升级或网页公开，继续保留现有Cloudflare Access私密预览。下方未提交状态和迁移基线SHA为历史记录，以当前Git/API为准。**

检查日期：2026-11-04（America/Los_Angeles）。只读盘点已完成；组织a2-meas随后由用户创建，Free，laihh88为Owner，成员身份未公开，未邀请他人。尚未转移/改名仓库、改变仓库可见性、修改远程地址或启用部署。最新接续步骤见MIGRATION_HANDOFF.md。

后续会话更新（同日）：已复核 main/HEAD、48项未提交或未跟踪改动、主页 Private/Pages关闭、组织 active Owner及空仓库列表。主页本机备份位于 `output/private-migration-backups/20261104-211630-homepage/`，含 Git bundle、184项工作区文件快照与平台元数据，范围和校验记录见该目录。忽略目录原始视频未重复复制，不能视为完整磁盘或异地备份。用户已确认算法入口为 `AutoLab-SAI-SJTU/A2MEAS`，尚未公开且与前端独立；本轮仅迁移前端，算法保持原状。未执行任何转移/改名。此次保护规则API返回403（套餐限制），当前保护规则不能按空列表处理。

## 用户指定目标与阶段边界

- 保留个人账号 `laihh88`，不改名、不转换成组织。
- 首选组织 `a2-meas`；若名称不可用，先询问是否采用 `a2meas`，不得自行替换。
- 主页目标：`a2-meas/a2-meas.github.io`；未来公开地址 `https://a2-meas.github.io/`。
- 算法：`AutoLab-SAI-SJTU/A2MEAS`，用户确认尚未公开、与前端独立。本轮保持原状；此前拟定的 `a2-meas/A2-MEAS` 不执行。
- 第一阶段全程 Private，仅本地预览，不新建或更新线上部署，不启用 GitHub Pages。
- 已有 Cloudflare 私密站点保持原状，是否停用另行确认。
- 创建组织、仓库转移、改名、改变可见性及其他难以撤销的动作，执行前分别确认。
- 只有用户明确说“可以公开”后才启动第二阶段；算法代码是否公开单独确认。
- 不重写历史、不 force push、不在原个人账号重建同名仓库。

## 已核验清单

| 项目 | 结果 |
| --- | --- |
| 本机有效 GitHub CLI 身份 | `laihh88`，来自 macOS Keychain；有仓库管理权限 |
| GitHub 插件身份 | `lai-aii`，无法访问该主页私有仓库；本次改用正确身份的 CLI 只读盘点 |
| 个人账号拥有的仓库 | API 返回仅 `laihh88/a2meas-homepage` |
| 主页仓库 ID / 可见性 | `1443768725` / Private，非 fork，未归档，当前账号有 admin 权限 |
| 技术栈 | 纯 HTML、CSS、原生 JavaScript；Python 仅用于打包/本地服务；没有 Vite/Next.js 配置 |
| 本地与远程默认分支 | 仅 `main`；远程与本地 HEAD 均为 `f744457e5304315177fc78248df34cf3b7cff94a` |
| 已有提交 | 本地可达历史 9 个提交 |
| Git 标签 | 本地与远程均为空 |
| GitHub Pages | `has_pages=false`；Pages API 返回404，未查到已启用站点 |
| GitHub Actions | 没有 workflow；本地没有 `.github/workflows` |
| Actions总开关 / 部署密钥 | Actions enabled=true、allowed_actions=all，但无workflow；deploy keys为0 |
| Actions Secrets / Variables / Environments | 均为0；未读取秘密值 |
| Webhooks | 0 |
| Issues / PR / Releases | API 返回均为空 |
| 本地待处理改动 | 审计开始时46个条目：39个已跟踪文件修改、7个未跟踪文件；不可用 reset/clean/stash 覆盖 |
| 部署方式 | Cloudflare 手动部署 `output/cloudflare-private/site`；Git push 不自动触发当前部署 |
| 当前私密预览 | `https://a2meas-preview-laihh88.pages.dev/`；本次不更新或关闭 |
| 主页源码引用检查 | 检查89项 HTML资源/锚点引用，未发现缺失；CSS本地资源与JS中的视频清单均存在 |
| 根路径适配 | 当前资源引用均为相对路径，已有 `.nojekyll`，可用于 `/`；迁移后仍需浏览器回归 |
| BibTeX | 当前未含 GitHub 仓库URL，不需要为迁移修改作者或论文信息 |
| 页面当前代码链接 | `https://github.com/AutoLab-SAI-SJTU/A2MEAS`，用户已确认是独立算法仓库且尚未公开；当前CLI查询404，不能据此判定不存在 |
| 组织名 | `a2-meas` 已由用户创建；GitHub Free，公开/私有仓库均为0 |
| 当前组织成员关系 | `laihh88` 为active、admin（Owner）；public_members检查404，成员身份未公开 |

本次仅检查秘密/密钥的元数据，未读取或保存任何凭据值。

## 当前需要先确认的事项

1. 算法入口已由用户确认，与前端独立，本轮不迁移或备份算法仓库；Code 链接保持原值。
2. 如代码确实与主页同仓库：先给出拆分方案，解释历史归属与 Issues/PR/Releases 归属，等待用户确认后再操作。一个原仓库的平台元数据不能通过复制代码自然完整复制到两个新仓库；不得为了拆分自行过滤/改写历史。
3. 当前本地前端更新尚未提交到 GitHub。转移仓库本身不会包含这些工作区文件。迁移前先备份、审阅应保留文件，之后通过普通新增提交纳入，不把用户原始PDF等未跟踪素材自动全部提交。

前端来源与算法独立性已澄清；主页备份已完成。下一步只请求主页原生转移确认，未获确认不执行；改名另行确认。

## 第一阶段拟执行顺序

1. **确认源仓库（已完成）**：前端源为 `laihh88/a2meas-homepage`；算法 `AutoLab-SAI-SJTU/A2MEAS` 与此前端独立，保留原状。
2. **迁移前备份**：为每个已确认源仓库保存 refs/提交SHA及平台元数据基线；创建 Git bundle 和本地工作区快照。Git bundle不替代Issues/PR/Releases的核验。保留当前工作区和用户素材。
3. **指导创建全新组织**：用户在 `laihh88` 下进入头像 → Settings → Organizations → New organization，选 GitHub Free，名称填 `a2-meas`，填写联系邮箱并完成GitHub验证。不要选择转换个人账号的入口。创建涉及条款或验证码时由用户完成最终提交。名称不可用时先询问用户，不切换备选名称。
4. **核验目标组织**：确认 `laihh88` 为Owner、目标为Free组织、成员默认仓库权限尽量为No permission，并检查目标不存在同名仓库。任何权限设置修改另行说明确认；不额外邀请成员或赋予应用新权限。
5. **转移主页前单独确认**：列出源 `laihh88/a2meas-homepage` → 目标 `a2-meas/a2meas-homepage`，明确保持Private；得到确认后使用GitHub原生Transfer ownership，不复制新建代替转移。
6. **转移后核验、再改名确认**：检查仓库ID、Private、refs与元数据；再请求将组织内仓库改名为 `a2-meas.github.io` 的确认。可合并在同一次转移表单操作中，但必须提前明确两个动作并取得确认。
7. **算法仓库保持原状**：本轮不转移、不改名、不公开、不建立替代仓库。
8. **更新本地远程**：主页执行 `git remote set-url origin https://github.com/a2-meas/a2-meas.github.io.git`；算法仓库远程地址不变。核验fetch/push均指向正确位置，不force push。
9. **更新前端和文档链接**：更新README、HANDOFF及当前状态文档中的活动仓库地址；Code & releases链接保留 `https://github.com/AutoLab-SAI-SJTU/A2MEAS`。历史部署记录保留真实历史。检查工作流中的owner/repo、Secrets引用、OIDC受众/subject及外部授权，必要变更另行确认；Cloudflare项目名不随GitHub组织自动改名。
10. **根路径与本地预览回归**：确认 `/` 下HTML/CSS/JS/图像/视频/PDF/字体/JSON全部可访问，导航、图片放大、视频播放/拖动与移动端正常；运行 `python3 scripts/package_site.py` 生成静态 `dist/`，避免使用带Cloudflare Worker的托管副本发布到未来GitHub Pages。该步骤不上传或启用站点。
11. **第一阶段交接并停止**：提供前后仓库映射、Private证明、refs/元数据核验、修改清单、本地预览地址和剩余问题。GitHub Pages保持禁用，等待用户明确下一阶段授权。

## GitHub 网页操作位置（组织已创建，仓库操作尚未执行）

- **创建组织**：头像 → Settings → Organizations → New organization → GitHub Free → Organization name。
- **转移仓库**：源仓库 → Settings → General → 页面底部Danger Zone → Transfer ownership → 选择目标组织；核对名称和可见性提示，最终确认按钮前再次征求用户确认。
- **改名**：转移后的仓库 → Settings → General → Repository name → 填目标名 → Rename；点击前征求确认。
- **不启用Pages**：第一阶段不在Settings → Pages选择发布来源，不运行发布Actions。

## 转移需核对的GitHub规则

- 原生转移保留提交及平台元数据；仓库ID和各分支/标签SHA用于前后核对。
- Secrets、Webhooks、deploy keys通常随仓库保留，但外部服务绑定、组织策略和Actions执行权限需另核验。
- 个人仓库转入组织后，不属于组织的Issue assignee可能被清除；如代码仓库存在此类分配，要先与用户确认处理方式。
- Private仓库转入Free组织可能失去受保护分支等付费功能。主页保护接口本次返回403，不能认定无规则；算法仓库不在本轮范围，不能承诺其全部设置完全保留。
- 旧仓库地址通常重定向，但不能在旧账号重建相同路径；GitHub Pages旧网址本身不保证随仓库转移重定向。
- 公开阶段单独检查当前文件及完整历史，发现敏感内容即停下报告；不擅自重写历史。算法代码公开与主页公开分别确认。

官方参考：

- https://docs.github.com/en/repositories/creating-and-managing-repositories/transferring-a-repository
- https://docs.github.com/en/organizations/collaborating-with-groups-in-organizations/creating-a-new-organization-from-scratch
- https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages

只读API盘点：`output/private-migration-inventory.json`（本地忽略目录，不是公开发布文件）。本报告不代表第二阶段的完整历史敏感信息审计已经完成。
