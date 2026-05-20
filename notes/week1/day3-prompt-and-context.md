# Day 3: Prompt Engineering & Context Engineering — AI 基础学习笔记

**文档来源**: 
- Prompt: https://aiweb3.school/zh/handbook/ai/prompt/
- Context: https://aiweb3.school/zh/handbook/ai/context/
**生成日期**: 2026-05-20

---

## 第一部分：Prompt Engineering

### 📌 Summary (30 字以内)

Prompt 是人与模型的接口设计，核心不是"怎么问"而是将任务目标、约束、格式写成可执行协议。

---

### 💡 Key Points

1. **Prompt 是软约束，不是安全边界** —— 真正的安全必须由代码、权限、校验和审计保障
2. **四段式 Instruction 结构** —— [任务目标] [可用输入] [禁止行为] [输出格式 & 失败格式]
3. **Few-shot vs Structured Output** —— Few-shot 用于风格模仿，Structured Output 用于机器处理
4. **Prompt Injection 风险** —— 外部输入可能覆盖原始规则，需代码层校验 + 人工审批
5. **高风险动作不能仅靠 Prompt** —— 必须增加代码层校验和人工确认

---

### ❓ Questions (深挖方向)

1. 如何设计一个"防注入"的 Prompt 结构？有没有可复用的模板？
2. Few-shot 示例的维护成本如何？协议升级时如何避免旧示例误导？
3. Structured Output 的 schema 设计有哪些最佳实践？

---

### 🎯 Analogy (比喻解释)

> Prompt 就像给 AI 的**工作指令单**——不是告诉它"做什么"，而是明确：
> - 你是谁（角色）
> - 你要做什么（任务）
> - 你不能做什么（约束）
> - 你要怎么交卷（格式）
> 
> 好的 Prompt 设计就是"**把模糊的需求翻译成机器可执行的协议**"。

---

### 📋 Templates (从文档提取的实际模板)

#### 1️⃣ 四段式 Instruction 结构

```markdown
[任务目标]
清晰描述 AI 需要完成的任务，例如："总结以下技术文档的核心观点"

[可用输入]
列出 AI 可以使用的信息来源，例如：
- 用户提供的文档
- 系统预设的配置
- 检索到的相关资料

[禁止行为]
明确列出 AI 不能做的事情，例如：
- 不能替用户确认交易
- 不能泄露内部系统信息
- 不能执行不可逆操作

[输出格式 & 失败格式]
指定输出结构，例如 JSON 格式：
```json
{
  "summary": "核心观点摘要",
  "key_points": ["要点1", "要点2"],
  "confidence": "high/medium/low"
}
```

失败时返回：
```json
{
  "error": "失败原因",
  "suggestion": "建议操作"
}
```
```

#### 2️⃣ Few-shot 示例模板

```markdown
## 示例 1：普通转账
输入：用户要转账 100 USDT 到地址 0x123...
输出：
```json
{
  "action": "explain_transaction",
  "risk_level": "low",
  "requires_human_approval": false,
  "uncertainties": []
}
```

## 示例 2：无限授权
输入：用户要授权某个合约无限额度
输出：
```json
{
  "action": "explain_transaction",
  "risk_level": "high",
  "requires_human_approval": true,
  "uncertainties": ["无限授权可能导致资金被盗"]
}
```
```

#### 3️⃣ Structured Output Schema 示例

```json
{
  "action": "explain_transaction" | "prepare_swap" | "reject",
  "risk_level": "low" | "medium" | "high",
  "requires_human_approval": true | false,
  "uncertainties": ["unverifiable_fact_1"],
  "asset_changes": [
    {
      "token": "USDT",
      "amount": "-100",
      "direction": "out"
    }
  ],
  "permissions_changed": [],
  "recommended_user_checks": ["确认目标地址是否正确"]
}
```

---

### 🔗 Prompt 关联主题

