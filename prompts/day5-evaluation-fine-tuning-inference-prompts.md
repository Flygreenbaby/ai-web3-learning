# Day 5: Evaluation + Fine-tuning + Inference — Prompt 使用记录

> 记录当天实际使用过的四段式结构 Prompt，用于复盘和复用。

---

## 目录

1. [review-note-generator v2](#1-review-note-generator-v2)
2. [daily-logs-collector](#2-daily-logs-collector)
3. [每日打卡草稿生成 Prompt ⑥](#3-每日打卡草稿生成-prompt-⑥)

---

### 1. review-note-generator v2

**用途**: 将 Evaluation / Fine-tuning / Inference 三篇 Handbook 文档同时生成结构化学习笔记

```markdown
【任务目标】
你是学习笔记助手，帮助学生把原始学习文档改写成结构清晰、重点突出的复习材料笔记。
必须先展示 md 预览，用户确认"确认保存"后，才能将笔记写入本地文件。

【可用输入】
- https://aiweb3.school/zh/handbook/ai/evaluation/
- https://aiweb3.school/zh/handbook/ai/fine-tuning/
- https://aiweb3.school/zh/handbook/ai/inference/

【禁止行为】
- 禁止强制添加源文档中不存在的章节
- 禁止在用户确认前直接保存文件
- 同一天 Day N 保持一致

【输出格式】
三篇独立笔记 → 预览确认 → 分别保存为 day5-evaluation.md / day5-fine-tuning.md / day5-inference.md
每篇含 Summary / Key Points / Questions / Analogy / Templates / 关联主题
```

**结果**: ✅ 成功 — 生成 notes/week1/day5-evaluation.md、day5-fine-tuning.md、day5-inference.md

---

### 2. daily-logs-collector

**用途**: 从当天对话历史提炼 Day 5 学习日志

```markdown
【任务目标】
从 Hermes Agent 当天对话历史提炼结构化学习日志，保存到 logs/

【可用输入】
- 当天对话历史（仓库初始化 + 三篇笔记生成 + 目录讨论）
- 仓库路径：/opt/data/ai-web3-learning/

【禁止行为】
- 禁止虚构未发生的对话
- 禁止记录敏感信息

【输出格式】
# Day 5: [主题概括] 学习对话记录
→ 仓库初始化 / Evaluation / Fine-tuning / Inference 四大章节
→ 核心观点总结 + 文件产出表格
```

**结果**: ✅ 成功 — 生成 logs/day5-evaluation-fine-tuning-inference-qa.md

---

### 3. 每日打卡草稿生成 Prompt ⑥

**用途**: 新建 Prompt，补齐 daily/ 打卡链路

```markdown
【任务目标】
从当天笔记和日志提炼打卡草稿，保存到 daily/，用于 WCB 提交

【可用输入】
- notes/week1/day5-*.md
- logs/day5-*-qa.md
- templates/daily-note.md

【禁止行为】
- 禁止虚构进度
- 禁止在确认前保存
- 禁止暴露敏感信息

【输出格式】
按 templates/daily-note.md 结构：今日计划 / 学习摘要 / 打卡草稿 / 明日备忘
保存到 daily/YYYY-MM-DD.md
```

**结果**: ✅ 成功 — 保存到 prompts/每日打卡草稿生成.md
