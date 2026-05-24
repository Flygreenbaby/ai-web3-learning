# Day 7: Agent + Frameworks 实践 — 学习日志

**日期**: 2026-05-24

---

## Agent 实践：DAO 提案研究 Agent

### 核心收获

1. **Agent 五要素不是背概念，是用来填空的格子**
   → Goal / Tools / State / Permission / Stop，每填一格都是一次设计决策
   
2. **停止条件 ≠ 出错**
   → "提案不存在"是正确的停止，不是 bug。Agent 诚实地告诉用户"我做到这里了"
   
3. **权限升级版的本质是"加一个写入通道"**
   → 只读版完成 → 用户授权 → simulation → 二次确认 → 生成交易草稿

### 踩坑

- 刚开始写得太模糊（"状态=记录搜索状态"），被要求改成可查询字段清单
- 输出格式只说"来源、总结、风险、检查清单"四个词，缺少结构化 schema

### 产出

- `experiments/week1-agent-dao-research.md`

---

## Frameworks 实践：Raw API vs DSPy 框架对比

### 核心收获

1. **框架的"隐形收益"是测试纪律**
   → Raw API 版本只跑了一个用例；DSPy 版本天然跑了两个（含边界情况 #999）
   
2. **框架的代价是依赖膨胀**
   → DSPy → LiteLLM → botocore 警告，依赖链比实际需要长
   
3. **简单任务 Raw API 更可控；复杂任务框架优势才显现**
   → 互补而非互斥：先 Raw 验证思路 → 再框架工程化

### 实操

- 利用之前的 rag-practice venv，安装 openai + dspy-ai
- DeepSeek API key 失效 → 重新生成 → 两个版本均跑通
- DSPy 的 Signature → Module → test_cases 模式比 LangChain 轻量

### 产出

- `experiments/week1-frameworks-compare.md`
- `experiments/week1-frameworks/raw_api.py`
- `experiments/week1-frameworks/framework.py`

---

## Vibe Coding 实践：暂停

因为本地缺少 Node.js 环境，挑战（安装工具）留待后补。

---

## 今日总结

| 篇目 | 实践 | 状态 |
|------|:--:|:--:|
| ⑤ Agent | DAO 提案研究 Agent | ✅ |
| ⑥ Frameworks | Raw API vs DSPy 对比 | ✅ |
| ⑦ Vibe Coding | 暂停 | ⏸️ |

Week 1 实践进度：**6/11 完成**（LLM→Prompt→Context→RAG→Agent→Frameworks）

---

*AI x Web3 School Day 7 课程完成 — 由 Hermes AI（模型：deepseek-v4-pro）在 2026-05-24 生成*
