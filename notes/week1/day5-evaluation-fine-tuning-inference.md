# Day 5: Evaluation + Fine-tuning + Inference — AI 基础学习笔记

**文档来源**:
- https://aiweb3.school/zh/handbook/ai/evaluation/
- https://aiweb3.school/zh/handbook/ai/fine-tuning/
- https://aiweb3.school/zh/handbook/ai/inference/
**生成日期**: 2026-05-22

---

## 目录

1. [Evaluation 评估](#evaluation-评估)
2. [Fine-tuning 微调](#fine-tuning-微调)
3. [Inference 推理服务](#inference-推理服务)

---

## Evaluation 评估

### Summary
Eval 是把"感觉变好了"变成可重复测量、可防止退化的系统工程——没有它，每次改 prompt/模型/RAG 都是在盲飞。

### Key Points
- **先有 eval，再谈改进**：不能被重复测量的 AI 行为，就不能被稳定改进
- **Harness（框架）**：运行 eval 的脚手架，负责喂样本、调系统、收输出、跑 grader。核心价值是**可重复**
- **Golden Set（黄金集）**：30~100 条精心挑选的测试样本，覆盖正常/边界/高风险/历史 bug
- **LLM-as-Judge**：用模型评模型，适合开放式质量但不等于真相——要定期校准
- **Regression（回归测试）**：把历史问题固化，每次发布前重跑，防止"修 A 坏 B"
- **Observability（可观测性）**：线上看系统真实行为——没有它就不知道该往 Golden Set 里补什么

### Questions
1. LLM-as-Judge 用 GPT-4 评 Claude 输出会不会出现系统性偏差？怎么检测？
2. Golden Set 什么时候淘汰旧样本——有没有"样本腐烂"概念？
3. AI × Web3 高风险场景中哪些**必须** human-in-the-loop？

### Analogy
Eval 就像汽车的**年检 + 行车记录仪**。Harness 是检测线，Golden Set 是固定测试项目，Regression 确保上次修好的毛病不再犯，Observability 是行车记录仪——告诉你真实路况下哪里出了问题。

### Templates
#### 1️⃣ 最小 Eval 流程
```
1. 准备 30 条样本（10 正常 + 10 边界 + 5 历史 bug + 5 恶意/注入）
2. 为每条定义：输入、期望行为、必须包含/拒绝的情况、是否需要引用
3. 每次改 prompt / 模型 / 检索策略前后各跑一遍，记录变化
```

#### 2️⃣ AI × Web3 特评项
```
- 交易解释是否准确
- 风险提示是否漏报
- 工具调用参数是否越界
- 是否能拒绝不确定请求
- 是否能识别 Prompt Injection
- 引用和来源是否可追溯
- 高风险动作是否要求 human check
```

### 🛠️ 最小实践
给"交易解释 / 文档问答 / Agent 工具调用"原型做最小 eval：
1. 准备 30 条样本（10 正常 + 10 边界 + 5 历史 bug + 5 恶意/注入）
2. 为每条定义输入、期望行为、必须包含/拒绝的情况、引用要求
3. 每次改 prompt/模型/检索策略前后跑一遍，记录变化

> 📂 Demo 地址：[待补充]()

### 关联主题
- [提示词（Prompt）](https://aiweb3.school/zh/handbook/ai/prompt/)
- [智能体（Agent）](https://aiweb3.school/zh/handbook/ai/agent/)
- [AI 安全（AI Security）](https://aiweb3.school/zh/handbook/bridge/ai-security/)

---

## Fine-tuning 微调

### Summary
Fine-tuning 的正确打开方式：先用 prompt + few-shot + eval 穷尽手段，确认问题稳定存在且有明确目标后，再用高质量数据训练——它不是万能药，而是"最后一公里"的格式与风格校准工具。

### Key Points
- **FT 不是第一步**：遇到模型输出不好，先检查 prompt / context / RAG / schema
- **SFT（监督微调）**：用输入-期望输出样本训练，适合固定格式、语气、领域术语——数据质量决定一切
- **LoRA（低秩适配）**：不更新全部参数，只训练小适配器，降低成本和显存
- **Dataset 是核心资产**：必须区分训练集/验证集/测试集/回归集，**测试集绝不能参与训练**
- **Overfitting（过拟合）**：训练例子上完美，真实用户一问就崩
- **FT 不能替代**：链上状态、合约审计、交易模拟、钱包权限——模型永远不是可信执行层

### Questions
1. 如果 Golden Set 覆盖不全，微调后 eval 绿灯但上线翻车——怎么判断 eval 本身够不够？
2. LoRA adapter 在高并发推理时会不会成为瓶颈？
3. AI × Web3 的数据标注（如"交易风险摘要"）是不是比通用 NLP 更难？

### Analogy
Fine-tuning 像**给厨师定制菜谱**。SFT 是"照我给的 50 道菜反复练"，LoRA 是"只调关键调料比例"。但如果原始数据有问题——盐当糖放——练出来的厨师会把所有菜做成怪味。定制菜谱不等于厨师突然懂了食品安全法规。

### Templates
#### 1️⃣ SFT 适用场景对照
```
✅ 适合 SFT：固定格式输出、特定语气风格、领域术语、工具调用样式
❌ 不适合 SFT：实时知识更新 → RAG、权限安全边界 → 系统层控制、偶尔格式错误 → prompt+few-shot
```

#### 2️⃣ Dataset 切分标准
```
- 训练集（Training）：用于训练
- 验证集（Validation）：用于调参和选版本
- 测试集（Test）：用于最终评估
- 回归集（Regression）：防止历史问题复发
⚠️ 测试集绝不能拿去训练
```

### 🛠️ 最小实践
做一个"结构化摘要格式"的微调前评估（**先不要训练**）：
1. 准备 50 条样本：输入=技术文档/提案；输出=固定 JSON（summary, risks, open_questions, sources）
2. 比较三种方案：只改 prompt / Prompt + few-shot / 小规模 fine-tuning
3. 用同一套 eval 检查：字段完整度、是否编造来源、风险点是否漏掉、输出稳定性
4. 只有前两种无法稳定解决问题时，再考虑 fine-tuning

> 📂 Demo 地址：[待补充]()

### 关联主题
- [评估（Evaluation）](https://aiweb3.school/zh/handbook/ai/evaluation/)
- [提示词（Prompt）](https://aiweb3.school/zh/handbook/ai/prompt/)
- [推理服务（Inference）](https://aiweb3.school/zh/handbook/ai/inference/)

---

## Inference 推理服务

### Summary
Inference 不是"调 API 拿结果"，而是在延迟、成本、质量、隐私和运维之间做平衡——你选的不是一个模型，而是一整套部署约束下的服务方案。

### Key Points
- **API Model（托管）**：上手快免运维，但速率限制、成本控制、版本变更都要自己处理。Agent 场景多轮调用放大成本和延迟
- **Local Model（本地部署）**：隐私可控、离线可用，但吃硬件、吃运维。适合分类/抽取/轻量 Agent/隐私数据/fallback
- **Quantization（量化）**：FP16→INT8/INT4 省显存，但可能损害代码生成、工具调用质量——必须用任务样本测试
- **Serving（服务化）**：并发队列、流式输出、灰度发布、故障降级。Serving 做不好，模型越强线上越难排查
- **AI × Web3 特需**：链上动作不可逆 → 推理必须留可审计记录：模型/输入/输出/工具调用/失败处理

### Questions
1. 量化模型把 `"amount": 100` 误解成 `"amount": 10`——Web3 里这是灾难性的
2. 不同模型 tool calling 格式不同，model fallback 真的能无缝切换吗？
3. 链上推理审计记录要到什么粒度？token logprobs + 中间 tool call 都要吗？

### Analogy
Inference 像**外卖 vs 自家厨房 vs 中央厨房**。API 是外卖——方便但受制于平台。Local 是自家厨房——完全掌控但你要买设备、备菜、洗碗。Serving 是中央厨房——出餐速度、品质稳定、食品安全、高峰应对。Quantization 是用更小的锅炒菜——省地方但火候更难控制。

### Templates
#### 1️⃣ 推理部署选择矩阵
```
| 场景 | 推荐方案 | 理由 |
|------|---------|------|
| 快速原型 | API Model | 零运维，模型最新 |
| 隐私数据 | Local Model | 数据不出境 |
| 高并发低延迟 | Serving + 量化 | GPU利用率 + 成本优化 |
| Agent 敏感操作 | 留审计日志 | 链上不可逆 |
```

#### 2️⃣ 推理审计记录模板
```
- 模型名称和版本
- 输入来源（去敏后）
- 输出内容（去敏后）
- 是否触发 tool call
- 延迟和 token 消耗
- 失败时 fallback 路径
- 时间戳
```

### 🛠️ 最小实践
做一个最小推理对比：
1. 选同一任务："总结一笔交易的风险"或"从合约 ABI 提取可调用方法"
2. 用托管 API 模型跑一次（如 DeepSeek API）
3. 用本地模型或较小模型跑一次
4. 对比：延迟、成本、输出质量、隐私边界、失败情况
5. 写出产品选择理由和 fallback 设计

> 📂 Demo 地址：[待补充]()

### 关联主题
- [微调（Fine-tuning）](https://aiweb3.school/zh/handbook/ai/fine-tuning/)
- [评估（Evaluation）](https://aiweb3.school/zh/handbook/ai/evaluation/)
- [AI 安全（AI Security）](https://aiweb3.school/zh/handbook/bridge/ai-security/)

---

## 🛠️ 最小实践汇总

**[Evaluation]** 准备 30 条样本（10正常+10边界+5历史bug+5注入），定义输入/期望行为/拒绝条件，每次改 prompt 或模型前后跑一遍。

**[Fine-tuning]** 准备 50 条样本，比较 prompt-only / few-shot / FT 三种方案，用同一套 eval 检查。

**[Inference]** 选同一任务分别用 API 和本地模型跑，对比延迟/成本/质量/隐私，写出 fallback 设计。

> 📂 Demo 地址：[待补充]()

---

## 📊 各章节生成信息

| 章节 | 模型 | 生成时间 |
|------|------|----------|
| Evaluation | deepseek-v4-pro | 2026-05-22 |
| Fine-tuning | deepseek-v4-pro | 2026-05-22 |
| Inference | deepseek-v4-pro | 2026-05-22 |

---

*AI x Web3 School Day 5 课程完成 — 由 Hermes AI（模型：deepseek-v4-pro）在 2026-05-22 生成*
