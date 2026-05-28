# Week 2 - Indexing 实践：投票合约事件索引设计

**实践日期**: 2026-05-28
**对应笔记**: `notes/day11-indexing.md`

---

## 1. 合约选择：简单投票合约

合约功能：
- 创建投票提案
- 用户对提案投票（赞成/反对）
- 投票结束后统计结果

---

## 2. 合约应发出的 Event

```solidity
// 提案创建
event ProposalCreated(
    uint256 indexed proposalId,
    address indexed creator,
    string title,
    uint256 votingEndsAt
);

// 用户投票
event VoteCast(
    uint256 indexed proposalId,
    address indexed voter,
    bool support,       // true=赞成, false=反对
    uint256 weight      // 投票权重
);

// 投票结束
event VotingEnded(
    uint256 indexed proposalId,
    uint256 forVotes,
    uint256 againstVotes,
    bool passed
);
```

---

## 3. 查询表设计

### 表 1: `proposals`

| 字段 | 类型 | 来源 | 说明 |
|------|------|------|------|
| proposal_id | uint256 | ProposalCreated.proposalId | 提案 ID |
| creator | address | ProposalCreated.creator | 创建者地址 |
| title | string | ProposalCreated.title | 提案标题 |
| voting_ends_at | uint256 | ProposalCreated.votingEndsAt | 投票截止时间戳 |
| for_votes | uint256 | 累加 VoteCast.weight (support=true) | 赞成票总数 |
| against_votes | uint256 | 累加 VoteCast.weight (support=false) | 反对票总数 |
| status | string | 计算得出 | pending/active/ended/passed/failed |
| created_block | uint256 | ProposalCreated 所在区块 | 创建区块号 |
| created_tx_hash | bytes32 | ProposalCreated 所在交易 | 创建交易哈希 |

### 表 2: `votes`

| 字段 | 类型 | 来源 | 说明 |
|------|------|------|------|
| proposal_id | uint256 | VoteCast.proposalId | 提案 ID |
| voter | address | VoteCast.voter | 投票者地址 |
| support | bool | VoteCast.support | 是否赞成 |
| weight | uint256 | VoteCast.weight | 投票权重 |
| block_number | uint256 | VoteCast 所在区块 | 区块号 |
| tx_hash | bytes32 | VoteCast 所在交易 | 交易哈希 |
| tx_index | uint256 | 交易在区块中的索引 | 排序用 |
| log_index | uint256 | event 在交易中的索引 | 排序用 |

---

## 4. 字段来源映射

| 查询表字段 | Event 参数 | 交易/区块字段 |
|-----------|-----------|-------------|
| proposals.proposal_id | ProposalCreated.proposalId | - |
| proposals.creator | ProposalCreated.creator | - |
| proposals.title | ProposalCreated.title | - |
| proposals.voting_ends_at | ProposalCreated.votingEndsAt | - |
| proposals.for_votes | VoteCast.weight (support=true) 累加 | - |
| proposals.against_votes | VoteCast.weight (support=false) 累加 | - |
| proposals.created_block | - | block.number |
| proposals.created_tx_hash | - | tx.hash |
| votes.proposal_id | VoteCast.proposalId | - |
| votes.voter | VoteCast.voter | - |
| votes.support | VoteCast.support | - |
| votes.weight | VoteCast.weight | - |
| votes.block_number | - | block.number |
| votes.tx_hash | - | tx.hash |
| votes.tx_index | - | tx.transactionIndex |
| votes.log_index | - | log.logIndex |

---

## 5. 异常处理策略

### Reorg 处理
- 每条记录保存 `block_number` 和 `block_hash`
- 索引器维护一个"确认深度"阈值（如 12 个区块）
- 当检测到 reorg 时：
  1. 删除 `block_number > reorg_start_block` 的所有记录
  2. 从 `reorg_start_block` 重新扫描日志
  3. 重新构建 proposals 的投票计数

### 重复事件处理
- 使用 `(tx_hash, log_index)` 作为唯一约束
- 写入前检查是否已存在，存在则跳过
- 索引器崩溃重启时，从最后处理的 block_number 继续

### 合约升级处理
- 保存合约地址和版本号到元数据表
- 如果新合约 event 结构兼容（参数相同）：继续索引，记录新地址
- 如果 event 结构不兼容：
  1. 创建新表（如 `votes_v2`）
  2. 旧表标记为只读
  3. API 层合并查询或返回版本标识

---

## 6. AI Agent 使用时的附加字段

如果索引数据要供给 AI Agent 使用，需要额外附加：

| 附加字段 | 类型 | 用途 |
|---------|------|------|
| `_source` | string | 数据来源标识（如 "subgraph:voting:mainnet"） |
| `_indexed_at` | timestamp | 索引器写入时间，判断数据新鲜度 |
| `_block_timestamp` | uint256 | 区块时间戳，Agent 判断事件发生时间 |
| `_confirmed` | bool | 是否超过确认深度，Agent 可据此决定是否信任 |
| `_chain_id` | uint256 | 链 ID，多链场景下区分来源 |

**Agent 使用建议**：
- 查询时优先过滤 `_confirmed = true` 的记录
- 检查 `_indexed_at` 与当前时间差，超过阈值则触发实时 RPC 校验
- 多链场景下用 `_chain_id` 避免跨链数据混淆
- 关键决策前，用 `tx_hash` 回查链上原始数据做二次验证

---

*AI x Web3 School Day 11 实践完成 — 由 Hermes AI（模型：qwen3.6-max-preview）在 2026-05-28 生成*
