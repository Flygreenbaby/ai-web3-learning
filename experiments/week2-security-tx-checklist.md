# Week 2 - Security 实践：交易安全检查表

**实践日期**: 2026-05-28
**对应笔记**: `notes/day11-indexing-security.md`

---

## 1. 选择的交易

**交易哈希**: `0x2d5c3a8e7b1f9c4a6e8b3d2f1a0c9e7b6d5f4a3c2b1a0e9d8c7b6a5f4e3d2c1b0`（示例交易）
**网络**: Ethereum Mainnet
**协议**: Uniswap V3 Router 2
**区块**: 19,876,543

---

## 2. 交易详情分析

| 字段 | 值 | 说明 |
|------|-----|------|
| **from** | `0x1234...5678` | 用户 EOA 地址 |
| **to** | `0x68b3...89ab` | Uniswap V3: Swap Router 2（合约） |
| **method** | `exactInputSingle` | 精确输入换币 |
| **value** | 0 ETH | 不涉及 ETH 转账 |
| **tokenIn** | USDC (`0xa0b8...`) | 输入代币 |
| **tokenOut** | WETH (`0xc02a...`) | 输出代币 |
| **amountIn** | 10,000 USDC | 输入金额 |
| **amountOutMinimum** | 3.15 WETH | 最小输出（含滑点保护） |
| **fee** | 3000 | 手续费层级 0.3% |
| **deadline** | 1717200000 | 交易过期时间戳 |
| **gas used** | 185,432 | 实际消耗 gas |
| **gas price** | 25 gwei | gas 价格 |

### Token Transfers（日志解析）

| 方向 | 代币 | 金额 | 地址 |
|------|------|------|------|
| from → Router | USDC | 10,000 | 用户授权转账 |
| Pool → from | WETH | 3.182 | 实际输出 |

### Logs 关键 Event

1. `Transfer(address from, address to, uint256 value)` — USDC 从用户转到 Router
2. `Swap(address sender, address recipient, int256 amount0, int256 amount1, uint160 sqrtPriceX96, uint128 liquidity, int24 tick)` — 池子执行 swap
3. `Transfer(address from, address to, uint256 value)` — WETH 从池子转回用户

---

## 3. 交易影响判断

| 维度 | 是否改变 | 说明 |
|------|---------|------|
| **权限** | ❌ 否 | 不涉及 owner/admin 变更 |
| **资产** | ✅ 是 | 用户失去 10,000 USDC，获得 3.182 WETH |
| **协议参数** | ❌ 否 | 不修改 fee、oracle 等参数 |
| **合约状态** | ✅ 是 | 池子流动性、价格 tick 微调 |

**风险等级**: 🟡 中等 — 涉及资产转移但不涉及权限变更

---

## 4. Agent 发起此交易前的 Simulation & Human Check

### Simulation 检查项（自动执行）

```
✅ 链 ID 验证：确认是 Ethereum Mainnet (chainId=1)
✅ 合约地址验证：to 地址是已知的 Uniswap V3 Router 2
✅ 方法签名验证：exactInputSingle 符合预期 swap 操作
✅ 授权额度检查：USDC allowance ≥ 10,000（非无限 approve）
✅ 滑点检查：(10000/3.15 - 10000/3.182) / (10000/3.15) ≈ 1% < 设定阈值 2%
✅ 余额检查：USDC balance ≥ 10,000
✅ 过期时间检查：deadline > block.timestamp + 5min
✅ 预演结果：模拟返回 amountOut ≈ 3.18 WETH，与预期一致
✅ 资产变化：-10,000 USDC, +3.18 WETH（符合预期）
```

### Human Check 检查项（需人工确认）

```
⚠️ 金额确认：10,000 USDC 是大额交易，需人工确认金额无误
⚠️ 价格确认：当前 USDC/WETH 价格是否在合理范围？（对比 CEX 价格）
⚠️ 策略确认：此 swap 是否符合当前投资策略？（是否应该分批执行？）
⚠️ 时机确认：当前 gas price 25 gwei 是否合适？是否需要等低峰期？
```

### Agent 权限策略建议

| 操作类型 | Agent 自主执行 | 需 Human Check |
|---------|--------------|----------------|
| swap < $1,000 | ✅ 允许 | - |
| swap $1,000-$10,000 | ⚠️ 需确认金额 | ✅ 必须 |
| swap > $10,000 | ❌ 禁止 | ✅ 必须 + 二次确认 |
| approve 无限额度 | ❌ 禁止 | - |
| approve 有限额度 | ✅ 允许（≤ 交易额 110%） | - |

---

## 5. 上线后 Monitoring 指标

### 实时监控 Event

| Event | 监控条件 | 告警级别 |
|-------|---------|---------|
| `Swap` | 单笔 swap 金额 > $50,000 | 🟡 Warning |
| `Swap` | 1 分钟内连续 swap > 5 次 | 🟠 Alert |
| `Swap` | 滑点 > 3% | 🔴 Critical |
| `Transfer` | Router 向非预期地址转出 token | 🔴 Critical |
| 任意 | 交易 revert 率 > 10%（1h 窗口） | 🟡 Warning |

### 异常指标监控

| 指标 | 阈值 | 响应动作 |
|------|------|---------|
| Agent 连续触发 swap | > 3 次/10min | 暂停 Agent，人工审查 |
| 协议 TVL 变化 | > 5%/1h | 检查是否有 exploit |
| 预言机价格偏差 | > 2% vs CEX | 暂停依赖该 oracle 的操作 |
| gas price 异常 | > 100 gwei | 延迟非紧急交易 |
| 合约升级事件 | 任意 | 立即审查 diff，确认来源 |

### 应急响应流程

```
1. 监控告警触发
2. 自动暂停 Agent 交易权限（Pausable）
3. 发送告警到 Telegram/Discord（含交易 hash、资产变化）
4. 人工审查：
   - 如果是误报 → 恢复 Agent 权限
   - 如果是异常 → 保持暂停，调查根因
   - 如果是攻击 → 执行紧急提款/冻结流程
5. 事后复盘：更新 simulation 规则和监控阈值
```

---

## 6. 实践总结

### 关键收获

1. **Simulation 是最后一道防线**：能在签名前挡住 80% 的明显错误（链错、地址错、金额错、滑点过大）
2. **Human Check 不是万能的**：人会疲劳、会误判，所以要用 policy 限制 Agent 权限，而不是全靠人工审核
3. **Monitoring 必须配合响应**：只监控不响应 = 没监控，关键是"谁能 pause、多久能响应"
4. **AI Agent 安全是分层的**：model → tool → policy → simulation → human → monitoring，每层独立校验

### AI x Web3 安全设计原则

```
模型可以建议，但不能直接执行。
工具返回事实，但不能自主决策。
Policy 限制权限，但不能完全信任。
Simulation 预演结果，但不能替代审计。
Human 确认高风险动作，但不能成为瓶颈。
Monitoring 记录后果，但不能只记不响应。
```

---

*AI x Web3 School Day 11 实践完成 — 由 Hermes AI（模型：qwen3.6-max-preview）在 2026-05-28 生成*
