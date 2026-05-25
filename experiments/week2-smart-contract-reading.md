# Week 2: 智能合约 — 合约阅读练习实践

**文档来源**: https://aiweb3.school/zh/handbook/web3/smart-contract/
**完成日期**: 2026-05-25

---

## 实践：做一个最小合约阅读练习

### 读的合约

- **合约**: MintableERC20（可铸造 ERC-20 测试代币）
- **链**: Sepolia 测试网
- **源码结构**: 多文件（IERC20.sol 接口 + ERC20.sol 实现 + MintableERC20.sol 扩展）

### 步骤 3：读函数 vs 写函数

| 函数 | 类型 | 说明 |
|------|:--:|------|
| `totalSupply()` | 📖 只读 | 查总发行量 |
| `balanceOf(account)` | 📖 只读 | 查某地址余额 |
| `allowance(owner, spender)` | 📖 只读 | 查授权额度 |
| `nonces(owner)` | 📖 只读 | 查签名计数器 |
| `transfer(to, amount)` | ✏️ 写 | 转账，扣自己余额 |
| `approve(spender, amount)` | ✏️ 写 | 授权别人花你的币 |
| `transferFrom(from, to, amount)` | ✏️ 写 | 用授权额度替别人转账 |
| `permit(owner, spender, value, deadline, v, r, s)` | ✏️ 写 | 离线签名授权（EIP-712） |
| `mint(value)` / `mint(account, value)` | ✏️ 写 | 铸造新币 |

### 步骤 4：权限函数

| 函数 | 有没有 onlyOwner？ | 含义 |
|------|:--:|------|
| `mint()` | ❌ 没有 | 任何人可以无限铸币 |
| `_burn()` | `internal` 内部函数 | 只能合约内部调用，不对外暴露 |
| `_transfer()` | `internal` | 由 `transfer` / `transferFrom` 调用 |
| `pause` | ❌ 不存在 | 没有暂停功能 |
| `upgrade` | ❌ 不存在 | 不可升级合约 |

### 步骤 5：最重要的 Event

| Event | 何时触发 | 对应什么用户动作 |
|-------|---------|----------------|
| **`Transfer(from, to, value)`** | 转账 / 铸币 / 销毁 | `from=0x0` → 铸币；`to=0x0` → 销毁；其他 → 转账 |
| `Approval(owner, spender, value)` | 授权 | 用户批准某个地址花自己的币 |

> 最重要的 event 是 **Transfer**——它一条 event 覆盖三种完全不同的操作（转账/铸币/销毁），通过 `from` 和 `to` 是否为零地址来区分。

### 步骤 6：最重要的风险边界

> **`mint()` 没有任何权限控制，任何人都能无限增发代币——在测试网这是 feature，在主网这是灾难。**

### 🔑 实践中的额外发现

| 遇到的困惑 | 学到的知识 |
|-----------|-----------|
| 第一个合约有 admin + implementation 3 个文件 | 那是**代理合约（Proxy）**——可升级架构，管理员能换掉逻辑 |
| 第二个合约有 8 个 .sol 文件 | 真实项目都是多文件的，看 `IERC20.sol` 找接口，看 `ERC20.sol` 找实现 |
| `mint()` 没有 `onlyOwner` | 链上权限必须**显式声明**，不声明 = 谁都能调 |
| Transfer event 被 mint/burn/transfer 复用 | 一条 event 多个用途，通过参数区分，这是 gas 优化技巧 |

---

*AI x Web3 School Week 2 智能合约 实践完成 — 由 Hermes AI（模型：deepseek-v4-pro）在 2026-05-25 生成*
