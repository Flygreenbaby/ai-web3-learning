# Week 1 Frameworks 实践：文档问答 + 工具调用 — 框架对比

**来源**: [Handbook — 框架（Frameworks）](https://aiweb3.school/zh/handbook/ai/frameworks/)  
**完成日期**: 2026-05-24

---

## 实践目标

同一个「文档问答 + 工具调用」任务，用两方式实现并对比：
- 直接调用 DeepSeek API
- 使用 DSPy 框架

---

## 任务设计

### 场景
模拟 DAO 研究助手：用户提问 → 检索模拟文档 → 输出结构化 JSON

### 模拟文档
```
提案 #42：将金库 5% 分配给 Grants 计划，锁定期 6 个月，由多签控制。
论坛讨论 #1：支持方认为 Grants 能吸引开发者，反对方担心资金滥用。
论坛讨论 #2：提议先做 1% 试点，评估效果后再追加。
```

### 测试用例
| # | 问题 | 预期 |
|---|------|------|
| 1 | 提案 #42 的支持/反对理由 + 风险？ | 有回答 + 有来源 |
| 2 | 提案 #999 是什么？ | 无相关文档 |

---

## 版本 A：直接调用 API

**代码**：`experiments/week1-frameworks/raw_api.py`（~75 行）

**运行结果**：
```json
{
  "answer": "提案 #42 的支持理由：Grants 能吸引开发者。反对理由：担心资金滥用。风险：资金滥用是主要担忧，1% 试点建议暗示 5% 直接分配存在执行不确定风险。",
  "sources_used": ["提案 #42", "论坛讨论 #1", "论坛讨论 #2"],
  "confidence": "medium",
  "missing_info": ["具体风险细节", "支持/反对更详细论据"]
}
```

---

## 版本 B：DSPy 框架

**代码**：`experiments/week1-frameworks/framework.py`（~85 行）

**运行结果**：

*测试 1*：正常检索 → confidence medium → 3 个来源 + 缺失信息标注

*测试 2（提案 #999）*：
```
来源: []
置信度: low
缺失信息: ['提案 #999 的具体内容、目标、资金分配等详细信息']
```
→ 正确拒答，未编造内容 ✅

---

## 四维对比

| 维度 | 版本 A（Raw API） | 版本 B（DSPy） | 结果 |
|------|------|------|:--:|
| 更易读懂？ | 线性流程，~75 行。prompt 和解析写在一起 | 三层结构，多一个 Signature 概念 | **A** |
| 更易加工具？ | 改 prompt + JSON schema + 函数签名三处 | 加一个 InputField 即可 | **B** |
| 更易定位错误？ | 401 直接报行号，一目了然 | LiteLLM 套一层，堆栈更深 | **A** |
| 更易写回归测试？ | 无测试框架，需手写 assert | test_cases 数组直接定义 | **B** |

---

## 关键发现

1. **框架的"隐形收益"是测试纪律**：A 版本只跑了一个用例，B 版本天然跑了两个——框架把测试变成了代码结构，而不是"以后再说"
2. **框架的代价是依赖膨胀**：DSPy → LiteLLM → botocore 警告，依赖链比实际需要更长，出错时排查更难
3. **本次不是选冠军**：简单任务（一个 tool + 三次调用）Raw API 更可控；复杂任务（多 tool + 多步 + 多模型）框架优势才显现
4. **互补而非互斥**：先 Raw 验证思路 → 再用框架工程化，是最稳妥的路线

---

## 练习心得

- 第一次用 DSPy，Signature → Module → test_cases 的模式比 LangChain 轻量很多
- DeepSeek API 的 OpenAI 兼容接口可以无缝对接到 DSPy，只需改 api_base
- LiteLLM 的 botocore 警告无影响，可忽略——但不该有这么多无关依赖

---

## 运行环境

- **依赖**：Python 3, openai, dspy-ai
- **虚拟环境**：`%USERPROFILE%\rag-practice\venv`（与 RAG 实践共用）
- **模型**：DeepSeek Chat
- **API**：DeepSeek API（OpenAI 兼容）

---

*AI x Web3 School Week 1 Frameworks 实践完成 — 由 Hermes AI（模型：deepseek-v4-pro）在 2026-05-24 生成*
