import asyncio
import os
import sys
# Ensure project root is on sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from word_document_server.tools.extended_document_tools import (
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
    print("Starting conversions for DOCX:", src_docx)
    await convert_to_txt(src_docx)
    print("TXT conversion done")
    await convert_to_html(src_docx)
    print("HTML conversion done")
    await convert_to_markdown(src_docx)
    print("Markdown conversion done")

    print("Converting HTML to Markdown:", src_html)
    await convert_html_to_markdown(src_html)
    print("HTML→Markdown done")

    print("Converting Markdown to HTML:", src_md)
    await convert_markdown_to_html(src_md)
    print("Markdown→HTML done")

    print("Converting HTML to PDF:", src_html)
    try:
        await convert_html_to_pdf(src_html)
        print("HTML→PDF done")
    except Exception as e:
        print("HTML→PDF failed:", e)

    print("Converting Markdown to PDF:", src_md)
    try:
        await convert_markdown_to_pdf(src_md)
        print("Markdown→PDF done")
    except Exception as e:
        print("Markdown→PDF failed:", e)

if __name__ == "__main__":
    asyncio.run(main())