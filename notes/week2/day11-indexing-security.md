# Day 11: 索引（Indexing）+ 安全（Security）— Web3 基础学习笔记

**文档来源**: 
- https://aiweb3.school/zh/handbook/web3/indexing/
- https://aiweb3.school/zh/handbook/web3/security/
**生成日期**: 2026-05-28

---

## 目录

1. [索引（Indexing）](#索引indexing)
2. [安全（Security）](#安全security)
3. [🛠️ 最小实践](#🛠️-最小实践)
4. [关联主题](#关联主题)

---

# 索引（Indexing）

## Summary

把链上原始数据整理成产品可快速查询的结构化数据层。

## Key Points

- **Indexing 的本质**：链上数据公开 ≠ 好用，索引层把区块/交易/事件转换成面向业务查询的数据模型
- **第一性原理**：产品关心的是"某地址仓位""协议TVL""订单是否成交"，不是原始区块流；索引层负责做这个转换
- **Event 是核心入口**：合约 event 是索引器构建状态的主要信号，设计 event 时要考虑后续查询需求
- **RPC ≠ 数据库**：RPC 适合读当前状态和发交易，不适合承载复杂历史查询；频繁扫日志会触发限流
- **四种索引方式**：Event Indexing（初级，监听日志）→ Subgraph（中级，声明式+GraphQL）→ RPC（初级，节点接口）→ Data Pipeline（高级，完整数据系统）
- **AI Agent 依赖索引层**：Agent 需要结构化、带来源、带时间戳、可回溯的链上上下文，不能每次从原始区块搜索

## Questions

1. 如果合约升级后 event 结构变了，已有的 subgraph 如何平滑迁移而不丢失历史数据？
2. Data Pipeline 中 reorg 处理的具体策略是什么？多深的 reorg 需要全量重建？
3. AI Agent 使用索引数据时，如何验证数据的时效性和准确性，避免"垃圾进垃圾出"？

## Analogy

**索引层就像图书馆的目录系统**——区块链本身是一堆按时间堆放的书籍（区块），你能找到任何信息但效率极低。索引器就是图书管理员，把书按主题、作者、ISBN 分类编目，让你能一秒查到"某作者的所有作品"或"某主题的最新研究"。没有目录，图书馆只是仓库；没有索引，区块链只是数据坟墓。

## Templates

### Event 设计检查清单
- event 是否包含关键地址？
- 是否需要 indexed 参数？
- 是否能从 event 还原业务状态？
- 失败交易不会产生成功 event
- 合约升级后 event 是否兼容？

### 常见 RPC 问题清单
- rate limit
- 节点不同步
- archive 数据不可用
- 多 RPC 返回不一致
- 查询区块范围过大
- WebSocket 连接不稳定

### Data Pipeline 组件清单
- RPC 或节点数据源
- event listener
- 解码 ABI
- 数据库写入
- reorg 处理
- 数据校验和补偿任务
- API / GraphQL / vector store
- dashboard、alert 和 Agent context

---

# 安全（Security）

## Summary

Web3 安全不是一次审计，而是从设计、权限、模拟、监控到应急响应的完整工程流程。

## Key Points

- **安全 ≠ 审计**：安全是从合约设计→权限→测试→模拟→监控→应急暂停→权限撤销的全流程工程
- **第一性原理**：链上系统默认暴露在公开对抗环境，代码/状态/资金全公开，攻击者可反复模拟和抢跑
- **五大安全节点**：
  - **Reentrancy**（中级）：外部调用未完成前被再次调用，用 Checks-Effects-Interactions 防护
  - **Access Control**（中级）：权限最小化，owner/多签/timelock 边界要清晰
  - **Audit**（中级）：外部审查 ≠ 安全保证书，要看审计范围、修复状态、上线代码是否一致
  - **Simulation**（中级）：交易签名前预演，挡住链ID错、地址错、授权异常、滑点过大等明显错误
  - **Monitoring**（高级）：上线后感知层，关键是"监控 + 响应"闭环
- **AI x Web3 安全**：模型输出和链上执行必须分离——模型建议 → 工具返回事实 → policy 限制 → simulation 预演 → human check 确认 → monitoring 记录

## Questions

1. 如果 Agent 自主生成交易，simulation 和 human check 的边界如何设定？哪些操作必须人工确认？
2. 审计报告中"项目方接受风险"的条目，普通用户如何判断是否可接受？
3. 监控告警触发后，pause 权限应该给谁？多签还是自动化合约？延迟多久算太慢？

## Analogy

**Web3 安全就像金库安保系统**——审计是开业前请专家检查门锁和墙体（但不能保证以后没人挖地道）；Simulation 是每次开门前的"试开"，确认钥匙对得上、门后没有陷阱；Access Control 是分级钥匙系统，保洁员打不开保险柜；Monitoring 是 24 小时摄像头+震动传感器，发现异常自动报警；Reentrancy Guard 是防尾随门，第一道门关上之前第二道门打不开。安全不是"没出事"，而是"出事了能快速止损"。

## Templates

### Reentrancy 防护检查清单
- [ ] 是否遵循 Checks-Effects-Interactions 顺序？
- [ ] 高风险函数是否使用 ReentrancyGuard？
- [ ] 是否在状态更新前调用了不可信合约？
- [ ] 测试是否覆盖多合约交互场景？

### Access Control 审计清单
- [ ] owner 是 EOA、多签还是治理合约？
- [ ] 是否有 timelock？
- [ ] 角色能否相互授予？
- [ ] 权限变更是否发出 event？
- [ ] 紧急暂停和恢复由谁控制？
- [ ] 私钥泄漏时最坏结果是什么？

### 交易 Simulation 检查清单
- [ ] 链 ID 是否正确？
- [ ] 合约地址是否匹配预期？
- [ ] 授权额度是否异常（无限 approve？）？
- [ ] 滑点是否在可接受范围？
- [ ] 余额是否足够？
- [ ] 调用方法是否符合预期？
- [ ] 是否触发权限变更？

### Monitoring 告警清单
- [ ] 大额转账或提款
- [ ] 管理员权限变更
- [ ] 合约升级
- [ ] 预言机价格异常
- [ ] 大量失败交易
- [ ] TVL 快速流出
- [ ] 未预期的 event
- [ ] Agent 连续触发高风险工具

---

## 🛠️ 最小实践

### Indexing 实践：事件索引设计
> 📂 实践输出见：`experiments/week2-indexing-event-design.md`

### Security 实践：交易安全检查表
1. 选择一笔公开的合约调用交易
2. 查看 from、to、method、value、token transfers、logs 和 gas used
3. 判断这笔交易是否改变权限、资产或关键协议参数
4. 写出如果这笔交易由 Agent 发起，执行前要做哪些 simulation 和 human check
5. 写出上线后应该监控哪些 event 或异常指标

> 📂 实践输出见：`experiments/week2-security-tx-checklist.md`

---

## 关联主题

- [Ethereum JSON-RPC API](https://ethereum.org/en/developers/docs/apis/json-rpc/) — 理解读取链状态、查询日志和发送交易的底层接口
- [Ethereum Events and Logs](https://ethereum.org/en/developers/docs/smart-contracts/events/) — 理解后端如何监听链上事件
- [The Graph Subgraphs](https://thegraph.com/docs/en/developing/creating-a-subgraph/) — 学习 subgraph 的 schema、mapping 和查询方式
- [Substreams Documentation](https://substreams.streamingfast.io/) — 了解高吞吐链上数据 pipeline 的另一种方式
- [Dune Docs](https://docs.dune.com/) — 适合用 SQL 分析链上数据和构建 dashboard
- [Solidity Security Considerations](https://docs.soliditylang.org/en/latest/security-considerations.html) — 官方安全注意事项
- [OpenZeppelin Contracts](https://docs.openzeppelin.com/contracts/) — 常用安全组件和标准实现
- [OpenZeppelin Utils](https://docs.openzeppelin.com/contracts/5.x/api/utils) — ReentrancyGuard、Pausable 等工具
- [Ethereum Smart Contract Security](https://ethereum.org/en/developers/docs/smart-contracts/security/) — 以太坊安全实践
- [Tenderly Simulations](https://docs.tenderly.co/simulations-and-forks) — 交易模拟和执行 trace

---

*AI x Web3 School Day 11 课程完成 — 由 Hermes AI（模型：qwen3.6-max-preview）在 2026-05-28 生成*
