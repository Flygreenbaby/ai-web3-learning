# Day 8: 密码学 + 钱包 + 智能合约 学习对话记录

**日期**: 2026-05-25
**主题**: Week 2 Day 8 — Web3 基础三篇（密码学、钱包、智能合约）+ 配套实践

---

## 目录

1. [密码学：签名与权限的边界](#一密码学签名与权限的边界)
2. [钱包：连接、签名、交易的三层权限](#二钱包连接签名交易的三层权限)
3. [智能合约：从 Remix 到 Etherscan 源码阅读](#三智能合约从-remix-到-etherscan-源码阅读)
4. [核心观点总结](#核心观点总结)
5. [文件产出](#文件产出)

---

## 一、密码学：签名与权限的边界

### 1.1 Remix IDE 签名观察

**用户问题**: Remix 弹出签名后连接失败，Remix 的作用是什么？

**回答要点**:
- Remix 是完整的 Solidity 开发环境（编写 → 编译 → 部署 → 交互），不只是签名弹窗
- 用户遇到 "registration disabled" 是 Remix 服务器端问题，后来用 GitHub 登录解决了
- 签名登录 ≠ 发交易：签名是离线证明身份，不花 gas，不产生 tx hash

| 项目 | 内容 |
|------|------|
| 结论 | Remix = 浏览器里的合约工厂，签名登录只是进门第一步 |

### 1.2 签名消息 vs 发送交易

**用户问题**: 签名和交易到底差在哪？

**回答要点**:
- 签名消息：离线操作，不花 gas，不产生 tx hash，0 余额也能签
- 发送交易：改变链上状态，需 gas + ETH，产生 tx hash，上链不可逆
- MetaMask 弹窗特征不同：「sign」vs「Send + 金额 + gas」

| 项目 | 内容 |
|------|------|
| 结论 | 签名证明身份，交易转移资产——两种动作风险完全不在一个量级 |

---

## 二、钱包：连接、签名、交易的三层权限

### 2.1 水龙头 Claim 为什么没有 MetaMask 弹窗？

**用户问题**: 点 Stop & Claim 领测试币，MetaMask 没弹窗，为什么？

**回答要点**:
- 水龙头合约自己出 gas、自己转账给你——你是收款方，不是付款方
- MetaMask 弹窗只在「你主动花 gas 改变链上状态」时出现
- 验证方式：去 Sepolia Etherscan 查 tx hash → Status Success、From 是水龙头合约

| 项目 | 内容 |
|------|------|
| 结论 | 收钱不需要确认，发钱才需要——和传统银行逻辑一致 |

### 2.2 连接钱包为什么弹窗那么简洁？

**用户问题**: 连接 Uniswap 时 MetaMask 只显示了 Connect，没有其他信息？

**回答要点**:
- MetaMask 权限分级：eth_requestAccounts（连接=只读地址）→ eth_sign（签名=中等风险）→ eth_sendTransaction（交易=高风险）
- 连接越简洁越安全——如果连接就弹满屏十六进制才可疑

| 项目 | 内容 |
|------|------|
| 结论 | MetaMask 弹窗的复杂度和风险成正比——连接=绿灯，签名=黄灯，交易=红灯 |

---

## 三、智能合约：从 Remix 到 Etherscan 源码阅读

### 3.1 Etherscan 上遇到代理合约

**用户问题**: 点进合约看到 admin + implementation 3 个文件，看不懂

**回答要点**:
- 那是代理合约（Proxy）——用户 → Proxy（固定地址）→ Implementation（可被换掉）
- 对新手不友好，换了一个简单的不可升级合约来读

| 项目 | 内容 |
|------|------|
| 结论 | 看到 contract 页面多个文件 = 可升级架构，管理员能换逻辑 |

### 3.2 MintableERC20 权限分析

**用户问题**: 合约里 `mint()` 没有 `onlyOwner`，这正常吗？

**回答要点**:
- 测试网是 feature（方便任何人铸币测试），主网是灾难（无限增发）
- 链上权限必须显式声明——不声明 = 谁都能调
- Transfer event 被 mint/burn/transfer 三条路径复用，通过 from/to 零地址区分

| 项目 | 内容 |
|------|------|
| 结论 | 读合约不只是看「有什么函数」，更要看「谁有权限调」 |

---

## 核心观点总结

| 概念 | 要点 |
|------|------|
| 签名 vs 交易 | 签名=证明身份（离线免费），交易=改变链状态（需 gas 不可逆） |
| 收款 vs 付款 | 收钱不需要 MetaMask 确认，发钱才弹窗 |
| MetaMask 权限分级 | 连接=绿灯（只读地址），签名=黄灯（授权），交易=红灯（花钱） |
| 代理合约 | admin + implementation = 可升级，管理员能换逻辑 |
| 合约权限 | 不显式声明 onlyOwner = 任何人可调——在测试网是 feature，在主网是灾难 |

---

## 文件产出

| 文件 | 用途 |
|------|------|
| notes/week2/day8-cryptography.md | 密码学学习笔记 |
| notes/week2/day8-wallet.md | 钱包学习笔记 |
| notes/week2/day8-smart-contract.md | 智能合约学习笔记 |
| experiments/week2-cryptography-signature-practice.md | 密码学：签名观察实践 |
| experiments/week2-wallet-interaction-map.md | 钱包：交互地图实践 |
| experiments/week2-smart-contract-reading.md | 智能合约：合约阅读实践 |

---

*学习对话记录生成 — 由 Hermes AI（模型：deepseek-v4-pro）在 2026-05-25 生成*
