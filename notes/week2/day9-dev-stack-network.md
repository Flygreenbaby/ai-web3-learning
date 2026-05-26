# Day 9: 开发栈（Dev Stack）+ 网络（Network）— Web3 基础学习笔记

**生成日期**: 2026-05-26

---

## 目录

1. [开发栈（Dev Stack）](#开发栈dev-stack)
2. [网络（Network）](#网络network)
3. [🛠️ 最小实践汇总](#🛠️-最小实践汇总)
4. [📊 各章节生成信息](#-各章节生成信息)

---

## 开发栈（Dev Stack）

**文档来源**: https://aiweb3.school/zh/handbook/web3/dev-stack/

### Summary

Web3 开发栈是一条"写→编译→部署→测试→前端调用→链上验证"的工程链路，目标是让不可逆的链上操作变得可测试、可复现、可审查。

### Key Points

- **六步最小开发链路**：写合约 → 编译得 bytecode/ABI → 本地/测试网部署 → 写测试覆盖状态变化和权限 → 前端用 ABI+地址读写 → 区块浏览器验证源码
- **Remix = 合约实验台**：浏览器 IDE，适合快速原型和教学，但不适合多人协作 — 正式项目应迁入 Hardhat/Foundry + Git
- **Hardhat = JS/TS 合约工程框架**：contracts/ + test/ + scripts/ + hardhat.config.ts + artifacts/，和前端/CI 结合自然
- **Foundry = Solidity-native 命令行工具链**：forge test/build、anvil 本地链、cast call/send，适合测试驱动开发和安全审计
- **前端四类状态必须分开**：钱包连接状态、当前链、合约读取加载/过期、写交易的五步生命周期（等待签名→已广播→等待确认→成功/失败）
- **OpenZeppelin ≠ 免审计**：库降低基础风险，但权限组合、升级模式、参数设置仍需自己验证
- **AI 参与开发栈后验证要更明确**：Agent 运行 forge test/cast/部署脚本时，必须受 repo workflow、测试、权限、secret 管理约束

### Questions

1. Hardhat 和 Foundry 都支持本地链部署和测试，但一个偏向 JS/TS 生态、一个偏向 Solidity-native，什么场景下必须二选一，什么场景下可以互补？
2. 前端合约调用的四个状态（连接/链/读取/写交易）如果混在一个按钮里，用户会遇到哪些具体困惑？可以画一个状态机吗？
3. 如果 AI Agent 能跑 `forge test` 和 `cast send`，哪些命令应该设为"需人工确认"？用什么机制来拦截？

### Analogy

Web3 开发栈就像**火箭发射前的倒计时检查清单**。链上部署等于点火 — 一旦发射就无法撤回。所以需要先在模拟器（本地链）里测试、写自动化检查脚本（测试）、确认每个零件版本号（合约地址+ABI 版本化）、监控飞行数据（event/交易状态）。如果跳过检查清单直接点火，出了问题只能在太空中修，成本是地面的百倍。

### Templates

#### 1️⃣ 六步最小开发链路

```
① 本地/浏览器 IDE 写合约
② 编译 → bytecode + ABI
③ 本地链/测试网部署
④ 写测试覆盖核心状态变化 + 权限边界
⑤ 前端用合约地址 + ABI 读/写
⑥ 区块浏览器验证源码 + 交易 + event
```

#### 2️⃣ Hardhat 标准项目结构

```
contracts/        → Solidity 合约源码
test/             → TypeScript/Solidity 测试
ignition/ 或 scripts/  → 部署模块和脚本
hardhat.config.ts → 网络、编译器、插件、变量配置
artifacts/        → 编译生成的 ABI、bytecode、metadata
```

#### 3️⃣ Foundry 常用命令

```
forge test   → 运行合约测试
forge build  → 编译合约
anvil        → 启动本地测试链
cast call    → 读取链上合约
cast send    → 发送交易调用合约
```

#### 4️⃣ 前端四类状态分离

| 状态类别 | 关键问题 |
|---------|---------|
| 钱包连接 | 已连接？哪个账户？ |
| 当前链 | 用户在 mainnet/testnet/其他？ |
| 合约读取 | 加载中？已过期？ |
| 写交易 | 等待签名→已广播→等待确认→成功→失败 |

#### 5️⃣ 投票合约完整工具链示例

```
Remix 写 Voting.sol 原型
→ 迁入 Hardhat/Foundry repo
→ 写测试：创建投票、重复投票、投票结束、权限失败
→ 本地链部署，记录地址+ABI
→ viem/wagmi 前端：读取候选项、发起投票、展示 pending/confirmed
→ 测试网部署 + 区块浏览器验证源码 + 检查 event
```

### 关联主题

- [智能合约（Smart Contract）](https://aiweb3.school/zh/handbook/web3/smart-contract/) — 理解合约 ABI、event、升级风险
- [Remix Documentation](https://remix-ide.readthedocs.io/) — 浏览器 IDE 入门
- [Hardhat Documentation](https://hardhat.org/docs) — TypeScript 合约开发流程
- [Foundry Book](https://book.getfoundry.sh/) — Solidity-native 测试工具链
- [OpenZeppelin Contracts](https://docs.openzeppelin.com/contracts/) — 合约标准库
- [viem Documentation](https://viem.sh/) — TypeScript 链交互库
- [wagmi Documentation](https://wagmi.sh/) — React 钱包+合约 hooks

---

## 网络（Network）

**文档来源**: https://aiweb3.school/zh/handbook/web3/network/

### Summary

Web3 网络是交易打包、状态同步、费用产生和确认的基础环境，不是抽象背景。

### Key Points

- **Block（区块）= 批量排序单位**：交易按区块批量提交，有 gas limit（吞吐非无限），新区块引用前一区块形成可验证历史链
- **Consensus（共识）= 信任来源**：网络决定"哪段历史有效"的机制，影响确认数、区块重组风险和状态读取延迟
- **PoS（权益证明）**：用质押+惩罚机制组织验证者，替代 PoW 挖矿；验证者质押 ETH 参与提议和证明，行为错误被罚没
- **Testnet（测试网）**：接近真实链的测试环境，资产无经济价值；但测试网不能完全替代主网安全审查
- **L2 + Rollup = 扩展路线**：把大量交易放到主网外执行，再把结果/证明提交回主网；主流路线分 optimistic rollup 和 ZK rollup
- **AI Agent 必须感知网络**：读取链上状态或执行交易时，工具必须返回结构化网络信息——chain id、RPC 来源、区块高度、交易哈希、确认数、explorer 链接

### Questions

1. Optimistic Rollup 和 ZK Rollup 在安全性和最终确认延迟上有什么本质区别？各自适合什么场景？
2. 如果 AI Agent 同时在多条链上操作，如何管理不同网络的 RPC 延迟、确认时间和 gas 差异？
3. 测试网不能模拟主网的哪些真实场景（如 MEV、拥堵、重组）？安全审计时如何弥补这个差距？

### Analogy

Web3 网络就像**不同城市的交通系统**——主网是高铁（贵但安全可靠），测试网是模拟驾驶舱（免费练习但路况简化），L2 是城市地铁（便宜快速但最终要换乘回高铁站结算）。同一张身份证（钱包地址）可以在所有城市使用，但每个城市的余额、票价和到站时间完全独立。

### Templates

#### 1️⃣ AI Agent 网络信息结构

```
每次链上操作返回：
- chain_id: 网络标识（1=Mainnet, 11155111=Sepolia）
- rpc_url: 数据来源
- block_number: 当前区块高度
- tx_hash: 交易哈希
- confirmations: 确认数
- explorer_url: 区块浏览器链接
```

#### 2️⃣ 交易生命周期

```
钱包签名 → 广播到 mempool → 矿工/验证者打包 → 区块确认 → 状态更新
  (pending)    (pending)        (included)      (confirmed)   (final)
```

#### 3️⃣ 网络对比

| 属性 | Mainnet | Testnet (Sepolia) | L2 (如 Arbitrum) |
|------|---------|-------------------|-------------------|
| 资产价值 | 真实 | 无 | 真实 |
| Gas 费用 | 高 | 极低/免费 | 低 |
| 确认时间 | ~12s | ~12s | ~1s |
| 安全等级 | 最高 | 低 | 继承主网 |
| 用途 | 生产环境 | 开发测试 | 低成本生产 |

#### 4️⃣ 区块三要素

```
① 交易有顺序 — 顺序影响执行结果
② 区块有 gas limit — 吞吐非无限
③ 新区块引用前一区块 — 形成可验证历史链
```

### 关联主题

- [区块（Ethereum Blocks）](https://ethereum.org/developers/docs/blocks/) — 区块结构和排序机制
- [网络（Networks）](https://ethereum.org/developers/docs/networks/) — 以太坊主网与测试网
- [权益证明（Proof-of-Stake）](https://ethereum.org/developers/docs/consensus-mechanisms/pos/) — PoS 共识机制
- [Layer 2](https://ethereum.org/developers/docs/scaling/) — L2 扩展方案总览
- [Rollups](https://ethereum.org/developers/docs/scaling/#rollups) — Optimistic vs ZK Rollup

---

## 🛠️ 最小实践汇总

**开发栈（Dev Stack）**

搭一个最小 Web3 开发链路：

1. 用 Remix 部署一个极简计数器合约，包含 `count()`、`increment()` 和 `CountChanged` event
2. 用 Hardhat 或 Foundry 建一个本地工程，并写测试覆盖初始值和 `increment()` 后的状态变化
3. 记录合约地址、ABI、部署网络、部署账号和交易哈希
4. 用 viem 或 wagmi 从前端读取 `count()`，再发起一次 `increment()` 交易
5. 在区块浏览器或本地日志里确认 event 被正确发出
6. 写下这条链路中哪些信息必须进版本控制，哪些必须放在 `.env` 或密钥管理里

> 📂 Demo 地址：[待补充]()

**网络（Network）**

做一笔测试网交易追踪：

1. 在 Sepolia 水龙头领取测试 ETH（使用 pk910.de 水龙头，通过浏览器算力挖矿领取）
2. 用 MetaMask 给自己发一笔 0.001 ETH 交易
3. 在 Sepolia Etherscan 追踪交易，记录以下字段：
   - Transaction Hash: `0x6e1ea5205c33f1f188b2ab0737d6690da7bab83d484bbeb9cbe69ca6c7e0fcb8`
   - Status: Success
   - Block: 10924975（9 Block Confirmations）
   - Gas Fee: 0.000100635876222 ETH
   - Gas Price: 4.792184582 Gwei
4. 切换到 Ethereum Mainnet，发现同一地址余额为 0、无交易记录 → 验证多链隔离
5. 思考：AI Agent 必须由工具读取的字段（chain id、block、confirmations、gas），vs 模型可生成的描述（交易含义解释、风险评估）

> 📂 Demo 地址：[待补充]()

---

## 📊 各章节生成信息

| 章节 | 模型 | 生成时间 |
|------|------|----------|
| 开发栈（Dev Stack） | 阿里百炼免费模型 | 2026-05-26 |
| 网络（Network） | 阿里百炼免费模型 | 2026-05-26 |

---

*AI x Web3 School Day 9 课程完成 — 由 Hermes AI（模型：阿里百炼免费模型）在 2026-05-26 生成*
