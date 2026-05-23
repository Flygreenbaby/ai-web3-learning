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
            # 取第一行作标题
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

    # 判断是否有足够证据
    has_evidence = len(results) > 0 and results[0][1] > 0.08
    version_keywords = ["版本", "新版", "旧版", "弃用", "deprecated", "ES5", "ES6", "ES202"]

    # 四字段输出
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
