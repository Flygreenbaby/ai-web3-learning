# Day 4: RAG（检索增强生成）— AI 基础学习笔记

**文档来源**: https://aiweb3.school/zh/handbook/ai/rag/
**生成日期**: 2026-05-21

---

## 目录

1. [Summary](#summary)
2. [Key Points](#key-points)
3. [Questions](#questions)
4. [Analogy](#analogy)
5. [Templates](#templates)
6. [关联主题](#关联主题)

---

## Summary

RAG 不是"接向量库"——是一条取回→筛选→引用→交付的证据链，让回答有来源、有版本、有边界。

---

## Key Points

1. **RAG 的核心是证据链，不是向量库** —— 文档怎么切、取哪些内容、如何引用和拒答，三层任何一层出错，模型都会拿着错误材料说得很顺
2. **Citation 和 Freshness 是 RAG 的底线** —— 没有来源标注和时效信息的 RAG，只是把幻觉从模型内部搬到了检索系统
3. **检索结果 ≠ 事实** —— 它只是候选证据，仍然要看来源、时间、版本、适用范围
4. **检索失败要允许拒答** —— 找不到证据时说"不确定"，而不是让模型补全
5. **Chunking 要按结构切，不能按固定字数** —— 技术文档的函数说明、参数表、风险提示常跨段落，按标题/API endpoint/小节切更稳

---

## Questions

1. RAG 和之前学的 Context Engineering 有什么区别？Context 是"整理好桌面"，RAG 是"从档案馆取文件放在桌面上"——二者如何配合？
2. Rerank 什么时候加？如果一次检索返回 50 条候选，Rerank 的加不加判断标准是什么？成本 vs 效果如何取舍？
3. 在 Web3 场景中，RAG 取回的"旧版本文档"可能导致用户执行已废弃的合约接口——Citation 的版本标注能否堵住这个风险？还需要什么辅助机制？

---

## Analogy

> RAG 就像给 AI 配了一个**带索引的档案馆**：
> - 查到了 → 把文件编号、段落、版本一起交给 AI 参考
> - 查不到 → AI 说"档案里没有，我不能编"
> - 查到但版本旧了 → AI 提示"这是 2023 年的文档，建议核对最新版"

---

## Templates

### 1️⃣ Chunking 切分规则

```markdown
【切分原则】
- 按文档结构切：标题 > 小节 > 段落，不按固定字数
- 每个 chunk 附带 metadata：来源 URL、更新时间、版本号

【示例】
文档: solidity-by-example.md
├── chunk_001: "## 合约结构" → metadata: {source: "solidity-by-example.md", section: "合约结构", version: "0.8.20"}
├── chunk_002: "## 状态变量" → metadata: {source: "solidity-by-example.md", section: "状态变量", version: "0.8.20"}
└── chunk_003: "## 函数"     → metadata: {source: "solidity-by-example.md", section: "函数", version: "0.8.20"}
```

### 2️⃣ Vector DB 存储规范

```json
{
  "id": "chunk_uuid",
  "embedding": [0.123, -0.456, ...],
  "metadata": {
    "source_url": "https://docs.example.com/api/v2",
    "source_type": "official_doc",
    "last_updated": "2025-03-15",
    "version": "v2.1.0",
    "section": "POST /users",
    "chunk_index": 3,
    "total_chunks": 12
  },
  "content": "POST /users 接口的完整说明文本..."
}
```

**检索流程**：先 `metadata filter`（只搜 official_doc + 近 6 个月），再 `vector similarity rank`。

### 3️⃣ Citation 引用格式

```json
{
  "answer": "该接口需要 x-api-key 头部...",
  "citations": [
    {
      "source_url": "https://docs.example.com/api/v2",
      "source_type": "official",
      "version": "v2.1.0",
      "section": "Authentication",
      "quote_snippet": "...x-api-key 用于验证请求来源..."
    }
  ],
  "unsupported_claims": [
    "旧版本文档中提到的 api-key（v1 格式）已废弃，未在 v2.1.0 中找到对应说明"
  ],
  "needs_human_verification": false
}
```

**规则**：每个关键结论必须有 citation 支撑；没有 citation 的声明归入 `unsupported_claims`。

### 4️⃣ 最小实践输出结构

```json
{
  "query": "用户原始问题",
  "answers": [
    {
      "claim": "具体回答",
      "citations": [{ "source_url": "...", "section": "...", "version": "..." }]
    }
  ],
  "sources": [
    { "url": "...", "type": "official_doc", "version": "v2.1.0", "relevance": "high" }
  ],
  "uncertainties": ["v2.0 和 v2.1 的参数名不一致，建议核对"],
  "needs_version_check": true,
  "refused": false
}
```

---

## 关联主题

- [Context](https://aiweb3.school/zh/handbook/ai/context/) — RAG 的上游：如何把检索结果放进 Context
- [Agent](https://aiweb3.school/zh/handbook/ai/agent/) — Agent 用 RAG 补充上下文后执行多步操作
- [Chain-aware Context](https://aiweb3.school/zh/handbook/bridge/chain-aware-context/) — 链上状态进入检索结果
- [Memory](https://aiweb3.school/zh/handbook/ai/memory/) — RAG 和 Memory 如何分工

---

*AI x Web3 School Day 4 课程完成*
