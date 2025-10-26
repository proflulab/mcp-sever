import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
print("Loading configuration from .env file...")
load_dotenv()
# Set required environment variable for FastMCP 2.8.1+
os.environ.setdefault('FASTMCP_LOG_LEVEL', 'INFO')
from fastmcp import FastMCP
from word_document_server.tools import extended_document_tools
from word_document_server.tools.content_tools import replace_paragraph_block_below_header_tool
from word_document_server.tools.content_tools import replace_block_between_manual_anchors_tool

def get_transport_config():
    # Default configuration
    config = {
        'transport': 'stdio',  # Default to stdio for backward compatibility
        'host': '0.0.0.0',
        'port': 8000,
        'path': '/mcp',
        'sse_path': '/sse',
        'debug': False,
    }
    
    # Override with environment variables if provided
    transport = os.getenv('MCP_TRANSPORT', 'stdio').lower()
    print(f"Transport: {transport}")
    # Validate transport type
    valid_transports = ['stdio', 'streamable-http', 'sse']
    if transport not in valid_transports:
        print(f"Warning: Invalid transport '{transport}'. Falling back to 'stdio'.")
        transport = 'stdio'
    
    config['transport'] = transport
    config['host'] = os.getenv('MCP_HOST', config['host'])
    # Use PORT from Render if available, otherwise fall back to MCP_PORT or default
    config['port'] = int(os.getenv('PORT', os.getenv('MCP_PORT', config['port'])))
    config['path'] = os.getenv('MCP_PATH', config['path'])
    config['sse_path'] = os.getenv('MCP_SSE_PATH', config['sse_path'])
    
    # Debug flag
    debug_env = os.getenv('MCP_DEBUG', '').strip().lower()
    config['debug'] = debug_env in ('1', 'true', 'yes', 'on')
    
    return config


def setup_logging(debug_mode):

    import logging
    
    if debug_mode:
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        print("Debug logging enabled")
    else:
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )


# Initialize FastMCP server
mcp = FastMCP("Word Document Server")


