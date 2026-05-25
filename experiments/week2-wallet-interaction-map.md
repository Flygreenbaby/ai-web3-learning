# Week 2: 钱包 — 钱包交互地图实践

**文档来源**: https://aiweb3.school/zh/handbook/web3/wallet/
**完成日期**: 2026-05-25

---

## 实践：做一个钱包交互地图

### 使用到的网站

| 用途 | 网址 |
|------|------|
| 测试网 ETH 水龙头（PoW 挖矿） | https://sepolia-faucet.pk910.de/ |
| 去中心化交易所（连接钱包测试） | https://app.uniswap.org/ |
| 区块浏览器（查看交易） | https://sepolia.etherscan.io/ |
| 签名消息观察（密码学实践复用） | https://remix.ethereum.org/ |

### 完整流程记录

| 步骤 | 动作 | 实际操作 | MetaMask 弹窗 |
|------|------|---------|--------------|
| ① 连接钱包 | 连接 Uniswap（Sepolia） | https://app.uniswap.org/ → Connect Wallet | 仅显示「Connect」+ 账户地址——只请求读取地址，无需更多信息 |
| ② 切换网络 | Sepolia ↔ 其他网络 | Uniswap 左上角切网络 | 弹窗确认切换，显示目标链名 |
| ③ 签名消息 | Remix IDE 登录 | https://remix.ethereum.org/ → Sign in with Ethereum | 显示网站域名、地址、链 ID、Nonce、时间戳 |
| ④ 发送交易 | 水龙头 Claim 领币 | https://sepolia-faucet.pk910.de/ → Stop & Claim | ⚠️ 无弹窗！原因见下方「关键发现」 |
| ⑤ 查看 Explorer | Sepolia Etherscan | https://sepolia.etherscan.io/tx/0xf1c4... | 看到 Status/Success、From/To/Value/Gas |

### 关键发现：为什么 Claim 没有 MetaMask 弹窗？

**因为你是收款方，不是付款方。** 水龙头合约自己出 gas、自己发起转账给你。你只是提供了地址等待收款——就像别人给你银行转账，不需要你输密码。MetaMask 弹窗只在「你主动花 gas 改变链上状态」时才出现。

**验证方式**：去区块浏览器查 tx hash：
- Status：✅ Success
- From：`0x6Cc9...`（水龙头合约）
- To：`0x7b10...`（你的钱包）
- Value：0.174 SepETH
- Gas Used：0.0000655 ETH

收钱不需要确认，发钱才需要——这是 Web3 和传统银行一致的地方。

### 只读 vs 改变链上状态

| 动作 | 读/写 | 花 Gas？ | 能撤销？ |
|------|:--:|:--:|:--:|
| ① 连接钱包 | 只读 | ❌ | 随时断开 |
| ② 切换网络 | 只读（本地设置） | ❌ | 随时切回 |
| ③ 签名消息 | 离线授权 | ❌ | 不需要撤销 |
| ④ 发送交易 | **写链上状态** | ✅ | ❌ 永久上链 |
| ⑤ 查看 Explorer | 只读 | ❌ | — |

### MetaMask 弹窗的权限分级设计

| 请求类型 | 弹窗内容 | 风险 |
|----------|---------|:--:|
| `eth_requestAccounts`（连接） | 仅「Connect」+ 账户列表 | 🟢 低——只暴露地址 |
| `eth_sign` / `personal_sign`（签名） | 消息内容、域名、Nonce | 🟡 中——授权身份证明 |
| `eth_sendTransaction`（发交易） | 金额、Gas、合约地址、方法名 | 🔴 高——改变链上资产 |

**连接时越简洁越安全**——如果连接钱包就弹出满屏十六进制让你确认，那才是可疑的。

### 每一步用户应该看到的关键信息

| 步骤 | 关键信息 |
|------|---------|
| 连接钱包 | 哪个网站、请求什么权限（读地址/发起交易）、你的哪个账户 |
| 切换网络 | 目标链名称、链 ID |
| 签名消息 | 签名目的、域名、链 ID、Nonce、具体消息内容 |
| 发送交易 | 接收方地址、金额、Gas 费、合约方法名、资产变化 |
| 查看 Explorer | Status、From/To、Value、Gas Used、Token Transfers |

### AI Agent 辅助时，哪些必须保留人工确认？

| 动作 | AI 能做 | 必须人工确认 | 原因 |
|------|---------|:--:|------|
| 连接钱包 | 建议连哪个 dApp | ✅ | 用户决定暴露哪个地址 |
| 切换网络 | 提示需要切网 | ✅ | 用户知道自己在哪条链 |
| 签名消息 | 解释签名内容 | ✅ | 签名 = 授权，AI 不能代签 |
| 发送交易 | 准备参数、估算 gas | ✅ | 涉及资产转移，不可逆 |
| 查看 Explorer | ✅ AI 全自动 | ❌ | 只读操作，无风险 |

**核心原则：读 → AI 全自动；写 → 人必须确认。**

---

*AI x Web3 School Week 2 钱包 实践完成 — 由 Hermes AI（模型：deepseek-v4-pro）在 2026-05-25 生成*
