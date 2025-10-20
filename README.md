# Office Word MCP Server

一个用于在 MCP 环境中进行 Word 文档转换的服务器，支持将 DOCX 转换为多种格式。

## 功能特性
- DOCX → PDF（使用 `docx2pdf` 或 LibreOffice）
- DOCX → TXT（提取纯文本）
- DOCX → HTML（使用 `mammoth` 进行语义化 HTML 转换）
- DOCX → Markdown（先转 HTML，再用 `markdownify` 转为 Markdown）
- HTML ↔ Markdown（`markdownify`、`markdown`）
- HTML → PDF（通过 LibreOffice `soffice --convert-to pdf`）
- Markdown → PDF（先转 HTML，再用 LibreOffice 转 PDF）

## 安装依赖
确保已经安装 Python 3.10+。常用依赖如下（如果你的环境尚未安装）：

```
pip install docx2pdf mammoth markdownify markdown python-docx msoffcrypto-tool python-dotenv fastmcp
```

Windows 上如需使用 LibreOffice 作为备选转换器，请先安装 LibreOffice 并将其加入系统 PATH（或位于默认路径，如 `C:\Program Files\LibreOffice\program\soffice.exe`）。

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
- `input_path` 为输入文件的绝对路径。
- `output_path` 可选；不提供时将自动生成与输入同名的目标文件（扩展名分别为 `.pdf`/`.txt`/`.html`/`.md`）。

## 代码中调用示例
如果你希望直接在 Python 中调用（无需 MCP 客户端），可以参考：

```python
import asyncio
from word_document_server.tools.extended_document_tools import (
    convert_to_pdf,
    convert_to_txt,
    convert_to_html,
    convert_to_markdown,
    convert_html_to_markdown,
    convert_markdown_to_html,
    convert_html_to_pdf,
    convert_markdown_to_pdf,
)

async def main():
    src_docx = r"e:\\Office-Word-MCP-Server-main\\Lulab_优秀学员_Yang_Jinze.docx"
    src_html = r"e:\\Office-Word-MCP-Server-main\\Lulab_优秀学员_Yang_Jinze.html"
    src_md = r"e:\\Office-Word-MCP-Server-main\\Lulab_优秀学员_Yang_Jinze.md"
    await convert_to_pdf(src_docx)
    await convert_to_txt(src_docx)
    await convert_to_html(src_docx)
    await convert_to_markdown(src_docx)
    await convert_html_to_markdown(src_html)
    await convert_markdown_to_html(src_md)
    await convert_html_to_pdf(src_html)
    await convert_markdown_to_pdf(src_md)

asyncio.run(main())
```

## 备注
- 进行 PDF 转换时，若系统未安装 LibreOffice，`HTML→PDF` 与 `Markdown→PDF` 会提示安装需求。
- 部分受保护/加密的文档可能需要额外处理；工具会尽力提取文本并给出错误信息。
- 转换结果质量依赖源文档结构与样式；HTML/Markdown 转换倾向保持语义结构而非原始布局。