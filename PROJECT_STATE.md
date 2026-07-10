# PROJECT_STATE

## 当前状态

- GitHub Actions 已部署到 Fork 的 `main` 分支，每 6 小时自动运行一次，也支持手动触发。
- 已配置 4 个 AnyRouter 账号和 3 个 AgentRouter 访问令牌账号。
- AgentRouter 第 3 个账号使用数字用户 ID `197632`。
- 已配置 QQ 邮箱通知，SMTP 授权信息保存在 GitHub Environment Secrets 中。
- 敏感配置保存在 GitHub `production` Environment Secrets 中，仓库不包含明文凭据。

## 关键实现

- AgentRouter 访问令牌请求优先使用精简 HTTP/1.1 请求；失败时保留浏览器回退。
- 自动签到 Provider 首次用户信息请求成功后不再重复请求，降低 WAF 触发概率。
- Mihomo 支持 `PROXY_NODE_FILTER`，工作流固定到已验证兼容 AgentRouter 的代理节点。
- 代理配置失败会直接终止任务，避免 AgentRouter 在无代理状态下继续运行。

## 验证记录

- 本地 AgentRouter：3/3 成功。
- Ruff lint/format：通过。
- Pytest：27 passed，1 skipped。
- GitHub Actions run `29086336275`：7/7 成功，0/7 失败。
- 对应功能提交：`d033ea4`。
- QQ SMTP 测试邮件：发送成功。

## 最近完成

- 【Codex】【2026-07-10】完成 GitHub Actions 自动签到部署、AgentRouter 访问令牌适配、代理节点固定与云端 7/7 验证。
- 【Codex】【2026-07-10】完成 QQ 邮箱通知配置，并通过 SMTP 实际发送测试邮件。
