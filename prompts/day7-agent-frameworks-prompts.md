# Day 7 Prompt 学习记录

**日期**: 2026-05-24

---

## Prompt 1 — Agent 实践设计

**场景**: 设计 DAO 提案研究 Agent 规格

**Prompt 要点**:
- 目标：只读研究 → 输出检查清单，不投票不签名
- 5 个只读工具，每项用 Tool Use 6 问定义
- State 外置可查（字段清单而非模糊描述）
- Permission：只读自动、写入确认、发送禁止
- Stop：提案不存在/讨论缺失/高危风险/信息严重不足/用户拒绝
- 输出 schema：JSON 含 sources/summary/pro&con/uncertainties/risks/checklist
- 权限升级版：用户授权 → simulation → 二次确认 → 生成草稿（不自动发送）

**使用的 Agent 框架**:
```
Goal → Tools → State → Permission → Stop → Output Schema → Upgrade Path
```

---

## Prompt 2 — Frameworks 实践：Raw API vs DSPy

**场景**: 同一任务用两种方式实现并四维对比

**任务**: 文档问答 + 工具调用（DAO 研究助手）
**测试用例**: 
1. 正常提案 #42
2. 不存在的提案 #999（边界测试）

**对比维度**:
1. 更易读懂？ → A（Raw）领先
2. 更易加工具？ → B（DSPy）领先
3. 更易定位错误？ → A（Raw）领先
4. 更易写回归测试？ → B（DSPy）领先

**关键发现**: 
- 框架的隐形收益是测试纪律（自动跑了两个用例 vs 只跑一个）
- 框架的代价是依赖膨胀（DSPy→LiteLLM→botocore）
- 简单任务 Raw 更可控，复杂任务框架优势才显现

---

## Prompt 3 — Vibe Coding 实践（暂停）

**场景**: 安装配置 AI Coding 工具 + 完成工程闭环

**暂停原因**: 本地缺 Node.js 环境
**后续**: 安装 Node.js 后补做

**任务边界模板**:
```
【要做什么】
【可以改的文件】
【绝对不能动的文件】
【允许运行的命令】
【停止条件】
```

---

*AI x Web3 School Day 7 课程完成 — 由 Hermes AI（模型：deepseek-v4-pro）在 2026-05-24 生成*
