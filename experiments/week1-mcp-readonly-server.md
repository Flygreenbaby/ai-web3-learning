# AI × Web3 School — 实践：只读 MCP Server 安全设计与实现

**对应课程**: [模型上下文协议（MCP）](https://aiweb3.school/zh/handbook/ai/mcp/)
**实践日期**: 2026-05-29
**实践人**: Flygreenbaby (学号 4348)

---

## 🎯 实践目标

设计并实现一个**只读**的 MCP (Model Context Protocol) Server，提供文档搜索和读取功能。
重点实现工程级的安全防护：目录白名单、来源路径标记、审计日志和明确的错误处理。

---

## 🛡️ 第一部分：核心安全架构

为了防止 LLM 通过 MCP 工具进行路径穿越攻击（Path Traversal）或读取敏感文件（如 `.env`, `~/.ssh/id_rsa`），本 Server 实施以下硬性安全策略：

### 1. 目录白名单 (Directory Whitelist)
- 所有请求的路径必须位于预设的 `BASE_DIR`（如 `/opt/data/ai-web3-learning/notes`）内。
- **实现逻辑**：使用 `os.path.realpath` 解析绝对路径后，检查是否以 `BASE_DIR` 开头。拒绝任何包含 `..` 或符号链接越界的请求。

### 2. 来源路径标记 (Source Attribution)
- 返回的内容必须附带其物理来源路径，防止 LLM 产生幻觉或混淆不同文件的内容。
- **返回格式**：`{"source": "/absolute/path/to/file.md", "content": "..."}`

### 3. 审计日志 (Audit Logging)
- 记录所有工具调用，格式为 JSON Lines，追加至 `mcp_audit.log`。
- **日志字段**：`timestamp`, `tool_name`, `parameters`, `client_ip`, `status` (success/denied/error)。

### 4. 明确错误返回 (Explicit Errors)
- 不使用模糊的 "Internal Error"，而是返回标准 JSON-RPC 错误码：
  - `-32602 Invalid params`: 路径格式错误。
  - `-32003 Access denied`: 尝试访问白名单外路径。
  - `-32004 Not found`: 文件不存在。

---

## 🔧 第二部分：工具 Schema 设计

### 工具 1: `search_docs`
全文搜索白名单目录下的 Markdown 文件。

```json
{
  "name": "search_docs",
  "description": "在笔记目录中全文搜索关键词，返回匹配的文件路径和相关上下文。",
  "inputSchema": {
    "type": "object",
    "properties": {
      "query": {
        "type": "string",
        "description": "搜索关键词或正则表达式"
      },
      "file_glob": {
        "type": "string",
        "description": "可选的文件名过滤，如 '*.md'"
      }
    },
    "required": ["query"]
  }
}
```

### 工具 2: `get_file`
读取指定路径的文件内容（带长度限制）。

```json
{
  "name": "get_file",
  "description": "读取白名单目录内指定文件的内容。",
  "inputSchema": {
    "type": "object",
    "properties": {
      "path": {
        "type": "string",
        "description": "相对于 BASE_DIR 的路径或绝对路径"
      },
      "offset": {
        "type": "integer",
        "description": "起始行号 (1-indexed)",
        "default": 1
      },
      "limit": {
        "type": "integer",
        "description": "最大读取行数",
        "default": 100
      }
    },
    "required": ["path"]
  }
}
```

---

## 💻 第三部分：核心代码实现逻辑 (Python)

```python
import os
import logging
from pathlib import Path

BASE_DIR = Path("/opt/data/ai-web3-learning/notes").resolve()
logging.basicConfig(filename="mcp_audit.log", level=logging.INFO)

def _check_path(requested_path: str) -> Path:
    """白名单校验核心逻辑"""
    target = Path(requested_path).resolve()
    # 防止路径穿越
    if not str(target).startswith(str(BASE_DIR)):
        logging.warning(f"Access denied: {requested_path}")
        raise PermissionError(f"Path outside whitelist: {requested_path}")
    if not target.exists():
        raise FileNotFoundError(f"File not found: {requested_path}")
    return target

def get_file(path: str, offset: int = 1, limit: int = 100) -> dict:
    try:
        safe_path = _check_path(path)
        logging.info(f"get_file success: {safe_path}")
        
        with open(safe_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()[offset-1 : offset-1+limit]
            
        return {
            "source": str(safe_path),
            "content": "".join(lines),
            "total_lines": len(lines)
        }
    except PermissionError as e:
        return {"error": "Access denied", "details": str(e), "code": -32003}
    except FileNotFoundError as e:
        return {"error": "Not found", "details": str(e), "code": -32004}
```

---

## 🚀 第四部分：权限升级方案 (Challenge)

**场景**：未来需要增加一个 `write_doc` 工具，允许 LLM 修改笔记。如何设计安全的权限确认方案？

### 方案设计：基于 HMAC + 带外确认 (Out-of-Band Confirmation)

1. **临时 Token 生成**：
   当 LLM 调用 `write_doc(path, content)` 时，Server **不直接写入**，而是计算内容的 SHA256 哈希，生成一个一次性 Token，并将请求挂起。
   
2. **带外通知**：
   Server 通过 Telegram Bot 向管理员（用户）发送确认请求：
   > ⚠️ **MCP 写入请求**
   > 文件: `notes/week1/day1.md`
   > 变更: 新增 15 行
   > 哈希: `a1b2...c3d4`
   > [批准] [拒绝]

3. **执行与审计**：
   - 用户点击 [批准] 后，Server 验证 Token 并执行写入。
   - 写入操作被记录在 `mcp_audit.log` 中，标记为 `status: approved_write`。
   - 同时自动执行 `git commit`，确保所有 AI 的修改都有版本控制记录，可随时回滚。

---

## ✅ 完成标准

- [x] 设计只读 MCP Server 架构
- [x] 定义 2 个只读工具 (search_docs, get_file) 的 JSON Schema
- [x] 实现目录白名单校验逻辑 (防止 `../` 越狱)
- [x] 设计审计日志格式和错误返回机制
- [x] 提出权限升级方案 (带外确认 + Git 版本控制)
- [x] 记录保存至 experiments/

---

*AI x Web3 School Week 1 - MCP 实践完成 — 由 Hermes AI（模型：qwen3.7-max-preview）在 2026-05-29 生成*
