# Day 10 实践：价格 Feed 风险检查 + AI Oracle 场景设计

**关联笔记**: `notes/week2/day10-oracle.md`
**完成日期**: 2026-05-27

---

## Part A：Price Feed 风险检查

### 1. 找到链上的 ETH/USD Price Feed

| 项目 | 内容 |
|------|------|
| 网络 | Ethereum Mainnet |
| Feed | ETH / USD |
| 合约地址 | `0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419` |
| 提供方 | Chainlink |
| Decimals | 8 |
| 验证来源 | https://docs.chain.link/data-feeds/price-feeds/addresses#ethereum-mainnet |

### 2. 查看最新价格和更新时间

通过 Chainlink Data Feeds 页面（https://data.chain.link/）查看：

| 项目 | 值 |
|------|------|
| 最新价格 | ~$2,680.45（示例值，实际需实时查询） |
| 最后更新 | 几秒~几分钟前（持续更新） |
| 心跳间隔 | 3,600 秒（1 小时） |
| 偏差阈值 | 0.5%（价格变化超过 0.5% 立即触发更新） |
| 数据源节点 | 21+ 个独立 Chainlink 节点 |

> 更新机制：Chainlink 采用 heartbeat + deviation threshold 双触发机制。正常情况下每小时至少更新一次，价格波动超过 0.5% 时立即更新。

### 3. 如果价格延迟 30 分钟，哪些协议动作受影响？

| 受影响动作 | 影响程度 | 说明 |
|------------|:--------:|------|
| 借贷清算 | 🔴 高 | 抵押品价格过时 → 可能错误清算用户仓位，或漏清算导致坏账 |
| 杠杆开仓 | 🔴 高 | 用旧价格开仓 → 用户可能以不利价格建仓，协议承担坏账风险 |
| 稳定币铸币 | 🟡 中 | 抵押率计算偏差 → 可能超额铸币，影响稳定币锚定 |
| 衍生品结算 | 🔴 高 | 结算价格不准 → 一方不当获利，另一方损失 |
| 普通 swap | 🟢 低 | AMM 用池子状态定价（x*y=k），不直接依赖 oracle |
| 限价单触发 | 🟡 中 | 价格延迟可能导致限价单在错误时机触发 |

**攻击场景示例**：
- ETH 实际价格从 $2,700 暴跌到 $2,500
- Oracle 价格仍显示 $2,700（延迟 30 分钟）
- 攻击者用 $2,500 的实际价值抵押品，按 $2,700 的价格借出资产
- 30 分钟后 Oracle 更新，攻击者的仓位被清算，但协议已经产生坏账

### 4. 合约读取 Feed 时应该检查的条件

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

contract SafePriceReader {

    /// @notice 安全读取 Chainlink Price Feed
    /// @param feed Price Feed 合约地址
    /// @param maxDelay 最大允许延迟（秒）
    /// @return price 价格（已考虑 decimals）
    function getPrice(
        address feed,
        uint256 maxDelay
    ) internal view returns (uint256 price) {

        // 获取最新轮次数据
        (
            uint80 roundId,
            int256 answer,
            ,
            uint256 updatedAt,
            uint80 answeredInRound
        ) = AggregatorV3Interface(feed).latestRoundData();

        // 检查 1：价格必须为正数
        require(answer > 0, "Oracle: invalid price");

        // 检查 2：数据不能过旧
        require(
            block.timestamp - updatedAt <= maxDelay,
            "Oracle: stale price"
        );

        // 检查 3：本轮必须已完成回答（防止使用过时轮次数据）
        require(
            answeredInRound >= roundId,
            "Oracle: incomplete round"
        );

        // 检查 4：roundId 不能为 0（异常情况）
        require(roundId > 0, "Oracle: invalid round");

        return uint256(answer);
    }

    /// @notice 获取价格并转换为标准精度（18 decimals）
    function getNormalizedPrice(
        address feed,
        uint256 maxDelay
    ) external view returns (uint256) {

        uint256 price = getPrice(feed, maxDelay);
        uint8 feedDecimals = AggregatorV3Interface(feed).decimals();

        // 统一到 18 decimals
        if (feedDecimals < 18) {
            return price * (10 ** (18 - feedDecimals));
        } else if (feedDecimals > 18) {
            return price / (10 ** (feedDecimals - 18));
        }
        return price;
    }
}
```

**关键检查项总结**：

| 检查项 | 条件 | 失败后果 |
|--------|------|----------|
| `price > 0` | 价格为正 | 负价格或零值导致计算错误 |
| `block.timestamp - updatedAt <= maxDelay` | 数据新鲜 | 旧价格被使用 → 错误清算/套利 |
| `answeredInRound >= roundId` | 轮次完整 | 使用过时轮次数据 |
| `roundId > 0` | 轮次有效 | 异常情况（如 feed 刚部署） |

**推荐的 maxDelay 值**：
- 借贷协议：600 秒（10 分钟）— 保守，防止清算风险
- 衍生品：300 秒（5 分钟）— 更保守，结算价格必须准确
- 一般用途：3,600 秒（1 小时）— 匹配 Chainlink heartbeat

---

## Part B：AI Oracle 输出场景设计

### 场景：AI Agent 评估 DeFi 协议风险等级

**用途**：为保险协议、借贷协议、投资组合 Agent 提供协议风险评级

### 1. 输入数据（必须记录）

```
输入数据清单：
├── 协议合约地址：0x1234...5678
├── 合约源码哈希：0xAbCd...（IPFS CID 或 Keccak256）
├── 近 30 天链上交易数据：
│   ├── 交易笔数：12,345
│   ├── 总交易量：$45.6M
│   └── 数据来源：Dune Analytics Query #123456
├── TVL 变化趋势：
│   ├── 30 天前：$12.5M
│   ├── 当前：$8.7M（-30.4%）
│   └── 数据来源：DefiLlama API
├── 审计记录：
│   ├── 是否有审计：是
│   ├── 审计机构：CertiK
│   └── 审计报告哈希：0x7890...
├── 团队信息：
│   ├── 是否 KYC：否（匿名团队）
│   └── 链上活动历史：6 个月
└── 输入数据总哈希：0xFeed...（用于链上验证输入完整性）
```

### 2. 模型信息（必须记录）

```
模型信息：
├── 模型名称：risk-assessor
├── 模型版本：v2.1.0
├── 模型权重哈希：0xModel...（确保可复现）
├── Prompt 模板版本：prompt-risk-v3.2
├── Prompt 完整内容哈希：0xPrompt...
├── 推理引擎：llama.cpp / vLLM
├── 推理时间：2026-05-27T12:00:00Z
└── 推理耗时：4.2 秒
```

### 3. 输出结果

```
AI Oracle 输出：
├── 风险等级：中（Medium）
├── 置信度：78%
├── 关键风险因素：
│   ├── [高] 团队匿名 — 无法追溯责任
│   ├── [中] TVL 下降 30% — 用户信心流失
│   └── [低] 审计报告已过时（6 个月前）
├── 建议动作：
│   ├── 保险协议：提高保费 15%
│   ├── 借贷协议：降低该协议代币抵押系数至 60%
│   └── 投资 Agent：将该协议配置上限降至 5%
└── 输出哈希：0xOutput...
```

### 4. 争议流程

```
争议机制设计：
├── 挑战期：72 小时（259,200 秒）
│
├── 挑战条件：
│   ├── 任何人都可以发起挑战
│   ├── 必须提交替代风险评估 + 押金 100 USDC
│   └── 替代评估必须使用相同输入数据（验证输入哈希）
│
├── 仲裁流程：
│   ├── 仲裁者：3 位注册的风险评估专家
│   ├── 投票方式：2/3 多数决
│   ├── 投票期限：48 小时
│   └── 仲裁费：从挑战押金中扣除
│
├── 挑战成功（仲裁者支持挑战）：
│   ├── 退还挑战者押金 + 奖励 50 USDC
│   ├── 原评估结果被覆盖
│   ├── 原提交者质押金被罚没 10%
│   └── 触发受影响协议的参数更新
│
└── 挑战失败（仲裁者驳回挑战）：
    ├── 挑战者押金归入仲裁基金
    ├── 原评估结果维持不变
    └── 挑战者获得"无效挑战"记录
