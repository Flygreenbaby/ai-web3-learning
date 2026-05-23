# Week 1 实践：RAG — 协议文档 RAG 问答

**对应 Handbook**: https://aiweb3.school/zh/handbook/ai/rag/
**实践目标**: 构建一个最小 RAG 系统，验证"检索—引用—拒答"的证据链
**文档源**: https://zh.javascript.info/（15 篇）
**技术方案**: TF-IDF + 余弦相似度（因本地性能限制，替代 embedding 向量方案）
**完成日期**: 2026-05-23

---

## 环境搭建（可复现）

### 系统环境
- Windows 10/11 x64
- Python 3.x
- 终端：cmd

### 创建虚拟环境
```cmd
mkdir %USERPROFILE%\rag-practice
cd %USERPROFILE%\rag-practice
python -m venv venv
venv\Scripts\activate
```

### 依赖安装
```cmd
pip install requests beautifulsoup4 scikit-learn
```

| 包名 | 用途 | 大小 |
|------|------|------|
| requests | HTTP 请求，抓取网页 | ~500KB |
| beautifulsoup4 | HTML 解析，提取正文和标题 | ~500KB |
| scikit-learn | TF-IDF 文本向量化 + 余弦相似度检索 | ~30MB |

---

## RAG 脚本

保存为 `rag_demo.py`，运行 `python rag_demo.py`：

```python
"""
RAG 最小实践：JavaScript 文档问答
zh.javascript.info → 抓取 → 切 chunk → 检索 → 输出四字段
"""
import requests, re, os
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ========== 第1步：抓取页面 ==========
BASE = "https://zh.javascript.info"

# 选 15 篇不同章节的页面
PAGES = [
    "/intro", "/manuals-specifications", "/code-editors", "/devtools",
    "/hello-world", "/structure", "/strict-mode", "/variables",
    "/types", "/alert-prompt-confirm", "/type-conversions", "/operators",
    "/comparison", "/ifelse", "/logical-operators",
]

def fetch_page(path):
    """抓取一篇文章，返回 (标题, 正文纯文本)"""
    url = BASE + path
    soup = BeautifulSoup(requests.get(url, timeout=15).text, "html.parser")
    title = soup.find("h1")
    title = title.get_text(strip=True) if title else path
    body = soup.find("div", class_="article-formatted")
    if not body:
        body = soup.find("article") or soup.find("main") or soup.body
    return title, body.get_text("\n", strip=True)[:3000]

print("抓取文档中...")
docs = []
for p in PAGES:
    try:
        title, text = fetch_page(p)
        docs.append({"title": title, "url": BASE + p, "text": text})
        print(f"  ✅ {title}")
    except Exception as e:
        print(f"  ❌ {p}: {e}")

print(f"\n成功抓取 {len(docs)} 篇\n")

# ========== 第2步：按标题切 chunk ==========
def chunk_by_heading(text):
    """按 ## 标题切分，保留标题作为 chunk 描述"""
    chunks = []
    parts = re.split(r'\n(?=#{1,3}\s)', text)
    for part in parts:
        part = part.strip()
        if len(part) > 50:
            first_line = part.split("\n")[0].lstrip("#").strip()
            chunks.append({"heading": first_line[:80], "content": part[:1500]})
    return chunks or [{"heading": "正文", "content": text[:1500]}]

all_chunks = []
for d in docs:
    for c in chunk_by_heading(d["text"]):
        all_chunks.append({
            "doc_title": d["title"],
            "url": d["url"],
            "heading": c["heading"],
            "content": c["content"],
        })

print(f"总共 {len(all_chunks)} 个 chunk\n")

# ========== 第3步：TF-IDF 向量化 ==========
corpus = [c["content"] for c in all_chunks]
vectorizer = TfidfVectorizer(max_features=2000)
tfidf_matrix = vectorizer.fit_transform(corpus)

# ========== 第4步：检索函数 ==========
def search(query, top_k=3):
    q_vec = vectorizer.transform([query])
    scores = cosine_similarity(q_vec, tfidf_matrix)[0]
    top_idx = scores.argsort()[::-1][:top_k]
    return [(all_chunks[i], scores[i]) for i in top_idx if scores[i] > 0.05]

# ========== 第5步：交互问答 ==========
print("=" * 50)
print("RAG 问答就绪，输入问题（输入 q 退出）")
print("=" * 50)

while True:
    q = input("\n❓ 你的问题: ").strip()
    if q.lower() == "q":
        break

    results = search(q, top_k=3)

    has_evidence = len(results) > 0 and results[0][1] > 0.08
    version_keywords = ["版本", "新版", "旧版", "弃用", "deprecated", "ES5", "ES6", "ES202"]

    if has_evidence:
        top = results[0][0]
        answer = f"根据《{top['doc_title']}》中「{top['heading']}」的内容：\n{top['content'][:400]}..."
    else:
        answer = "未在文档中找到明确答案。"

    sources = [{"doc": r[0]["doc_title"], "url": r[0]["url"], "heading": r[0]["heading"], "score": round(float(r[1]), 3)} for r in results]

    uncertainties = []
    if not has_evidence:
        uncertainties.append("检索结果相关性低，以下来源仅供参考")
    if len(results) < 2:
        uncertainties.append("仅找到极少量相关内容，可能遗漏")

    needs_version_check = any(kw in q for kw in version_keywords) or any(kw in (results[0][0]["content"] if results else "") for kw in version_keywords)

    print(f"\n📋 answer: {answer}")
    print(f"📎 sources: {sources}")
    print(f"⚠️  uncertainties: {uncertainties if uncertainties else '无'}")
    print(f"🔢 needs_version_check: {needs_version_check}")
```

