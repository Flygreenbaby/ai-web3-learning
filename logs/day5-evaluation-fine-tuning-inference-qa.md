# Day 5: Evaluation + Fine-tuning + Inference 学习对话记录

**日期**: 2026-05-22
**主题**: AI 基础收官——评估体系、微调策略、推理部署

---

## 目录

1. [仓库结构初始化](#一仓库结构初始化)
2. [Evaluation 评估](#二evaluation-评估)
3. [Fine-tuning 微调](#三fine-tuning-微调)
4. [Inference 推理服务](#四inference-推理服务)
5. [核心观点总结](#核心观点总结)
6. [文件产出](#文件产出)

---

## 一、仓库结构初始化

### 1.1 对比启动 Prompt 补齐结构

**用户问题**: 启动 Prompt 和 Handbook 推荐的仓库结构与我现有的差异在哪？
**回答要点**: 对比发现缺少 profile.md / learning-plan.md / daily/ / templates/ / handbook-feedback/ / experiments/ 等，按需精简为 4 个核心目录 + 2 个模板文件

| 项目 | 内容 |
|------|------|
| 结论 | 保留现有仓库名，只补缺不改名，最终新增 4 目录 + 5 文件 |

### 1.2 README 隐私提醒修正

**用户问题**: 我的邮箱 hxqlst@gmail.com 已公开写在 README 里，隐私提醒里"未公开联系方式"不合适
**回答要点**: 去掉该条目，保留 API Key / Token / 私钥 / 助记词 / 他人数据

### 1.3 Prompt ⑥ 创建

**用户问题**: 新目录 daily/ 需要的文件怎么生成？要不要像五个 Prompt 一样写 Prompt？
**回答要点**: 评估后确定 daily/ 需要 Prompt⑥，其余目录不需要；当天生成并保存到 prompts/ 目录

---

## 二、Evaluation 评估

### 2.1 核心概念学习

**用户问题**: 加载 review-note-generator，学习 Evaluation 章节
**回答要点**:
- Evaluation 是把"感觉变好了"变成可重复测量的系统工程
- 五大知识节点：Harness（框架）、Golden Set（黄金集）、LLM-as-Judge（模型评判）、Regression（回归测试）、Observability（可观测性）
- AI × Web3 场景 eval 更重要：错误可能影响资产、权限、链上执行
- 比喻：年检+行车记录仪

| 项目 | 内容 |
|------|------|
| 结论 | 没有 eval 的 AI 系统 = 没年检的车上高速 |

---

## 三、Fine-tuning 微调

### 3.1 核心概念学习

**用户问题**: 继续学习 Fine-tuning 章节
**回答要点**:
- FT 不是第一步——先检查 prompt / context / RAG / schema
- SFT（监督微调）+ LoRA（低秩适配）+ PEFT（参数高效微调）
- Dataset 是核心资产，必须有训练/验证/测试/回归四集切分
- Overfitting：训练例子上完美，真实用户一问就崩
- FT 不能替代：链上状态、合约审计、交易模拟、钱包权限

| 项目 | 内容 |
|------|------|
| 结论 | 先有 eval 再谈 FT；先修数据再修模型 |

---

## 四、Inference 推理服务

### 4.1 核心概念学习

**用户问题**: 继续学习 Inference 章节
**回答要点**:
- 推理不是"调 API 拿结果"，是延迟/成本/质量/隐私/运维的平衡
- 四层知识：API Model（托管）、Local Model（本地）、Quantization（量化）、Serving（服务化）
- AI × Web3 特需：链上动作不可逆 → 必须留可审计记录
- 比喻：外卖 vs 自家厨房 vs 中央厨房

| 项目 | 内容 |
|------|------|
| 结论 | 选的不是一个模型，是一整套部署约束下的服务方案 |

---

## 核心观点总结

| 概念 | 要点 |
|------|------|
| Evaluation | 可重复测量→可稳定改进；Harness+Golden Set+Regression 三件套 |
| Fine-tuning | 最后手段不是第一选择；先穷尽 prompt/eval 再谈训练 |
| Inference | 质量/成本/延迟三角权衡；链上场景必须留审计记录 |
| Prompt ⑥ | daily/ 打卡链路补齐，六个 Prompt 覆盖完整学习闭环 |

---

## 文件产出

| 文件 | 用途 |
|------|------|
| notes/week1/day5-evaluation.md | Evaluation 学习笔记 |
| notes/week1/day5-fine-tuning.md | Fine-tuning 学习笔记 |
| notes/week1/day5-inference.md | Inference 学习笔记 |
| prompts/每日打卡草稿生成.md | Prompt ⑥ 新增 |
| profile.md | 学员画像 |
| learning-plan.md | 4 周学习计划 |