```

### 5. 链上后果

```
如果 AI Oracle 结果被接受（挑战期结束无挑战 或 挑战失败）：

保险协议：
├── 读取风险等级：Medium
├── 执行动作：调整该协议的保险费率
├── 合约调用：InsurancePool.setPremium(protocol, newRate)
└── 事件：PremiumUpdated(protocol, oldRate, newRate)

借贷协议：
├── 读取风险等级：Medium
├── 执行动作：调整该协议代币的抵押系数
├── 合约调用：LendingPool.setCollateralFactor(token, 60%)
└── 事件：CollateralFactorUpdated(token, 75%, 60%)

投资组合 Agent：
├── 读取风险等级：Medium + 建议动作
├── 执行动作：重新平衡投资组合
├── 操作：卖出该协议代币至 ≤5% 配置
└── 审计日志：记录再平衡交易哈希
```

### 6. 完整的链上数据结构

```solidity
struct AIOracleOutput {
    bytes32 inputHash;        // 输入数据哈希
    bytes32 modelHash;        // 模型版本哈希
    bytes32 promptHash;       // Prompt 哈希
    bytes32 outputHash;       // 输出结果哈希
    uint8 riskLevel;          // 0=Low, 1=Medium, 2=High, 3=Critical
    uint8 confidence;         // 0-100%
    uint256 timestamp;        // 提交时间
    address submitter;        // 提交节点地址
    uint256 challengeEnd;     // 挑战期结束时间
    bool finalized;           // 是否已最终确认
}

struct Challenge {
    address challenger;       // 挑战者地址
    bytes32 alternativeHash;  // 替代评估哈希
    uint256 deposit;          // 押金金额
    uint8 votesFor;           // 支持挑战的票数
    uint8 votesAgainst;       // 反对挑战的票数
    bool resolved;            // 是否已解决
}
```

---

## 学习总结

### 关键收获

1. **Price Feed 不是"读一个数字"这么简单**：必须检查新鲜度、有效性、精度，还要有 fallback 机制
2. **延迟是最大的系统性风险**：30 分钟的价格延迟在极端行情下可以造成数百万美元损失
3. **AI Oracle 需要完整的审计链**：输入、模型、Prompt、输出全部要记录哈希，才能做到可验证、可争议
4. **争议机制是 AI Oracle 的安全网**：没有争议机制的 AI Oracle 就是"AI 说了算"，这不可接受

### 下一步探索

- [ ] 在 Sepolia 上实际部署一个读取 Chainlink Price Feed 的合约
- [ ] 研究 UMA Optimistic Oracle 的挑战机制实现
- [ ] 对比 Chainlink vs Pyth 的更新速度和成本

---

*AI x Web3 School Day 10 实践完成 — 由 Hermes AI（模型：qwen3.7-max）在 2026-05-27 生成*