---

## 测试结果

### 测试 1：文档中存在的 API（alert）

> **问题**: alert 函数的作用是什么？

```json
{
  "answer": "根据《代码结构》中「我们将要学习的第一个内容就是构建代码块。」的内容：...语句之间可以使用分号进行分割...alert('Hello'); alert('World');...",
  "sources": [
    {"doc": "代码结构", "score": 0.467},
    {"doc": "基础运算符，数学运算", "score": 0.43},
    {"doc": "值的比较", "score": 0.252}
  ],
  "uncertainties": "无",
  "needs_version_check": false
}
```

⚠️ 最优来源《交互：alert、prompt 和 confirm》未进前三——TF-IDF 无语义理解，按词频匹配不够精准。

### 测试 2：文档中不存在的问题（React）

> **问题**: React 的 useEffect 怎么用？

```json
{
  "answer": "未在文档中找到明确答案。",
  "sources": [],
  "uncertainties": ["检索结果相关性低，以下来源仅供参考", "仅找到极少量相关内容，可能遗漏"],
  "needs_version_check": false
}
```

✅ 正确拒答。

### 测试 3：版本相关问题（ES6）

> **问题**: let 和 var 在 ES6 版本中有什么区别？

```json
{
  "answer": "根据《变量》中「大多数情况下，JavaScript 应用需要处理信息。」的内容：...变量就是用来储存这些信息的...使用 let 关键字...",
  "sources": [
    {"doc": "变量", "score": 0.327},
    {"doc": "基础运算符，数学运算", "score": 0.051}
  ],
  "uncertainties": "无",
  "needs_version_check": true
}
```

⚠️ 返回了 let 介绍但未覆盖 let vs var 对比；`uncertainties` 漏标了"文档中未找到 let 与 var 对比内容"。

---

## 测试分析

| 评估维度 | 测试 1 | 测试 2 | 测试 3 |
|------|:--:|:--:|:--:|
| 有证据时返回内容 | ✅ | — | ✅ |
| 无证据时拒答 | — | ✅ | — |
| sources 溯源到具体文档 | ✅ | ✅ | ✅ |
| uncertainties 标注缺失 | ❌ | ✅ | ❌ |
| needs_version_check 触发 | ✅ | ✅ | ✅ |

### 关键发现

1. **TF-IDF 的局限性暴露了**：测试 1 的 alert 问题，"交互：alert、prompt 和 confirm"那篇明明直接相关却排不进来——因为 TF-IDF 只看词频，不理解语义。真实场景应该用 embedding 模型（sentence-transformers）
2. **拒答逻辑有效**：测试 2 零匹配 → 系统正确拒答，没有编造
3. **uncertainties 是脚本逻辑缺陷**：当检索结果不够精准时（测试 1、3），脚本没有自动标注"可能存在更相关的未命中内容"——这是 RAG 系统常见盲区
4. **RAG 的核心教训**："RAG 不是把向量库接给模型就完了，而是一条把外部知识取回、筛选、引用、交给模型使用的证据链。任何一层做错，模型都会拿着错误材料说得很顺。"——测试 1 就是活例子

---

## 环境清理

### 虚拟环境删不删？

**建议留着**。只占 ~35MB，后续 Agent / MCP / Frameworks 实践大概率还要装 Python 包。

如果确实要删：
```cmd
# 先退出虚拟环境
deactivate
# 直接删文件夹
rmdir /s %USERPROFILE%\rag-practice
```

---

*AI x Web3 School Week 1 RAG 实践完成 — 由 Hermes AI（模型：deepseek-v4-pro）在 2026-05-23 生成*