def register_tools():
    """Register only conversion tools with the MCP server."""
    @mcp.tool()
    def convert_to_pdf(filename: str, output_filename: str = None):
        return extended_document_tools.convert_to_pdf(filename, output_filename)

    @mcp.tool()
    def convert_to_txt(filename: str, output_filename: str = None):
        """Convert a Word document to plain text (.txt)."""
        return extended_document_tools.convert_to_txt(filename, output_filename)

    @mcp.tool()
    def convert_to_html(filename: str, output_filename: str = None):
        """Convert a Word document to HTML (.html)."""
        return extended_document_tools.convert_to_html(filename, output_filename)

    @mcp.tool()
    def convert_to_markdown(filename: str, output_filename: str = None):
        """Convert a Word document to Markdown (.md)."""
        return extended_document_tools.convert_to_markdown(filename, output_filename)

    @mcp.tool()
    def convert_html_to_markdown(input_path: str, output_path: str = None):
        """Convert an HTML document to Markdown (.md)."""
        return extended_document_tools.convert_html_to_markdown(input_path, output_path)

    @mcp.tool()
    def convert_markdown_to_html(input_path: str, output_path: str = None):
        """Convert a Markdown document to HTML (.html)."""
        return extended_document_tools.convert_markdown_to_html(input_path, output_path)

    @mcp.tool()
    def convert_html_to_pdf(input_path: str, output_path: str = None):
        """Convert an HTML document to PDF (.pdf) using LibreOffice."""
        return extended_document_tools.convert_html_to_pdf(input_path, output_path)

    @mcp.tool()
    def convert_markdown_to_pdf(input_path: str, output_path: str = None):
        """Convert a Markdown document to PDF (.pdf) via HTML."""
        return extended_document_tools.convert_markdown_to_pdf(input_path, output_path)

    @mcp.tool()
    def convert_to_rtf(filename: str, output_filename: str = None):
        """Convert a Word document to RTF (.rtf)."""
        return extended_document_tools.convert_to_rtf(filename, output_filename)

    @mcp.tool()
    def convert_to_odt(filename: str, output_filename: str = None):
        """Convert a Word document to ODT (.odt)."""
        return extended_document_tools.convert_to_odt(filename, output_filename)

    @mcp.tool()
    def convert_html_to_docx(input_path: str, output_path: str = None):
        """Convert an HTML document to DOCX (.docx)."""
        return extended_document_tools.convert_html_to_docx(input_path, output_path)

    @mcp.tool()
    def convert_markdown_to_docx(input_path: str, output_path: str = None):
        """Convert a Markdown document to DOCX (.docx)."""
        return extended_document_tools.convert_markdown_to_docx(input_path, output_path)

    @mcp.tool()
    def convert_txt_to_docx(input_path: str, output_path: str = None):
        """Convert a TXT document to DOCX (.docx)."""
        return extended_document_tools.convert_txt_to_docx(input_path, output_path)

    @mcp.tool()
    def convert_odt_to_docx(input_path: str, output_path: str = None):
        """Convert an ODT document to DOCX (.docx)."""
        return extended_document_tools.convert_odt_to_docx(input_path, output_path)

    @mcp.tool()
    def convert_rtf_to_docx(input_path: str, output_path: str = None):
        """Convert an RTF document to DOCX (.docx)."""
        return extended_document_tools.convert_rtf_to_docx(input_path, output_path)

    @mcp.tool()
    async def convert_doc_to_docx(input_path: str, output_path: Optional[str] = None) -> str:
        return await extended_document_tools.convert_doc_to_docx(input_path, output_path)

    @mcp.tool()
    async def convert_to_doc(filename: str, output_filename: Optional[str] = None) -> str:
        return await extended_document_tools.convert_to_doc(filename, output_filename)

    @mcp.tool()
    async def convert_txt_to_pdf(input_path: str, output_path: Optional[str] = None) -> str:
        return await extended_document_tools.convert_txt_to_pdf(input_path, output_path)

    @mcp.tool()
    async def convert_odt_to_pdf(input_path: str, output_path: Optional[str] = None) -> str:
        return await extended_document_tools.convert_odt_to_pdf(input_path, output_path)

    @mcp.tool()
    async def convert_rtf_to_pdf(input_path: str, output_path: Optional[str] = None) -> str:
        return await extended_document_tools.convert_rtf_to_pdf(input_path, output_path)

    @mcp.tool()
    async def convert_doc_to_pdf(input_path: str, output_path: Optional[str] = None) -> str:
        return await extended_document_tools.convert_doc_to_pdf(input_path, output_path)

    @mcp.tool()
    def replace_paragraph_block_below_header(filename: str, header_text: str, new_paragraphs: list, detect_block_end_fn=None):
        """Reemplaza el bloque de párrafos debajo de un encabezado, evitando modificar TOC."""
        return replace_paragraph_block_below_header_tool(filename, header_text, new_paragraphs, detect_block_end_fn)

    @mcp.tool()
    def replace_block_between_manual_anchors(filename: str, start_anchor_text: str, new_paragraphs: list, end_anchor_text: str = None, match_fn=None, new_paragraph_style: str = None):
        """Replace all content between start_anchor_text and end_anchor_text (or next logical header if not provided)."""
        return replace_block_between_manual_anchors_tool(filename, start_anchor_text, new_paragraphs, end_anchor_text, match_fn, new_paragraph_style)

    # Comment tools
    @mcp.tool()
    def get_all_comments(filename: str):
        """Extract all comments from a Word document."""
        return comment_tools.get_all_comments(filename)
    
    @mcp.tool()
    def get_comments_by_author(filename: str, author: str):
        """Extract comments from a specific author in a Word document."""
        return comment_tools.get_comments_by_author(filename, author)
    
    @mcp.tool()
    def get_comments_for_paragraph(filename: str, paragraph_index: int):
        """Extract comments for a specific paragraph in a Word document."""
        return comment_tools.get_comments_for_paragraph(filename, paragraph_index)
    # New table column width tools
    @mcp.tool()
    def set_table_column_width(filename: str, table_index: int, col_index: int, 
                              width: float, width_type: str = "points"):
        """Set the width of a specific table column."""
        return format_tools.set_table_column_width(filename, table_index, col_index, width, width_type)

    @mcp.tool()
    def set_table_column_widths(filename: str, table_index: int, widths: list, 
                               width_type: str = "points"):
        """Set the widths of multiple table columns."""
        return format_tools.set_table_column_widths(filename, table_index, widths, width_type)

    @mcp.tool()
    def set_table_width(filename: str, table_index: int, width: float, 
                       width_type: str = "points"):
        """Set the overall width of a table."""
        return format_tools.set_table_width(filename, table_index, width, width_type)

    @mcp.tool()
    def auto_fit_table_columns(filename: str, table_index: int):
        """Set table columns to auto-fit based on content."""
        return format_tools.auto_fit_table_columns(filename, table_index)

    # New table cell text formatting and padding tools
    @mcp.tool()
    def format_table_cell_text(filename: str, table_index: int, row_index: int, col_index: int,
                               text_content: str = None, bold: bool = None, italic: bool = None,
                               underline: bool = None, color: str = None, font_size: int = None,
                               font_name: str = None):
        """Format text within a specific table cell."""
        return format_tools.format_table_cell_text(filename, table_index, row_index, col_index,
                                                   text_content, bold, italic, underline, color, font_size, font_name)

    @mcp.tool()
    def set_table_cell_padding(filename: str, table_index: int, row_index: int, col_index: int,
                               top: float = None, bottom: float = None, left: float = None, 
                               right: float = None, unit: str = "points"):
        """Set padding/margins for a specific table cell."""
        return format_tools.set_table_cell_padding(filename, table_index, row_index, col_index,
                                                   top, bottom, left, right, unit)



def run_server():
    """Run the Word Document MCP Server with configurable transport."""
    # Get transport configuration
    config = get_transport_config()
    
    # Setup logging
    # setup_logging(config['debug'])
    
    # Register all tools
    register_tools()
    
    # Print startup information
    transport_type = config['transport']
    print(f"Starting Word Document MCP Server with {transport_type} transport...")
    
    # if config['debug']:
    #     print(f"Configuration: {config}")
    
    try:
        if transport_type == 'stdio':
            # Run with stdio transport (default, backward compatible)
            print("Server running on stdio transport")
            mcp.run(transport='stdio')
            
        elif transport_type == 'streamable-http':
            # Run with streamable HTTP transport
            print(f"Server running on streamable-http transport at http://{config['host']}:{config['port']}{config['path']}")
            mcp.run(
                transport='streamable-http',
                host=config['host'],
                port=config['port'],
                path=config['path']
            )
            
        elif transport_type == 'sse':
            # Run with SSE transport
            print(f"Server running on SSE transport at http://{config['host']}:{config['port']}{config['sse_path']}")
            mcp.run(
                transport='sse',
                host=config['host'],
                port=config['port'],
                path=config['sse_path']
            )
            
    except KeyboardInterrupt:
        print("\nShutting down server...")
    except Exception as e:
        print(f"Error starting server: {e}")
        if config['debug']:
            import traceback
            traceback.print_exc()
        sys.exit(1)
    
    return mcp


def main():
    """Main entry point for the server."""
    run_server()


if __name__ == "__main__":
    main()
