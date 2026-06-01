# Day 13: 链感知上下文（Chain-aware Context）— AI × Web3 Bridge 学习笔记

**文档来源**: https://aiweb3.school/zh/handbook/bridge/chain-aware-context/
**生成日期**: 2026-06-01

---

## 目录

1. [Summary](#summary)
2. [Key Points](#key-points)
3. [Questions](#questions)
4. [Analogy](#analogy)
5. [Templates](#templates)
6. [🛠️ 最小实践](#🛠️-最小实践)
7. [关联主题](#关联主题)

---

## Summary

AI 必须从工具层读取链上事实而非凭记忆猜测，每条结论需带可验证来源（citation），否则只是观点。

---

## Key Points

- **链上状态有时间性**：同一地址的余额、授权、仓位随区块变化，Agent 不能把旧数据当当前事实
- **On-chain Data 读取必须带元数据**：chain id + block number + contract address + method + 返回值 + 读取时间，缺了这些字段，模型会把不同链/不同时间的数据混在一起
- **ABI ≠ 业务语义**：ABI 只给函数签名（如 `execute(bytes calldata data)`），Contract Docs 补足"这是普通执行还是高权限入口"，但文档可能过期，必须用链上数据验证（合约地址、版本、owner、proxy implementation、事件、最近交易）
- **Citation 是链上解释的生命线**：没有 tx hash / block number / explorer 链接的链上结论只是观点，带 citation 的解释才能被验证和追责
- **好的链感知上下文包结构** = 用户目标 + chain id/网络名 + 地址余额 + 合约 ABI/文档/风险 + 交易授权记录 + 索引数据更新时间 + 每条结论的 citation

---

## Questions

1. 如果同一合约地址在多条链上部署（如 USDC 在 Ethereum 和 Arbitrum 都有），Chain-aware Context 的 chain id 字段如何防止 Agent 混淆不同链的状态？需要额外做哪些校验？
2. Indexing Context 有同步延迟（"落后 500 个区块的索引结果不应被当成当前事实"），Agent 如何判断索引数据"足够新鲜"？除了落后区块数，还有没有更智能的新鲜度判断方式？
3. 如果 Agent 读取的 Contract Docs 和链上实际行为不一致（如 proxy 升级后文档未更新），Citation 机制如何暴露这个矛盾？Agent 应该"信任文档"还是"信任链上"？

---

## Analogy

链感知上下文就像**医生看病不靠病人自述，而是看实时化验单**。病人说"我好像发烧"是不可靠的——体温计读数 38.5°C（链上数据）+ 血常规报告（交易历史）+ 病历本（Contract Docs）+ 化验单编号可追溯（citation）才是决策依据。AI Agent 没有链感知上下文，就像医生蒙着眼睛开处方。

---

## Templates

### 1️⃣ On-chain Data 读取字段模板
从 RPC / 区块浏览器 / 索引器读取链上数据时，每条记录至少携带：

| 字段 | 说明 |
|------|------|
| `chain_id` | 链标识（1=Ethereum, 137=Polygon, 42161=Arbitrum...） |
| `block_number` | 数据所在区块高度 |
| `contract_address` | 目标合约地址 |
| `method` | 调用的函数或查询方法 |
| `return_value` | 返回值原文（不要提前总结） |
| `read_timestamp` | 读取时间（链上状态会变） |

> ⚠️ 缺少任一字段，模型极易混淆不同链、不同时间、不同合约的数据。

### 2️⃣ 链感知上下文包结构模板
Agent 接收的完整上下文应包含：

| 组成部分 | 内容 |
|----------|------|
| **用户目标** | 用户想做什么（如"把 100 USDC 换成 ETH"） |
| **网络信息** | chain id + 网络名称（如 `1 / Ethereum Mainnet`） |
| **地址 & 余额** | 用户地址 / 合约地址 + 当前余额 |
| **合约信息** | ABI + 文档 + 审计状态 + 风险提示 |
| **交易 & 授权** | 最近交易列表 + allowance 状态 |
| **索引状态** | 所用索引数据的最后同步时间/区块 |
| **Citation** | 每条关键结论附带 tx hash / block / explorer link |

---

## 🛠️ 最小实践

> 📂 实践输出见：`experiments/week3-chain-aware-context-tx-context-package.md`

**任务**：给一笔交易做上下文包

1. 找一笔公开交易哈希（可在 Etherscan 上随便找一笔 Swap / Transfer 交易）。
2. 收集以下字段：chain id、block number、from、to、method、value、token transfers、logs。
3. 找到该合约的 ABI 或 verified source code。
4. 写一段模型可读的上下文描述（英文/中文均可），但每个关键结论都附上交易哈希或 explorer 链接。
5. 标出哪些内容是**链上事实**（标注 `[FACT]`），哪些是你的**解释/推理**（标注 `[INTERPRETATION]`）。

---

## 关联主题

- [智能合约（Smart Contract）](https://aiweb3.school/zh/handbook/web3/smart-contract/) —— 理解 ABI 和 event 在合约交互中的位置
- [索引（Indexing）](https://aiweb3.school/zh/handbook/web3/indexing/) —— event 如何进入索引层成为可查询上下文
- [Web3 工具调用（Web3 Tool Use）](https://aiweb3.school/zh/handbook/bridge/web3-tool-use/) —— 下一篇：有了上下文后 Agent 如何调用链上工具

---

*AI x Web3 School Day 13 课程完成 — 由 Hermes AI（模型：deepseek-v4-pro）在 2026-06-01 生成*
