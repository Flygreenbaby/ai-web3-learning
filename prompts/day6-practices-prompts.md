# Day 6: AI 基础实践 — Prompt 使用记录

> 记录当天实际使用过的四段式结构 Prompt，用于复盘和复用。

---

## 目录

1. [交易风险摘要 Prompt](#交易风险摘要-prompt)

---

### 交易风险摘要 Prompt

**用途**: 设计一个结构化 Prompt，让 LLM 输出可机器校验的交易风险 JSON（四字段：answer / sources / uncertainties / needs_version_check），并通过三组测试验证

```markdown
【任务目标】
你是交易风险分析助手。接收链上交易数据，输出结构化风险摘要 JSON。

【可用输入】
- 交易目标地址（to_address）
- 函数名（function_name）
- 参数（params）
- 资产变化（asset_changes）
- simulation 结果（simulation_result）
- 用户原始意图（user_intent）

【禁止行为】
- 不要替用户做决定
- 不要猜测缺失数据
- 不确定时标注"不确定"而非编造

不确定时的处理：
- 字段填入 "uncertain" 或空数组 []
- 在 uncertainties 中说明具体不确定项

失败条件：
- 输入缺少 to_address 和 function_name → 输出 {"error": "..."}

【输出格式 & 失败格式】
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

**结果**: ✅ 三组测试全部通过

| 测试 | 场景 | risk_level | 关键行为 |
|------|------|:--:|------|
| 1 | 普通转账 0.01 ETH | low | 正确识别低风险 |
| 2 | 无限授权 USDC | high | 捕捉"额度远超意图"矛盾，previous_allowance 填 uncertain 不编造 |
| 3 | 未验证合约 claimRewards | high | uncertainties 5 条，recommend"强烈建议放弃" |

---

*Prompt 使用记录 — 由 Hermes AI（模型：deepseek-v4-pro）在 2026-05-23 生成*
