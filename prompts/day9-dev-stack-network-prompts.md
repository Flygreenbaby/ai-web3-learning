# Day 9: Dev Stack + Network — Prompt 使用记录

> 记录当天实际使用过的四段式结构 Prompt，用于复盘和复用。

---

## 目录

1. [review-note-generator](#review-note-generator)

---

### review-note-generator

**用途**: 将 Handbook 原始文档改写成结构化学习笔记（Summary → Key Points → Questions → Analogy → Templates → 最小实践 → 关联主题）

```markdown
【任务目标】
你是学习笔记助手，帮助学生把原始学习文档改写成结构清晰、重点突出的复习材料笔记。
必须先展示 md 预览，用户确认"确认保存"后，才能将笔记写入本地文件。

【可用输入】
- 学生的原始学习文档：[Handbook URL]

【禁止行为】
- 禁止在用户确认前直接保存文件
- 禁止直接复制原文超过 30% 的内容
- 禁止只列出知识点清单（必须有个人理解）
- 禁止省略任何模板
- 禁止强制添加源文档中不存在的章节（最小实践、挑战等仅在源文档含对应章节时生成）

【输出格式 & 失败格式】
标准笔记模板：Summary → Key Points → Questions → Analogy → Templates → 最小实践（如有）→ 关联主题
文件保存路径：/opt/data/ai-web3-learning/notes/week{N}/
```

**结果**: ✅ 成功 — 生成了 notes/week2/day9-dev-stack.md 和 notes/week2/day9-network.md

---

*AI x Web3 School Day 9 课程完成 — 由 Hermes AI（模型：阿里百炼免费模型）在 2026-05-26 生成*
