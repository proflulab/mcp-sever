# LuLab Convert MCP Server

一个用于在 MCP 环境中进行 Word 文档转换的服务器，支持将 DOCX 转换为多种格式。

**🚀 现已支持所有兼容MCP协议的AI客户端！**

支持的AI客户端包括但不限于：
- Claude Desktop
- Cline (VS Code扩展)
- 其他支持MCP协议的AI工具

## 📦 安装方式

### 方法 1: 从 PyPI 安装 (推荐)

**最简单的方式！无需克隆代码库**

```bash
# 使用 pip 安装
pip install lulab-convert-mcp-server

# 或使用 uv 安装
uv pip install lulab-convert-mcp-server
```

**MCP 客户端配置 (Claude Desktop):**
```json
{
  "mcpServers": {
    "lulab-convert-mcp-server": {
      "command": "uvx",
      "args": [
        "lulab-convert-mcp-server"
      ],
      "env": {
        "MCP_TRANSPORT": "stdio"
      }
    }
  }
}
```

📖 **详细的 PyPI 使用指南**: 请查看 [PYPI_USAGE.md](./PYPI_USAGE.md)

### 方法 2: 本地开发安装
1. 克隆或下载此项目
2. 安装依赖：`pip install -r requirements.txt`
3. 在您的AI客户端配置文件中添加MCP服务器配置（参考下方json配置示例）

## 功能特性
- DOCX → PDF（使用 `docx2pdf` 或 LibreOffice）
- DOCX → TXT（提取纯文本）
- DOCX → HTML（使用 `mammoth` 进行语义化 HTML 转换）
- DOCX → Markdown（先转 HTML，再用 `markdownify` 转为 Markdown）
- DOCX → RTF（通过 LibreOffice 转换）
- DOCX → ODT（通过 LibreOffice 转换）
- DOCX → DOC（通过 LibreOffice 转换）
- DOC → DOCX（通过 LibreOffice 转换）
- TXT/ODT/RTF/DOC → PDF（通过 LibreOffice 转换）
- HTML ↔ Markdown（`markdownify`、`markdown`）
- HTML → PDF（通过 LibreOffice `soffice --convert-to pdf`）
- HTML → DOCX（通过 LibreOffice 转换）
- Markdown → PDF（先转 HTML，再用 LibreOffice 转 PDF）
- Markdown → DOCX（先转 HTML，再用 LibreOffice；无LibreOffice时回退为简易解析）
- TXT → DOCX（使用 `python-docx` 生成文档）
- ODT/RTF → DOCX（通过 LibreOffice 转换）



### 客户端配置示例：Claude Desktop
在Claude Desktop配置文件中添加：
```json
{
  "mcpServers": {
    "office-word-mcp-server": {
      "command": "python",
      "args": [
        "-m",
        "word_document_server.main"
      ],
      "env": {
        "PYTHONPATH": "e\\mcp-sever",
        "MCP_TRANSPORT": "stdio"
      }
    }
  }
}

```



## MCP 工具列表
- `convert_to_pdf(input_path, output_path=None)`
- `convert_to_txt(input_path, output_path=None)`
- `convert_to_html(input_path, output_path=None)`
- `convert_to_markdown(input_path, output_path=None)`
- `convert_to_rtf(input_path, output_path=None)`
- `convert_to_odt(input_path, output_path=None)`
- `convert_to_doc(input_path, output_path=None)`
- `convert_doc_to_docx(input_path, output_path=None)`
- `convert_html_to_markdown(input_path, output_path=None)`
- `convert_markdown_to_html(input_path, output_path=None)`
- `convert_html_to_pdf(input_path, output_path=None)`
- `convert_markdown_to_pdf(input_path, output_path=None)`
- `convert_txt_to_pdf(input_path, output_path=None)`
- `convert_odt_to_pdf(input_path, output_path=None)`
- `convert_rtf_to_pdf(input_path, output_path=None)`
- `convert_html_to_docx(input_path, output_path=None)`
- `convert_markdown_to_docx(input_path, output_path=None)`
- `convert_txt_to_docx(input_path, output_path=None)`
- `convert_odt_to_docx(input_path, output_path=None)`
- `convert_rtf_to_docx(input_path, output_path=None)`

说明：
- `input_path` 为输入文件的绝对路径。（如 `e\\mcp-sever\\docs\\sample.docx`）
- `output_path` 可选；不提供时将自动生成与输入同名的目标文件（扩展名分别为 `.pdf`/`.txt`/`.html`/`.md`/`.rtf`/`.odt`/`.doc`/`.docx`）。
- Windows/macOS/Linux：若需要 `rtf`/`odt`/`doc` 或 `html/md/txt → docx/pdf` 功能，请安装 LibreOffice；否则部分功能将降级或返回安装提示。

使用提示：
- `convert_to_doc(input_path)` 将 DOCX 转为旧版 `.doc` 格式，建议仅在兼容旧系统时使用。
- `convert_doc_to_docx(input_path)` 将 `.doc` 升级为现代 `.docx`，便于后续处理与版本控制。
- `convert_*_to_pdf(input_path)` 系列统一通过 LibreOffice 生成 PDF，输出路径不提供时默认与输入同目录。

## 备注
- 进行 PDF 转换时，若系统未安装 LibreOffice，`HTML→PDF` 与 `Markdown→PDF` 会提示安装需求。
- 部分受保护/加密的文档可能需要额外处理；工具会尽力提取文本并给出错误信息。
- 转换结果质量依赖源文档结构与样式；HTML/Markdown 转换倾向保持语义结构而非原始布局。