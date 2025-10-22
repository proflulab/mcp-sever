# LuLab Convert MCP Server

一个用于在 MCP 环境中进行 Word 文档转换的服务器，支持将 DOCX 转换为多种格式。

**🚀 现已支持所有兼容MCP协议的AI客户端！**

支持的AI客户端包括但不限于：
- Claude Desktop
- Cline (VS Code扩展)
- 其他支持MCP协议的AI工具

## 快速开始



### 使用方法：本地使用
1. 克隆或下载此项目
2. 安装依赖：`pip install -r requirements.txt`
3. 在您的AI客户端配置文件中添加MCP服务器配置（参考下方json配置示例）

## 功能特性
- DOCX → PDF（使用 `docx2pdf` 或 LibreOffice）
- DOCX → TXT（提取纯文本）
- DOCX → HTML（使用 `mammoth` 进行语义化 HTML 转换）
- DOCX → Markdown（先转 HTML，再用 `markdownify` 转为 Markdown）
- HTML ↔ Markdown（`markdownify`、`markdown`）
- HTML → PDF（通过 LibreOffice `soffice --convert-to pdf`）
- Markdown → PDF（先转 HTML，再用 LibreOffice 转 PDF）




### 客户端配置示例：Claude Desktop
在Claude Desktop配置文件中添加：
```json
{
  "mcpServers": {
    "word-document-server": {
      "command": "python",
      "args": [
        "-m",
        "word_document_server.main"
      ],
      "env": {
        "PYTHONPATH": "/path/to/your/Office-Word-MCP-Server",
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
- `convert_html_to_markdown(input_path, output_path=None)`
- `convert_markdown_to_html(input_path, output_path=None)`
- `convert_html_to_pdf(input_path, output_path=None)`
- `convert_markdown_to_pdf(input_path, output_path=None)`

说明：
- `input_path` 为输入文件的绝对路径。（如e:\\mcp-sever）
- `output_path` 可选；不提供时将自动生成与输入同名的目标文件（扩展名分别为 `.pdf`/`.txt`/`.html`/`.md`）。



## 备注
- 进行 PDF 转换时，若系统未安装 LibreOffice，`HTML→PDF` 与 `Markdown→PDF` 会提示安装需求。
- 部分受保护/加密的文档可能需要额外处理；工具会尽力提取文本并给出错误信息。
- 转换结果质量依赖源文档结构与样式；HTML/Markdown 转换倾向保持语义结构而非原始布局。