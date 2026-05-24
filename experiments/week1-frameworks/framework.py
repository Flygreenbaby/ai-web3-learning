"""
版本 B：使用 DSPy 框架
框架自动管理：tool schema、trace、失败重试、测试样本
"""
import json
import os
import dspy

# === 配置 DeepSeek 作为 DSPy 的 LM ===
lm = dspy.LM(
    model="openai/deepseek-chat",
    api_base="https://api.deepseek.com",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    temperature=0.3
)
dspy.configure(lm=lm)

# === 模拟文档检索（和 A 版本一样）===
FAKE_DOCS = [
    "提案 #42：将金库 5% 分配给 Grants 计划，锁定期 6 个月，由多签控制。",
    "论坛讨论 #1：支持方认为 Grants 能吸引开发者，反对方担心资金滥用。",
    "论坛讨论 #2：提议先做 1% 试点，评估效果后再追加。",
]

def search_docs(query: str) -> list:
    """模拟搜索工具 — DSPy 会把它注册为 tool"""
    return FAKE_DOCS

# === 定义 Signature（DSPy 的核心概念）===
class DAOResearch(dspy.Signature):
    """分析 DAO 提案，输出结构化研究结果"""
    question: str = dspy.InputField(desc="用户的问题")
    docs: list = dspy.InputField(desc="检索到的相关文档")
    
    answer: str = dspy.OutputField(desc="基于文档的回答")
    sources_used: list = dspy.OutputField(desc="引用的文档")
    confidence: str = dspy.OutputField(desc="high / medium / low")
    missing_info: list = dspy.OutputField(desc="缺失的信息")

# === 定义 Module（业务逻辑）===
class DAOResearchModule(dspy.Module):
    def __init__(self):
        super().__init__()
        self.researcher = dspy.ChainOfThought(DAOResearch)
    
    def forward(self, question: str):
        docs = search_docs(question)
        return self.researcher(question=question, docs=docs)

# === 测试样本（框架对比的关键：可回归测试）===
test_cases = [
    {
        "question": "提案 #42 的支持和反对理由是什么？有什么风险？",
        "expected_has_answer": True,
        "expected_has_sources": True,
    },
    {
        "question": "提案 #999 是什么？",
        "expected_has_answer": False,  # 无相关文档
    },
]

# === 运行对比 ===
if __name__ == "__main__":
    module = DAOResearchModule()
    
    for i, case in enumerate(test_cases):
        print(f"\n{'='*50}")
        print(f"测试 {i+1}: {case['question']}")
        print(f"{'='*50}")
        
        # 框架自动重试 + trace（无需手写 try/except）
        result = module(question=case["question"])
        
        print(f"回答: {result.answer[:100]}...")
        print(f"来源: {result.sources_used}")
        print(f"置信度: {result.confidence}")
        print(f"缺失信息: {result.missing_info}")
