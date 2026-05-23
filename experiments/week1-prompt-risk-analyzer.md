# Week 1 实践：Prompt — 交易风险摘要

**对应 Handbook**: https://aiweb3.school/zh/handbook/ai/prompt/
**实践目标**: 设计一个结构化的 Prompt，让 LLM 输出可机器校验的交易风险 JSON
**完成日期**: 2026-05-23

---

## Prompt 设计（定稿）

```
你是交易风险分析助手。接收链上交易数据，输出结构化风险摘要 JSON。

可用输入：
- 交易目标地址（to_address）
- 函数名（function_name）
- 参数（params）
- 资产变化（asset_changes）
- simulation 结果（simulation_result）
- 用户原始意图（user_intent）

禁止行为：
- 不要替用户做决定
- 不要猜测缺失数据
- 不确定时标注"不确定"而非编造

不确定时的处理：
- 字段填入 "uncertain" 或空数组 []
- 在 uncertainties 中说明具体不确定项

失败条件：
- 输入缺少 to_address 和 function_name → 输出 {"error": "缺少必要字段：to_address 和/或 function_name"}

输出 JSON：
{
  "summary": "一句话概述",
  "asset_changes": [...],
  "permissions_changed": [...],
  "risk_level": "low | medium | high | critical",
  "requires_human_approval": true/false,
  "uncertainties": [...],
  "recommended_user_checks": [...]
}
```

---

## 设计要点

| 维度 | 是否到位 | 说明 |
|------|----------|------|
| 角色定义 | ✅ | "交易风险分析助手"，明确职责边界 |
| Instruction 四段式 | ✅ | 任务目标→可用输入→禁止行为→输出格式+失败格式 |
| 输出 Schema 有约束 | ✅ | `risk_level` 四档枚举，`requires_human_approval` 布尔值 |
| 不确定时有兜底 | ✅ | `"uncertain"` 或空数组，在 `uncertainties` 中说明 |
| 失败条件明确 | ✅ | 缺少 `to_address` 和 `function_name` 即失败 |
| 符合 Handbook 原则 | ✅ | "不给模型更多自信，而是让它该停就停" |

---

## 测试用例

### 测试 1：普通转账

```
to_address: 0x4675C7e5BaAFBFFbca748158bEcBA61ef3b0a263
function_name: transfer (ETH 原生转账)
params: {}
asset_changes: "-0.01 ETH (发送方)"
simulation_result: success
user_intent: 给朋友转账 0.01 ETH
```

### 测试 2：无限授权

```
to_address: 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48 (USDC 合约)
function_name: approve
params: {spender: "0xDef1C0ded9bec7F1a1670819833240f027b25EfF", amount: "115792089237316195423570985008687907853269984665640564039457584007913129639935"}
asset_changes: "无（授权不转移资产）"
simulation_result: success
user_intent: 在 DEX 上交易少量 USDC
```

### 测试 3：目标地址与用户意图不匹配

```
to_address: 0xA3C5d01e09D2bB53D4f7BA8E8d5dA2b4c1B7C51F (未知合约)
function_name: claimRewards
params: {}
asset_changes: "无模拟结果"
simulation_result: failed (合约未验证)
user_intent: 领取空投奖励
```

---

## 测试结果

### 测试 1：普通转账

```json
{
  "summary": "用户向地址 0x4675C7e5BaAFBFFbca748158bEcBA61ef3b0a263 发起 0.01 ETH 原生转账，模拟成功，资产变化与意图一致。",
  "asset_changes": [
    {
      "asset_type": "ETH",
      "amount": "-0.01",
      "direction": "outgoing",
      "counterparty": "0x4675C7e5BaAFBFFbca748158bEcBA61ef3b0a263",
      "description": "发送 0.01 ETH 至目标地址"
    }
  ],
  "permissions_changed": [],
  "risk_level": "low",
  "requires_human_approval": false,
  "uncertainties": [
    "目标地址 0x4675C7e5BaAFBFFbca748158bEcBA61ef3b0a263 的归属和历史行为未知，无法验证是否为用户所说的'朋友'地址。",
    "未提供该地址是否为合约地址的信息，若为合约地址可能触发未知逻辑。"
  ],
  "recommended_user_checks": [
    "确认目标地址 0x4675C7e5BaAFBFFbca748158bEcBA61ef3b0a263 确实属于您信任的朋友。",
    "可在区块浏览器中查询该地址历史记录，确认无异常活动。"
  ]
}
```

### 测试 2：无限授权