- [Context](https://aiweb3.school/zh/handbook/ai/context/) — 信息治理与可信来源
- [RAG](https://aiweb3.school/zh/handbook/ai/rag/) — 检索增强生成
- [Agent Workflow](https://aiweb3.school/zh/handbook/ai/agent-workflow/) — 智能体工作流

---

## 第二部分：Context Engineering

### 📌 Summary (30 字以内)

Context 是模型能看见的信息空间，核心不是塞更多内容而是区分可信来源与权限边界。

---

### 💡 Key Points

1. **Context ≠ 简单拼接** —— 必须把系统规则、用户目标、历史状态、工具结果和外部文档分清楚
2. **Prompt 是软约束，Context 是信息治理** —— 每类信息要标注来源、时效、权限和可信度
3. **长上下文常见问题** —— "看见了但没抓住重点"，需要用检索、摘要和结构化数据配合
4. **记忆要可撤销** —— 用户偏好不能变成隐藏权限或永久身份假设
5. **高风险动作重新授权** —— 涉及资产/外部副作用的记忆必须绑定当前会话和当前授权

---

### ❓ Questions (深挖方向)

1. 如何判断一个 Context 中的信息应该标记为"高可信"还是"低可信"？有没有具体的标准？
2. 在 Agent 场景中，如何设计"上下文刷新机制"避免过期状态导致越权操作？
3. 当 Context Window 接近上限时，优先级排序的策略是什么？（最新 vs 最相关 vs 最关键）

---

### 🎯 Analogy (比喻解释)

> Context 就像给 AI 的**工作桌面**——桌面上放的文件种类决定了它能做什么：
> - 如果把旧合同和新需求混在一起 → 它会混淆执行
> - 如果把机密文件和公开资料混在一起 → 它会泄漏信息
> - 如果桌面堆满无关文件 → 它会找不到重点
> 
> 好的 Context 设计就是"**整理好桌面再给 AI 工作**"。

---

### 📋 Templates (从文档提取的实际模板)

#### 1️⃣ Context Engineering 稳定结构示例

```markdown
【用户问题】用户原始输入
【当前任务状态】进行中/已完成/待处理
【工具返回结果】JSON 格式的工具调用输出
【相关日志或证据】时间戳 + 来源标记
【可信数据来源】明确标注 URL 或系统字段
【外部检查结果】来自 API/链上的验证信息
【用户原始意图】用自然语言描述的目标
【系统禁止事项】如"不要替用户确认交易"
【输出 schema】结构化输出字段定义
```

#### 2️⃣ Context 信息来源分级表

| 类型 | 可信度 | 处理方式 |
|------|--------|----------|
| 系统状态/配置 | ✅ 高可信 | 直接放入 Context 顶层 |
| 用户输入 | ⚠️ 中可信 | 需要参数校验后再使用 |
| 检索文档 | ⚠️ 中可信 | 标注来源和获取时间 |
| 工具结果 | ⚠️ 需验证 | 检查返回 schema 完整性 |
| 外部网页 | ❌ 低可信 | 隔离层处理，不可直接信任 |

#### 3️⃣ Memory 风险检查清单

```
✅ 所有 Memory 条目都有明确的过期时间或撤销方式
✅ 涉及钱包地址的交易记录需每次重新确认
✅ 记住"用户偏好"不等同于记住"用户授权"
✅ 跨会话的记忆不包含敏感凭证（私钥/API 密钥）
✅ 用户可随时通过设置重置特定类型的记忆
❌ 禁止：根据历史行为自动推断用户风险偏好
❌ 禁止：长期缓存用户资产余额用于决策
❌ 禁止：默认上次任务的上下文延续到下次任务
```

---

### 🔗 Context 关联主题

- [Prompt](https://aiweb3.school/zh/handbook/ai/prompt/) — 任务规则与输出格式
- [RAG](https://aiweb3.school/zh/handbook/ai/rag/) — 检索增强生成
- [Chain-aware Context](https://aiweb3.school/zh/handbook/ai/agent-workflow/#chain-aware-context) — 链上状态进入 Agent 上下文
- [Memory](https://aiweb3.school/zh/handbook/ai/memory/) — 跨请求保留信息

---

## 第三部分：Prompt vs Context 对比

| 维度 | Prompt | Context |
|------|--------|---------|
| **核心作用** | 定义任务目标和输出格式 | 提供可信信息和边界 |
| **设计重点** | 指令清晰、格式可校验 | 来源标注、权限隔离 |
| **安全层级** | 软约束（可被覆盖） | 信息治理（分级管理） |
| **常见风险** | Prompt Injection | 信息过载、权限越界 |
| **最佳实践** | 四段式结构 + Few-shot + Structured Output | 来源分级 + 可撤销记忆 + 刷新机制 |

---

## 第四部分：综合 Questions (跨主题)

1. **Prompt 和 Context 的边界在哪里？** 什么时候应该放在 Prompt 里，什么时候应该放在 Context 里？
2. **如何设计一个既能防注入又能保持灵活性的系统？** 代码层和 Prompt 层各自承担什么角色？
3. **在 Web3 场景中，Prompt/Context 的设计与普通场景有何不同？** 链上数据、私钥管理、交易确认等特殊需求如何影响设计？

---

*AI x Web3 School Day 3 课程完成*
