# Day 3: Prompt & Context 学习对话记录

**日期**: 2026-05-20  
**主题**: GitHub 配置、Prompt 模板设计、Context 工程学习笔记

---

## 一、GitHub 配置流程（简略）

### 1.1 gh CLI 检测结果

| 项目 | 状态 |
|------|------|
| gh CLI | ❌ 未安装（无 sudo 权限） |
| git | ✅ 已配置 |
| 仓库 | ✅ `Flygreenbaby/ai-web3-learning` |

**用户决定**: 使用 `git + token` 方案

### 1.2 配置执行

- 删除旧仓库：`rm -rf /opt/data/ai-web3-learning`
- 配置 Git 身份：`Flygreenbaby <hxqlst@163.com>`
- 重新克隆：`git clone https://github.com/Flygreenbaby/ai-web3-learning.git`
- 验证连通：✅ 成功

---

## 二、Prompt 模板设计对话（核心）

### 2.1 四段式结构确认

**用户问题**: Prompt 是软约束还是硬约束？

**回答**:
> Prompt 是**软约束**，真正的安全边界必须由代码、权限、校验和审计承担。高风险动作不能只靠 prompt 拦截。

**确定的四段式结构**:
```
[任务目标]
[可用输入]
[禁止行为]
[输出格式 & 失败格式]
```

### 2.2 Few-shot vs Structured Output

**用户问题**: Few-shot 和 Structured Output 有什么区别？

**回答**:
| 特性 | Few-shot | Structured Output |
|------|----------|-------------------|
| 用途 | 风格模仿、边界模糊场景 | 固定格式供代码处理 |
| 输出 | 自由文本 | JSON/schema 约束 |
| 适用场景 | 难以一句话说清的任务 | 必须固定字段的任务 |

**关键结论**: 两者可组合使用

### 2.3 Prompt 模板生成

**用户需求**: 创建一个 Prompt 模板，把任意学习文档改写成复习笔记

**生成的模板字段**:
- `summary`: 一句话总结核心要点
- `key_points`: 关键知识点列表
- `questions`: 引导思考的问题
- `analogy`: 比喻解释
- `template`: 从文档中提取的实际模板

**用户偏好**:
- ✅ 输出纯 JSON，不要带 Review 分析
- ✅ 输入文档链接留空，由用户每次填写
- ❌ 禁止输出两个文件
- ❌ 禁止大量笔记删减

### 2.4 Context 工程笔记生成

**用户要求**: 用 Prompt 模板执行 Context 文档学习笔记

**生成内容**:
- Summary: 30 字以内
- Key Points: 5 个核心观点
- Questions: 3 个深挖方向
- Analogy: 工作桌面比喻
- Templates: 
  1. Context Engineering 稳定结构示例
  2. 信息来源分级表
  3. Memory 风险检查清单

---

## 三、学习笔记整合对话（核心）

### 3.1 文件命名讨论

**用户要求**: 
- 将 Prompt、Context 笔记整理到一个 md 文档
- 按照 `notes/week1` 下文件名对齐进行有规律的命名
- 禁止出现两个文件
- 禁止大量笔记删减

**最终命名**: `day3-prompt-and-context.md`

### 3.2 整合内容结构

```markdown
# Day 3: Prompt Engineering & Context Engineering

## 第一部分：Prompt Engineering
- Summary (30字以内)
- Key Points (5个)
- Questions (3个)
- Analogy (比喻解释)
- Templates (3个实际模板)

## 第二部分：Context Engineering
- Summary (30字以内)
- Key Points (5个)
- Questions (3个)
- Analogy (比喻解释)
- Templates (3个实际模板)

## 第三部分：Prompt vs Context 对比
## 第四部分：综合 Questions
```

---

## 四、真实仓库结构确认（简略）

**用户要求**: 展示本机学习仓库结构，禁止虚构

**展示结果**:
```
.
├── LICENSE
├── README.md
├── logs
│   └── day2-qa.md
└── notes
    └── week1
        ├── day1-Hermes.md
        └── day2-llm-basics.md
```

**重要说明**: 
- 无 `day3-prompt-and-context.md`（当时尚未创建）
- 无 `prompts/` 目录
- 无 `demos/` 目录

---

## 五、Git 操作执行（简略）

### 5.1 创建并推送笔记

**执行步骤**:
```bash
# 1. 创建文件
write_file notes/week1/day3-prompt-and-context.md

# 2. Git 操作
git add .
git commit -m "Add Day 3 Prompt & Context learning notes"
git push
```

**提交详情**:
- Commit: `f75ef7e`
- 文件: `notes/week1/day3-prompt-and-context.md`
- 行数: 252 行

### 5.2 创建对话日志

**执行步骤**:
```bash
# 1. 创建文件
write_file logs/day3-prompt-context-qa.md

# 2. Git 操作
git add .
git commit -m "Add Day 3 Prompt & Context conversation log"
git push
```

**提交详情**:
- Commit: 新提交
- 文件: `logs/day3-prompt-context-qa.md`

---

## 六、核心观点总结

### 6.1 Prompt 核心观点

| 概念 | 要点 |
|------|------|
| 本质 | 人与模型的接口设计，可执行协议 |
| 约束 | **软约束**，不是安全边界 |
| 结构 | 四段式：目标/输入/禁止/格式 |
| 风险 | Prompt Injection |
| 安全 | 代码层校验 + 人工审批 |

### 6.2 Context 核心观点

| 概念 | 要点 |
|------|------|
| 本质 | 模型可见的信息空间 |
| 核心 | 区分可信来源与权限边界 |
| 问题 | "看见了但没抓住重点" |
| 安全 | 记忆可撤销 + 重新授权 |

### 6.3 Prompt vs Context 对比

| 维度 | Prompt | Context |
|------|--------|---------|
| 作用 | 定义任务目标/输出格式 | 提供可信信息/边界 |
| 重点 | 指令清晰/格式校验 | 来源标注/权限隔离 |
| 安全 | 软约束（可覆盖） | 信息治理（分级） |
| 风险 | Injection 攻击 | 信息过载/越权 |

---

## 七、后续任务

| 任务 | 状态 |
|------|------|
| Day 3 笔记整合 | ✅ 完成 |
| Day 3 对话日志 | ✅ 完成 |
| Git 推送 | ✅ 完成 |
| Day 4 学习主题 | ⏳ 待确定（RAG/Memory/Agent Workflow） |

---

*对话记录结束*