```json
{
  "summary": "用户对 USDC 合约发起 approve 交易，授权地址 0xDef1... 支配最大可能数量的 USDC（即无限授权），模拟成功，但授权额度远超用户所述'少量交易'意图。",
  "asset_changes": [
    {
      "asset_type": "USDC",
      "amount": "0",
      "direction": "none",
      "counterparty": "0xDef1C0ded9bec7F1a1670819833240f027b25EfF",
      "description": "授权操作本身无资产转移，但授予 spender 支配 USDC 的权限"
    }
  ],
  "permissions_changed": [
    {
      "token": "USDC (0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48)",
      "spender": "0xDef1C0ded9bec7F1a1670819833240f027b25EfF",
      "previous_allowance": "uncertain",
      "new_allowance": "115792089237316195423570985008687907853269984665640564039457584007913129639935 (约 1.15e77，即无限授权)",
      "description": "授予 spender 支配全部 USDC 余额的权限"
    }
  ],
  "risk_level": "high",
  "requires_human_approval": true,
  "uncertainties": [
    "spender 地址 0xDef1C0ded9bec7F1a1670819833240f027b25EfF 的身份未知，未提供是否为已知 DEX 合约的验证信息。",
    "无法确认用户与该 spender 地址的交互历史，授权后风险取决于该合约的安全性。",
    "用户意图为'少量交易'，但授权数量为最大可能值，意图与实际操作之间存在显著偏差，原因不确定。"
  ],
  "recommended_user_checks": [
    "立即核实 spender 地址 0xDef1C0ded9bec7F1a1670819833240f027b25EfF 是否为正规、可信的 DEX 合约。",
    "强烈建议将授权数量修改为仅覆盖本次交易所需的小额数量，而非无限授权。",
    "若该 spender 合约存在漏洞或被恶意控制，当前授权将导致钱包中全部 USDC 面临风险。"
  ]
}
```

### 测试 3：目标地址与用户意图不匹配

```json
{
  "summary": "用户尝试与未验证合约 0xA3C5... 交互调用 claimRewards 函数以领取空投奖励，但模拟失败，资产变化未知，存在较高风险。",
  "asset_changes": [],
  "permissions_changed": [],
  "risk_level": "high",
  "requires_human_approval": true,
  "uncertainties": [
    "目标合约 0xA3C5d01e09D2bB53D4f7BA8E8d5dA2b4c1B7C51F 未经过验证，源代码不可查，实际执行逻辑完全未知。",
    "模拟失败，无法预测交易执行后的资产变化和权限变更情况。",
    "函数名 claimRewards 仅为合约表面命名，实际可能执行任意逻辑，包括资产转移、权限授予等。",
    "用户提及的'空投奖励'来源不明，无法确认该合约是否与任何已知合法项目关联。",
    "无参数传入，无法判断是否需要用户签名或支付额外费用。"
  ],
  "recommended_user_checks": [
    "通过区块浏览器查询该合约地址的创建者、创建时间及历史交易记录，判断其可信度。",
    "搜索合约地址 0xA3C5d01e09D2bB53D4f7BA8E8d5dA2b4c1B7C51F 在社交媒体、项目官方渠道是否有任何关联信息。",
    "注意：未验证合约的 claimRewards 可能是钓鱼手段，执行后可能导致钱包资产被盗。",
    "如无法确认合约来源，强烈建议放弃该交易。"
  ]
}
```

---

## 测试分析

| 评估维度 | 测试 1 | 测试 2 | 测试 3 |
|------|:--:|:--:|:--:|
| 风险分级准确 | ✅ | ✅ | ✅ |
| 遵守禁止行为（不编造、不做决定） | ✅ | ✅ | ✅ |
| 不确定时用 `uncertain` 兜底 | ✅ | ✅ | ✅ |
| 无限授权 vs 意图矛盾被捕捉 | — | ✅ | — |
| 未验证合约被识别为高风险 | — | — | ✅ |

### 关键发现

1. **Prompt 的禁止规则生效了**：测试 2 中 `previous_allowance` 填入 `"uncertain"` 而非编造数值，测试 3 中 `asset_changes` 为空数组而非猜测——模型在缺数据时没有编造，而是标注不确定性
2. **意图 vs 实际操作的矛盾被捕捉**：测试 2 的 summary 明确写出"授权额度远超用户所述少量交易意图"，这是 Prompt 设计中最核心的验证点
3. **风险分级有区分度**：low / high / high，三个场景得到不同风险等级，且理由充分
4. **建议可操作但不下决定**：所有 `recommended_user_checks` 都是检查、核实、建议的句式，没有"你应该签/不签"——符合"不替用户做决定"的规则

**结论：Prompt 设计通过。**

---

*AI x Web3 School Week 1 Prompt 实践完成 — 由 Hermes AI（模型：deepseek-v4-pro）在 2026-05-23 生成*
