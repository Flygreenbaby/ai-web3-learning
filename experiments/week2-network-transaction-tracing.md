# Day 9: Network 实践 — 测试网交易追踪

**日期**: 2026-05-26

---

## 实践目标

在 Sepolia 测试网做一笔交易，追踪从 pending 到 confirmed 的全过程，理解多链隔离。

---

## 操作步骤

### 1. 领取测试币

- 使用 **pk910 水龙头**：https://sepolia-faucet.pk910.de/
- 粘贴钱包地址：`0x7b108a7727Dc59138d6E5b996817e163EB471746`
- 点击 **Start Mining**，浏览器算力挖矿
- 挖到约 0.05 ETH 后点击 **Stop Mining** → **Claim**
- MetaMask 切换到 Sepolia 网络，确认余额增加

### 2. 发送交易

- MetaMask 确保在 **Sepolia** 网络
- 点击 **Send**
- 收款地址填自己：`0x7b108a7727Dc59138d6E5b996817e163EB471746`
- 金额：`0.001` ETH
- 点击 **Next** → **Confirm**
- 等待交易确认（约 10-15 秒）

### 3. 在 Etherscan 追踪

- 打开 **Sepolia Etherscan**：https://sepolia.etherscan.io/
- 搜索钱包地址
- 找到最新交易，点击 Txn Hash

**交易详情**：

| 字段 | 值 |
|------|------|
| Transaction Hash | `0x6e1ea5205c33f1f188b2ab0737d6690da7bab83d484bbeb9cbe69ca6c7e0fcb8` |
| Status | Success |
| Block | 10924975 |
| Block Confirmations | 9 |
| From | `0x7b108a7727Dc59138d6E5b996817e163EB471746` |
| To | `0x7b108a7727Dc59138d6E5b996817e163EB471746` |
| Value | 0.001 ETH |
| Transaction Fee | 0.000100635876222 ETH |
| Gas Price | 4.792184582 Gwei |

### 4. 切换网络对比

- MetaMask 切换到 **Ethereum Mainnet**
- 打开 **Etherscan Mainnet**：https://etherscan.io/
- 搜索同一地址：`0x7b108a7727Dc59138d6E5b996817e163EB471746`
- **结果**：余额为 0，无任何交易记录

---

## 关键发现

### 1. 多链隔离

同一地址在不同链上状态完全独立：
- Sepolia：有余额，有交易记录
- Mainnet：余额 0，无记录

**结论**：区块链是独立的账本，地址可以存在于多条链上，但每条链的状态互不影响。

### 2. Gas 机制

- **Gas Fee = Gas Used × Gas Price**
- 本次交易 Gas Fee：0.0001 ETH（约 $0.25）
- Gas Price：4.79 Gwei（Sepolia 测试网极低）
- 主网 Gas Price 通常 20-100 Gwei，L2 更低

### 3. 区块确认

- 交易被打包进区块后，还需等待后续区块确认
- Sepolia 上 12 个确认足够安全
- 本次交易已有 9 个确认，即将达到安全阈值

### 4. AI Agent 必须读取的字段

| 字段 | 必须由工具读取 | 原因 |
|------|:--:|------|
| chain_id | ✅ | 不知道网络就读错链 |
| block_number | ✅ | 模型无法凭空知道 |
| confirmations | ✅ | 实时变化 |
| gas_fee | ✅ | 实际支付的金额 |
| tx_hash | ✅ | 交易的唯一标识 |
| 交易含义解释 | ❌ | 模型可以生成 |
| 风险评估 | ❌ | 模型可以推理 |

---

## 收获

- 理解了多链隔离的核心概念
- 掌握了 Gas Fee 的计算方式
- 知道了区块确认的意义
- 明确了 AI Agent 操作链上时必须感知 chain id

---

*AI x Web3 School Day 9 实践完成 — 由 Hermes AI（模型：阿里百炼免费模型）在 2026-05-26 生成*
