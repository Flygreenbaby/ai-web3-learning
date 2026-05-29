# Day 12: AI基础实践补全 — Prompt 使用记录

> 记录当天实际使用过的四段式结构 Prompt，用于复盘和复用。

---

## 目录

1. [每日学习工作流触发](#每日学习工作流触发)

---

### 每日学习工作流触发

**用途**: 触发 Hermes 学习助手执行每日标准化收尾流程（日志、Prompt、README、打卡、Push）。

```markdown
【任务目标】
执行②到⑥的Prompt，还有记得生成打卡笔记草稿，向我展示确认后保存

【可用输入】
- 当天完成的学习笔记和实践文件
- 当前对话上下文

【禁止行为】
- 禁止跳过需求，禁止直接实现所有需求（打卡草稿需展示确认）
- 禁止私自 git push

【输出格式 & 失败格式】
1. 执行 ② daily-logs-collector
2. 执行 ③ daily-prompts-collector
3. 执行 ④ daily-readme-updater
4. 执行 ⑥ 每日打卡草稿生成（展示给用户）
5. 用户确认后，执行 ⑤ daily-push-checker
```

**结果**: ✅ 成功 — 触发了 Day 12 的完整收尾流程。

---

*Prompt 记录生成 — 由 Hermes AI（模型：qwen3.7-max-preview）在 2026-05-29 生成*
