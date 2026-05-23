# Day 6: AI 基础实践 — 学习对话记录

**日期**: 2026-05-23
**主题**: 完成 LLM / Prompt / Context / RAG 四篇课程实践

---

## 目录

1. [LLM 实践：交易解释器](#一llm-实践交易解释器)
2. [Prompt 实践：交易风险摘要](#二prompt-实践交易风险摘要)
3. [Context 实践：Context Spec 设计](#三context-实践context-spec-设计)
4. [RAG 实践：文档问答系统](#四rag-实践文档问答系统)
5. [Workflow 优化讨论](#五workflow-优化讨论)
6. [核心观点总结](#核心观点总结)
7. [文件产出](#文件产出)

---

## 一、LLM 实践：交易解释器

### 1.1 实践目标确立

**用户问题**: LLM 篇的实践应该怎么完成？

**回答要点**:
- 从 Handbook 原文提取：做一个"交易解释器"的最小版本
- 输入一笔交易哈希 → 读取链上数据 → LLM 生成解释
- 输出五维度：动作 / 资产地址 / 链上事实 vs 推断 / 不确定性 / 用户检查项

| 项目 | 内容 |
|------|------|
| 结论 | 配合方式：用户找交易 → Hermes 抓链上数据 → 用户审阅解释 |

### 1.2 Etherscan 找交易

**用户问题**: 如何在 Etherscan 找到合适的交易？

**回答要点**:
- 条件：简单 ETH 转账、Success、近 7 天
- 方法：etherscan.io/txs → 找 Method=Transfer、Status=✅
- 捷径：搜 vitalik.eth → Transactions 标签 → Transfer

| 项目 | 内容 |
|------|------|
| 结论 | 用户成功找到交易 `0x92a1bbcf…a794204` |

### 1.3 链上数据抓取与分析

**用户问题**: 抓取交易详情并生成解释

**回答要点**:
- Etherscan API v1 已弃用，curl 被 Cloudflare 拦截
- 改用 Blockscout API 成功获取交易数据
- 解释五维度全部覆盖，区分"链上数据"与"模型推断"

| 项目 | 内容 |
|------|------|
| 结论 | bob-the-builder.eth → 未知地址，0.01 ETH，纯转账，Success |

---

## 二、Prompt 实践：交易风险摘要

### 2.1 Prompt 设计迭代

**用户问题**: Prompt 怎么设计才能通过 Handbook 要求？

**回答要点**:
- 第一版问题：地址写死、缺角色定义、字段无约束、失败条件模糊
- 第二版修正：加角色、risk_level 枚举、uncertain 兜底、失败条件明确
- 符合 Handbook 四段式：任务目标 / 可用输入 / 禁止行为 / 输出格式

| 项目 | 内容 |
|------|------|
| 结论 | 两轮迭代通过审阅 |

### 2.2 三组测试验证

**用户问题**: 用 DeepSeek 跑三组测试用例

**回答要点**:
- 测试 1（普通转账）：risk_level=low，正确
- 测试 2（无限授权）：捕捉到"额度远超意图"矛盾，risk_level=high，previous_allowance=uncertain（不编造）
- 测试 3（未验证合约）：uncertainties 5 条最详细，recommend"强烈建议放弃"

| 项目 | 内容 |
|------|------|
| 结论 | 三组全部通过，Prompt 设计有效 |

---

## 三、Context 实践：Context Spec 设计

### 3.1 上下文分类训练

**用户问题**: 7 项上下文应该怎么分类（实时/缓存/不可信）？

**回答要点**:
- 用户初始分类有错误：allowance 误当缓存、dApp 页面误当实时查询
- Hermes 逐一纠正并给出理由
- 关键认知转变：链上状态（allowance）会随时被其他交易改变，必须实时查；dApp 页面是外部不可信来源，绝不能当事实

| 项目 | 内容 |
|------|------|
| 结论 | 🔴 4 项（区块/余额/spender地址/approve数量）🟡 3 项（chain id/合约地址/白名单）⚪ 3 项（simulation/dApp说明/用户意图） |

### 3.2 分类说明固化

**用户问题**: 怕记不住红黄白分类含义，需要说明

**回答要点**:
- 补充了三色分类的判断标准表
- 每个标记对应一条可操作的判断准则

| 项目 | 内容 |
|------|------|
| 结论 | 分类体系写入实验文件，形成可复用模板 |

---

## 四、RAG 实践：文档问答系统

### 4.1 技术方案选择

**用户问题**: 哪个文档站合适？电脑性能差怎么办？

**回答要点**:
- 确认 zh.javascript.info 结构清晰，适合 RAG
- 因本地性能限制，用 TF-IDF 替代 sentence-transformers embedding
- 依赖精简为 3 个包（requests + beautifulsoup4 + scikit-learn，~35MB）

| 项目 | 内容 |
|------|------|
| 结论 | Windows venv 环境搭建完成，脚本运行成功 |

### 4.2 虚拟环境教学

**用户问题**: 不知道在哪装依赖、venv 和虚拟机搞混

**回答要点**:
- 解释 venv ≠ 虚拟机：只是一个文件夹，隔离 Python 包，不占资源
- Windows 命令与 Linux 不同：`venv\Scripts\activate` 而非 `source venv/bin/activate`
- 创建项目：`mkdir ~/rag-practice` → `python -m venv venv` → `activate`

| 项目 | 内容 |
|------|------|
| 结论 | 用户成功搭建环境并运行脚本 |

### 4.3 测试结果分析

**用户问题**: 三组测试跑完，结果对吗？

**回答要点**:
- 测试 1（alert 作用）：检索不够精准，真正相关的"交互：alert、prompt 和 confirm"篇未进前三——TF-IDF 无语义理解的局限
- 测试 2（React useEffect）：正确拒答，sources=[]，uncertainties 标注到位
- 测试 3（let vs var ES6）：触发 needs_version_check=True，但 uncertainties 漏标"文档中未找到对比内容"

| 项目 | 内容 |
|------|------|
| 结论 | 实践成功暴露了 TF-IDF 的局限性，这正是 RAG 那篇要教的核心：检索结果只是候选证据，不是事实本身 |

---

## 五、Workflow 优化讨论

### 5.1 实践 vs 打卡流程

**用户问题**: Prompt 测试还没跑，先保存再继续下一章？

**回答要点**:
- Hermes 自检：Prompt 实践只完成了设计阶段，测试未跑
- 用户选择先跑完三组测试再收工
- 体现了"不跳过未完成步骤"的纪律

| 项目 | 内容 |
|------|------|
| 结论 | 每篇实践必须完整：设计 + 执行 + 分析 + 保存 |

---

## 核心观点总结

| 概念 | 要点 |
|------|------|
| 链上数据 vs 模型推断 | 即使最简单的 ETH 转账，能确定的东西也比看起来少得多 |
| Prompt 设计 | 不是在写"神奇咒语"，而是在写可机器校验的任务说明书 |
| Context 分层 | 每条信息进上下文时，必须带着"身份标签"（来源、时效、可信度） |
| RAG 证据链 | TF-IDF 只能做词频匹配，语义检索需要 embedding 模型 |
| RAG 拒答 | 找不到证据时应该说"不确定"，而不是让模型补全 |

---

## 文件产出

| 文件 | 用途 |
|------|------|
| experiments/week1-llm-transaction-interpreter.md | LLM 交易解释器实践 |
| experiments/week1-prompt-risk-analyzer.md | Prompt 设计 + 三组测试 |
| experiments/week1-context-context-spec.md | Context 上下文规范设计 |
| experiments/week1-rag-qa.md | RAG 文档问答系统 + 脚本 |
| experiments/week1-rag-qa/rag_demo.py | RAG Python 脚本 |

---

*学习对话记录生成 — 由 Hermes AI（模型：deepseek-v4-pro）在 2026-05-23 生成*
