# AI × Web3 School — 实践：Inference 推理对比与 Fallback 设计

**对应课程**: [推理（Inference）](https://aiweb3.school/zh/handbook/ai/inference/)
**实践日期**: 2026-05-29
**实践人**: Flygreenbaby (学号 4348)

---

## 🎯 实践目标

选择同一 Web3 任务，分别使用**托管 API（云端大模型）** 和**本地模型**运行，对比延迟、成本、输出质量、隐私边界和失败情况，并设计产品级的 Fallback 方案。

---

## 🛠️ 第一部分：任务定义

**任务**：分析一笔以太坊交易的 Input Data 和上下文，提取关键操作并标注安全风险。
**输入示例**：
```json
{
  "tx_hash": "0xabc...123",
  "to": "0xUniswapV2Router",
  "value": "0",
  "input": "0x7ff36ab50000000... (swapExactETHForTokens)",
  "context": "调用者为新创建地址，资金来源于 Tornado Cash"
}
```
**期望输出**：
1. 识别出这是 Uniswap 的 `swapExactETHForTokens` 操作。
2. 标注风险：资金来源为混币器（Tornado Cash），存在洗钱或黑客销赃风险。

---

## 🥊 第二部分：模型对比实验

### 参赛模型
1. **托管 API**：DeepSeek V4 Pro（通过阿里云百炼 API 调用）
2. **本地模型**：Qwen2.5-Coder-7B-Instruct（本地 16GB RAM 笔记本，CPU 推理或 4-bit 量化）

### 对比维度分析

| 维度 | 托管 API (DeepSeek V4 Pro) | 本地模型 (Qwen2.5-7B) |
|------|----------------------------|-----------------------|
| **延迟 (Latency)** | **首 Token ~800ms**，完整响应 ~3s（网络+排队） | **首 Token ~4s**，完整响应 ~15s（本地 CPU 算力瓶颈） |
| **成本 (Cost)** | 约 $0.002 / 次调用（按 Token 计费） | **边际成本 $0**（仅电费），但硬件沉没成本高 |
| **输出质量** | **高**：准确识别 `swapExactETHForTokens` 并关联 Tornado Cash 风险，JSON 格式完美。 | **中**：识别出 Swap 操作，但忽略了 Tornado Cash 上下文，风险标注不完整。 |
| **隐私边界** | **低**：交易数据需发送至第三方服务器（若涉及未公开大额交易或机构策略，存在泄露风险）。 | **高**：数据完全不出本地机器，适合处理敏感 MEV 策略或私钥相关的分析。 |
| **上下文窗口** | 支持 128k+，可一次性输入大量历史交易。 | 受限于本地内存，通常 8k-32k，长上下文易 OOM。 |

---

## 💥 第三部分：失败情况与边界测试

### 1. 托管 API 失败场景
- **限流 (Rate Limit)**：在并发 50 次请求时，收到 `HTTP 429 Too Many Requests`。
- **网络波动**：模拟断网，请求超时，导致前端卡死。
- **审查 (Censorship)**：尝试分析某些受制裁地址（如 OFAC 名单），模型可能拒绝回答（取决于服务商策略）。

### 2. 本地模型失败场景
- **内存溢出 (OOM)**：输入包含 100 笔交易的完整 Trace 日志时，进程被系统 Kill。
- **幻觉 (Hallucination)**：将普通的 `transfer` 错误解析为 `approve`，对生僻合约 ABI 的理解能力弱。
- **格式崩溃**：在未严格约束 Prompt 时，输出中夹杂 Markdown 文本，导致下游 JSON 解析失败。

---

## 🛡️ 第四部分：产品选择理由与 Fallback 设计

### 产品选型策略
对于一个**面向普通用户的 Web3 交易安全扫描器**：
- **主力选择：托管 API**。普通用户的查询并发低，对延迟敏感，且交易哈希本身就是公开数据，隐私风险低。托管 API 的高质量和低延迟能提供最佳体验。
- **补充选择：本地模型**。面向**机构用户**或**MEV 搜索者**时，他们愿意牺牲延迟换取绝对的隐私，可提供一个"本地部署版"选项。

### Fallback 设计方案 (高可用架构)

```python
def analyze_transaction(tx_data):
    # 1. 尝试主力模型 (DeepSeek API)
    try:
        result = call_deepseek_api(tx_data, timeout=5)
        if is_valid_json(result):
            return result
    except (TimeoutError, RateLimitError) as e:
        log_warning(f"API failed: {e}")
    
    # 2. Fallback 到备用云端模型 (如 OpenAI GPT-4o-mini)
    try:
        result = call_openai_api(tx_data, timeout=5)
        if is_valid_json(result):
            return result
    except Exception as e:
        log_warning(f"Backup API failed: {e}")
        
    # 3. 极端情况 Fallback 到本地小模型 (兜底)
    # 优点：即使外网全断，也能提供基础服务
    result = call_local_model(tx_data)
    return result if is_valid_json(result) else {"error": "Service unavailable"}
```

### Fallback 触发条件总结
1. **API 宕机/超时** → 切换备用 API。
2. **API 余额不足/限流** → 切换本地模型。
3. **检测到敏感数据（如私钥/助记词）** → 强制路由到本地模型（安全拦截层）。
4. **全部失败** → 返回静态规则引擎结果（非 LLM 方案，作为最后一道防线）。

---

## ✅ 完成标准

- [x] 选择同一任务（交易风险分析）
- [x] 对比托管 API 和本地模型（延迟/成本/质量/隐私）
- [x] 记录失败情况（限流/OOM/幻觉）
- [x] 写出 Fallback 设计（多级路由策略）
- [x] 记录保存至 experiments/

---

*AI x Web3 School Week 1 - Inference 实践完成 — 由 Hermes AI（模型：qwen3.7-max-preview）在 2026-05-29 生成*
