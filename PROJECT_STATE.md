# PROJECT_STATE

## 当前状态

- GitHub Actions 已部署到 Fork 的 `main` 分支，每 6 小时自动运行一次，也支持手动触发和强制通知测试。
- 自动任务当前只保留 4 个 AnyRouter 账号。
- 3 个 AgentRouter 已暂停自动签到，暂时由用户手动签到。
- 已配置 QQ 邮箱通知，SMTP 授权信息保存在 GitHub Environment Secrets 中。
- 敏感配置保存在 GitHub `production` Environment Secrets 中，仓库不包含明文凭据。

## 关键实现

- AnyRouter 通过浏览器登录并调用签到接口。
- 余额通知保存完整的跨运行快照，以“余额＋累计消耗”的总额度变化识别实际签到奖励。
- AgentRouter 暂停后，工作流已移除不再需要的代理启动步骤。
- 定时任务避开 GitHub Actions 整点高峰，按 UTC 每 6 小时的第 17 分钟触发。
- 当前仓库是公开 Fork；GitHub 未产生任何 `schedule` 运行，手动触发仍正常。已验证禁用再启用工作流及 5 分钟调度探针均无效，需迁移到非 Fork 仓库解决。

## 验证记录

- 本地 AgentRouter：3/3 成功。
- Ruff lint/format：通过。
- Pytest：27 passed，1 skipped。
- GitHub Actions run `29086336275`：7/7 成功，0/7 失败。
- 对应功能提交：`d033ea4`。
- QQ SMTP 测试邮件：发送成功。
- GitHub Actions run `29142935622`：强制首次通知成功，7/7 签到成功，云端邮件推送成功。
- 对比 `29086336275` 与 `29142935622`，4 个 AnyRouter 的总额度均增加 `$25`，确认实际签到成功。
- GitHub Actions run `29143536587`：仅运行 4 个 AnyRouter，4/4 成功，余额快照基线和邮件推送成功。
- GitHub Actions run `29143626358`：跨运行余额快照恢复成功，4/4 成功，正确识别 `$0.44` 使用量并发送邮件。
- 2026-07-13 调度排障：工作流状态为 active，但连续两个 5 分钟窗口均未产生 `schedule` 事件；确认问题位于公开 Fork 调度层。

## 最近完成

- 【Codex】【2026-07-10】完成 GitHub Actions 自动签到部署、AgentRouter 访问令牌适配、代理节点固定与云端 7/7 验证。
- 【Codex】【2026-07-10】完成 QQ 邮箱通知配置，并通过 SMTP 实际发送测试邮件。
- 【Codex】【2026-07-11】修复定时任务未触发问题，将计划错开整点，并通过 GitHub Actions 强制首次通知验证云端邮件发送成功。
- 【Codex】【2026-07-11】暂停 AgentRouter 自动签到；确认 4 个 AnyRouter 实际各增加 25 美元，并修复邮件以跨运行快照显示真实奖励和使用量。
- 【Codex】【2026-07-13】确认公开 Fork 的 GitHub Actions 定时调度未启用；邮件、手动运行和余额比较链路均正常，下一步需迁移到独立仓库。
