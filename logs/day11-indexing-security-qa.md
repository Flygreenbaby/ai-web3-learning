# Day 11: Indexing + Security 学习对话记录

**日期**: 2026-05-28
**主题**: Week 2 最后两篇（索引 + 安全）笔记生成与实践设计

---

## 目录

1. [学习流程执行](#学习流程执行)
2. [实践设计决策](#实践设计决策)
3. [核心观点总结](#核心观点总结)
4. [文件产出](#文件产出)

---

## 一、学习流程执行

### 1.1 笔记生成流程

**用户请求**: 使用 review-note-generator 学习 Indexing 和 Security 两篇文档，要求包含实践和挑战

**执行过程**:
- 抓取 Indexing 文档内容 → 生成笔记预览 → 用户确认保存
- 抓取 Security 文档内容 → 生成笔记预览 → 用户确认保存
- 两篇笔记合并为 `notes/day11-indexing-security.md`

**决策点**: 用户确认笔记格式（Summary/Key Points/Questions/Analogy/Templates/最小实践/关联主题）

### 1.2 实践设计流程

**用户请求**: 完成两篇文档的最小实践

**执行过程**:
- Indexing 实践：选择投票合约 → 设计 event → 设计查询表 → 异常处理策略 → AI Agent 附加字段 → 用户确认保存
- Security 实践：选择 Uniswap V3 swap 交易 → 分析交易详情 → 影响判断 → Simulation/Human Check 设计 → Monitoring 指标 → 用户确认保存

---

## 二、实践设计决策

### 2.1 Indexing 实践：投票合约事件索引

**设计选择**: 选择投票合约而非 NFT/计数器，因为投票场景涉及多事件关联（创建→投票→结束），更适合展示索引设计的复杂性

**关键决策**:
- 查询表分为 `proposals`（聚合状态）和 `votes`（原始记录）两层
- Reorg 处理采用"确认深度阈值 + 删除重建"策略
- AI Agent 附加字段包含 `_source`/`_indexed_at`/`_confirmed` 等来源和时效性标记

### 2.2 Security 实践：交易安全检查表

**设计选择**: 选择 Uniswap V3 swap 交易，因为 DeFi 交互是最常见的 Agent 链上操作场景

**关键决策**:
- Simulation 和 Human Check 分层：自动检查（链ID、地址、滑点、余额）vs 人工确认（金额、价格、策略、时机）
- Agent 权限策略按金额分级：< $1K 自主 / $1K-$10K 需确认 / > $10K 禁止
- Monitoring 必须配合响应流程，设计了"告警→暂停→审查→复盘"闭环

---

## 核心观点总结

| 概念 | 要点 |
|------|------|
| 索引层价值 | 链上数据公开 ≠ 好用，索引层把原始区块流转换为面向业务查询的数据模型 |
| RPC ≠ 数据库 | RPC 适合读当前状态和发交易，复杂历史查询需要独立索引层 |
| 安全 ≠ 审计 | 安全是设计→权限→模拟→监控→应急的全流程工程 |
| AI Agent 安全分层 | model → tool → policy → simulation → human → monitoring，每层独立校验 |
| Simulation 价值 | 签名前最后一道防线，挡住 80% 明显错误（链错、地址错、金额错、滑点过大） |

---

## 文件产出

| 文件 | 用途 |
|------|------|
| `notes/day11-indexing-security.md` | Indexing + Security 两篇学习笔记 |
| `experiments/week2-indexing-event-design.md` | 投票合约事件索引设计实践 |
| `experiments/week2-security-tx-checklist.md` | 交易安全检查表实践 |
| `logs/day11-indexing-security-qa.md` | 本日志文件 |

---

*学习对话记录生成 — 由 Hermes AI（模型：qwen3.6-max-preview）在 2026-05-28 生成*
