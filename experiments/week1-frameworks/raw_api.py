"""
版本 A：直接调用 DeepSeek API
无框架 — 手动管理 prompt、JSON 解析、重试
"""
import json
import os
from openai import OpenAI

# 配置 DeepSeek
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

# === 模拟的文档检索（假装搜到了相关文档）===
FAKE_DOCS = [
    "提案 #42：将金库 5% 分配给 Grants 计划，锁定期 6 个月，由多签控制。",
    "论坛讨论 #1：支持方认为 Grants 能吸引开发者，反对方担心资金滥用。",
    "论坛讨论 #2：提议先做 1% 试点，评估效果后再追加。",
]

def search_docs(query: str) -> list:
    """模拟搜索：实际项目中这里接入向量库或 API"""
    return FAKE_DOCS

def answer_via_raw_api(question: str) -> dict:
    """直接用 API 调用，手动管一切"""
    
    docs = search_docs(question)
    docs_text = "\n".join(f"- {d}" for d in docs)
    
    system_prompt = f"""你是一个 DAO 研究助手。
请基于以下检索到的文档回答用户问题。

检索结果：
{docs_text}

输出格式（必须是合法 JSON）：
{{
    "answer": "你的回答",
    "sources_used": ["引用的文档1", "引用的文档2"],
    "confidence": "high | medium | low",
    "missing_info": ["缺失的信息1"]
}}

规则：
- 只能基于检索结果回答，不能编造
- 如果文档不够，confidence 降为 low
- 缺失信息写出来
"""
    
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ],
        temperature=0.3
    )
    
    raw_output = response.choices[0].message.content
    
    # 手动解析 JSON（无框架帮处理）
    try:
        result = json.loads(raw_output)
    except json.JSONDecodeError:
        result = {"error": "JSON 解析失败", "raw": raw_output}
    
    return result

# === 运行 ===
if __name__ == "__main__":
    question = "提案 #42 的支持和反对理由分别是什么？有什么风险？"
    result = answer_via_raw_api(question)
    print(json.dumps(result, ensure_ascii=False, indent=2))
