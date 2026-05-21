# Day 4: RAG + Agent + Frameworks + Vibe Coding + MCP 学习对话记录

**日期**: 2026-05-21
**主题**: Day 4 集中学习 5 篇 AI 基础文档，完成 Phase 1 全部内容

---

## 目录

1. [模型切换与配置](#一模型切换与配置)
2. [学习笔记生成与 Prompt 工程设计](#二学习笔记生成与-prompt-工程设计)
3. [RAG 学习对话](#三rag-学习对话)
4. [Agent 学习对话](#四agent-学习对话)
5. [Frameworks 学习对话](#五frameworks-学习对话)
6. [Vibe Coding 学习对话](#六vibe-coding-学习对话)
7. [MCP 学习对话](#七mcp-学习对话)
8. [核心观点总结](#核心观点总结)
9. [文件产出](#文件产出)

---

## 一、模型切换与配置

### 1.1 模型切换：Qwen → DeepSeek V4 Pro

**用户问题**: 切换 Hermes 模型到 DeepSeek V4 Pro

**回答要点**:
- 配置 `model.base_url = https://api.deepseek.com`
- 配置 `model.default = deepseek-v4-pro`
- 配置 API Key + provider = custom
- 验证 HTTP 200 成功

| 项目 | 内容 |
|------|------|
| 结论 | DeepSeek V4 Pro 配置成功，后续所有学习均使用此模型 |

---

## 二、学习笔记生成与 Prompt 工程设计

### 2.1 Prompt 模板迭代（5 轮讨论）

**用户问题**: Prompt 模板需要统一输出格式、加目录、禁止省略模板、加文件命名规则

**回答要点**:
- 输出从纯 JSON 改为 md 格式含目录
- 新增「禁止省略任何模板」约束
- 新增文件命名规则：`day{N}-{主题}.md`
- 禁止同天顺延编号

| 项目 | 内容 |
|------|------|
| 结论 | `review-note-generator` v2.0 定稿，支持预览后保存 + 自适应章节 |

### 2.2 工作流 Prompt 体系设计（4 个新 Prompt）

**用户问题**: 需要 Logs 收集、Prompt 收集、README 更新、检查 Push 四个 Prompt 配置

**回答要点**:
- ① review-note-generator：文档 → 笔记，先预览后保存
- ② daily-logs-collector：对话 → 结构化日志，一天一个文件
- ③ daily-prompts-collector：提取当天四段式 Prompt
- ④ daily-readme-updater：更新 week1 进度，不 push
- ⑤ daily-push-checker：校验 Day N → 合并 → git 预览 → 确认 push

| 项目 | 内容 |
|------|------|
| 结论 | 5 个 Prompt + 5 个 Skill 全部注册，工作流 ①→②→③→④→⑤ 跑通 |

### 2.3 合并机制设计（方案 C）

**用户问题**: 一天学多篇文档，怎么合并为一个文件

**回答要点**:
- ① 每次独立保存（day4-rag.md, day4-agent.md …）
- ⑤ push 时检测合并：Day N 校验 → 合并 → 删除原始文件
- 合并后在末尾生成 `📊 各章节生成信息` 表格（动态提取模型 + 时间）

| 项目 | 内容 |
|------|------|
| 结论 | 合并逻辑归入 ⑤ daily-push-checker，实现 ① 只管生成、⑤ 管合并 |

### 2.4 末尾生成信息 + 最小实践/挑战自适应

**用户问题**: 每篇笔记末尾需要标注模型和日期，最小实践和挑战按源文档有无决定是否生成

**回答要点**:
- 末尾统一格式：`*AI x Web3 School Day N 课程完成 — 由 Hermes AI（模型：xxx）在 YYYY-MM-DD 生成*`
- 最小实践和挑战仅源文档包含对应章节时出现，否则跳过
- 最小实践后加 `📂 Demo 地址：[待补充]()` 占位

| 项目 | 内容 |
|------|------|
| 结论 | ① Skill 支持自适应章节，⑤ Skill 合并时汇总最小实践 + 挑战 + 📊 表格 |

### 2.5 课程全景发现

**用户问题**: Week 1 到底有多少内容？

**回答要点**:
- Week 1 = 11 篇 AI 基础、Week 2 = 10 篇 Web3 基础、Week 3 = 14 篇 AI×Web3 Bridge、Week 4 = Tracks + 项目
- 用户的 Day 编号应改为按周追踪实际进度

| 项目 | 内容 |
|------|------|
| 结论 | 已修正课程认知！后续 Day 按当天实际学习天数追踪，不再硬套 7 天 |

---

## 三、RAG 学习对话

### 3.1 RAG 核心理解

**用户问题**: 直接用 Prompt 模板生成 RAG 笔记

**回答要点**:
- RAG 是一条取回→筛选→引用→交付的证据链
- Citation + Freshness 是底线
- 检索失败允许拒答
- Chunking 要按结构切不按字数

| 项目 | 内容 |
|------|------|
| 结论 | RAG 笔记生成，含 4 个模板：切分规则/存储规范/Citation 格式/最小实践输出 |

---

## 四、Agent 学习对话

### 4.1 Agent 核心理解

**用户问题**: 学 Agent 篇

**回答要点**:
- Agent = 目标/工具/状态/权限/停止条件五要素
- 工具比回答更危险（读/写/支付分级）
- State 必须外置可查
- Reflection 是辅助不是安全边界
- Multi-Agent 先问必要性

| 项目 | 内容 |
|------|------|
| 结论 | Agent 笔记生成，含 3 个模板：执行循环五要素/Tool Use 问卷/AI×Web3 链路 |

---

## 五、Frameworks 学习对话

### 5.1 Frameworks 核心理解 + 最小实践

**用户问题**: 最小实践必须清楚，否则不好做 demo

**回答要点**:
- 框架的本质是把 Agent 设计原则变成工程约束
- 最小实践重写为 A/B 双路径完整对比
- 末尾模型名修正为 deepseek-v4-pro

| 项目 | 内容 |
|------|------|
| 结论 | Frameworks 笔记 v2 重写，最小实践逐步骤展开，Demo 占位已加 |

---

## 六、Vibe Coding 学习对话

### 6.1 Vibe Coding 核心理解

**用户问题**: 一次确认即保存（含最小实践 + 挑战）

**回答要点**:
- Vibe Coding = 人定方向/约束/验收，Agent 搜/改/测
- 最小实践：选小功能走完完整工程闭环
- 挑战：安装配置至少一个 Vibe Coding 工具

| 项目 | 内容 |
|------|------|
| 结论 | Vibe Coding 笔记含最小实践 + 挑战，两个 Demo 占位 |

---

## 七、MCP 学习对话

### 7.1 MCP 核心理解

**用户问题**: 确认保存

**回答要点**:
- MCP 是把工具接入标准化的协议
- Server 设计核心是边界（暴露什么/只读还是写入/权限在哪）
- 最小实践：做只读 MCP Server（2 工具 + 5 硬性要求 + 4 验证项）

| 项目 | 内容 |
|------|------|
| 结论 | MCP 笔记含最小实践，无挑战（源文档无此章节） |

---

## 核心观点总结

| 概念 | 要点 |
|------|------|
| RAG | 证据链不是向量库，Citation + Freshness 是底线 |
| Agent | 五要素约束的执行循环，工具比回答更危险 |
| Frameworks | 框架本质是约束层，把设计原则变成工程检查项 |
| Vibe Coding | 人定边界 Agent 执行，质量责任在人不在 AI |
| MCP | 工具接入标准化协议，Permission 是最被低估的问题 |
| Prompt 设计 | 四段式结构 + 预览后保存 + 自适应章节 + 末尾生成信息 |
| 工作流 | ①→②→③→④→⑤ 闭环，合并逻辑归 ⑤ |

---

## 文件产出

| 文件 | 用途 |
|------|------|
| notes/week1/day4-rag.md | RAG 学习笔记 |
| notes/week1/day4-agent.md | Agent 学习笔记 |
| notes/week1/day4-frameworks.md | Frameworks 学习笔记 |
| notes/week1/day4-vibe-coding.md | Vibe Coding 学习笔记 |
| notes/week1/day4-mcp.md | MCP 学习笔记 |
| prompts/学习笔记生成Prompt.md | ① review-note-generator 配置 |
| prompts/当天Logs学习记录.md | ② daily-logs-collector 配置 |
| prompts/当天Prompt学习记录.md | ③ daily-prompts-collector 配置 |
| prompts/当天README更新配置.md | ④ daily-readme-updater 配置 |
| prompts/当天检查与Push配置.md | ⑤ daily-push-checker 配置 |
