"""
Extended document tools for Word Document Server.

These tools provide enhanced document content extraction and search capabilities.
"""
import os
import json
import subprocess
import platform
import shutil
from typing import Dict, List, Optional, Any, Union, Tuple
from docx import Document

from word_document_server.utils.file_utils import check_file_writeable, ensure_docx_extension
from word_document_server.utils.extended_document_utils import get_paragraph_text, find_text


async def get_paragraph_text_from_document(filename: str, paragraph_index: int) -> str:
    """Get text from a specific paragraph in a Word document.
    
    Args:
        filename: Path to the Word document
        paragraph_index: Index of the paragraph to retrieve (0-based)
    """
    filename = ensure_docx_extension(filename)
    
    if not os.path.exists(filename):
        return f"Document {filename} does not exist"
    

    if paragraph_index < 0:
        return "Invalid parameter: paragraph_index must be a non-negative integer"
    
    try:
        result = get_paragraph_text(filename, paragraph_index)
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Failed to get paragraph text: {str(e)}"


async def find_text_in_document(filename: str, text_to_find: str, match_case: bool = True, whole_word: bool = False) -> str:
    """Find occurrences of specific text in a Word document.
    
    Args:
        filename: Path to the Word document
        text_to_find: Text to search for in the document
        match_case: Whether to match case (True) or ignore case (False)
        whole_word: Whether to match whole words only (True) or substrings (False)
    """
    filename = ensure_docx_extension(filename)
    
    if not os.path.exists(filename):
        return f"Document {filename} does not exist"
    
    if not text_to_find:
        return "Search text cannot be empty"
    
    try:
        
        result = find_text(filename, text_to_find, match_case, whole_word)
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Failed to search for text: {str(e)}"


async def convert_to_pdf(filename: str, output_filename: Optional[str] = None) -> str:
    """Convert a Word document to PDF format.
    
    Args:
        filename: Path to the Word document
        output_filename: Optional path for the output PDF. If not provided, 
                         will use the same name with .pdf extension
    """
    filename = ensure_docx_extension(filename)
    
    if not os.path.exists(filename):
        return f"Document {filename} does not exist"
    
    # Generate output filename if not provided
    if not output_filename:
        base_name, _ = os.path.splitext(filename)
        output_filename = f"{base_name}.pdf"
    elif not output_filename.lower().endswith('.pdf'):
        output_filename = f"{output_filename}.pdf"
    
    # Convert to absolute path if not already
    if not os.path.isabs(output_filename):
        output_filename = os.path.abspath(output_filename)
    
    # Ensure the output directory exists
    output_dir = os.path.dirname(output_filename)
    if not output_dir:
        output_dir = os.path.abspath('.')
    
    # Create the directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Check if output file can be written
    is_writeable, error_message = check_file_writeable(output_filename)
    if not is_writeable:
        return f"Cannot create PDF: {error_message} (Path: {output_filename}, Dir: {output_dir})"
    
    try:
        # Determine platform for appropriate conversion method
        system = platform.system()
        
        if system == "Windows":
            # On Windows, try docx2pdf which uses Microsoft Word
            try:
                from docx2pdf import convert
                convert(filename, output_filename)
                return f"Document successfully converted to PDF: {output_filename}"
            except (ImportError, Exception) as e:
                return f"Failed to convert document to PDF: {str(e)}\nNote: docx2pdf requires Microsoft Word to be installed."
                
        elif system in ["Linux", "Darwin"]:  # Linux or macOS
            errors = []
            
            # --- Attempt 1: LibreOffice ---
            lo_commands = []
            if system == "Darwin":  # macOS
                lo_commands = ["soffice", "/Applications/LibreOffice.app/Contents/MacOS/soffice"]
            else:  # Linux
                lo_commands = ["libreoffice", "soffice"]

            for cmd_name in lo_commands:
                try:
                    output_dir_for_lo = os.path.dirname(output_filename) or '.'
                    os.makedirs(output_dir_for_lo, exist_ok=True)
                    
                    cmd = [cmd_name, '--headless', '--convert-to', 'pdf', '--outdir', output_dir_for_lo, filename]
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60, check=False)

                    if result.returncode == 0:
                        # LibreOffice typically creates a PDF with the same base name as the source file.
                        # e.g., 'mydoc.docx' -> 'mydoc.pdf'
                        base_name = os.path.splitext(os.path.basename(filename))[0]
                        created_pdf_name = f"{base_name}.pdf"
                        created_pdf_path = os.path.join(output_dir_for_lo, created_pdf_name)

                        # If the created file exists, move it to the desired output_filename if necessary.
                        if os.path.exists(created_pdf_path):
                            if created_pdf_path != output_filename:
                                shutil.move(created_pdf_path, output_filename)
                            
                            # Final check: does the target file now exist?
                            if os.path.exists(output_filename):
                                return f"Document successfully converted to PDF via {cmd_name}: {output_filename}"
                        
                        # If we get here, soffice returned 0 but the expected file wasn't created.
                        errors.append(f"{cmd_name} returned success code, but output file '{created_pdf_path}' was not found.")
                        # Continue to the next command or fallback.
                    else:
                        errors.append(f"{cmd_name} failed. Stderr: {result.stderr.strip()}")
                except FileNotFoundError:
                    errors.append(f"Command '{cmd_name}' not found.")
                except (subprocess.SubprocessError, Exception) as e:
                    errors.append(f"An error occurred with {cmd_name}: {str(e)}")
            
            # --- Attempt 2: docx2pdf (Fallback) ---
            try:
                from docx2pdf import convert
                convert(filename, output_filename)
                if os.path.exists(output_filename) and os.path.getsize(output_filename) > 0:
                    return f"Document successfully converted to PDF via docx2pdf: {output_filename}"
                else:
                    errors.append("docx2pdf fallback was executed but failed to create a valid output file.")
            except ImportError:
                errors.append("docx2pdf is not installed, skipping fallback.")
            except Exception as e:
                errors.append(f"docx2pdf fallback failed with an exception: {str(e)}")

            # --- If all attempts failed ---
            error_summary = "Failed to convert document to PDF using all available methods.\n"
            error_summary += "Recorded errors: " + "; ".join(errors) + "\n"
            error_summary += "To convert documents to PDF, please install either:\n"
            error_summary += "1. LibreOffice (recommended for Linux/macOS)\n"
            error_summary += "2. Microsoft Word (required for docx2pdf on Windows/macOS)"
            return error_summary
        else:
            return f"PDF conversion not supported on {system} platform"
            
    except Exception as e:
        return f"Failed to convert document to PDF: {str(e)}"

# --- New conversions ---
async def convert_to_txt(filename: str, output_filename: Optional[str] = None) -> str:
    filename = ensure_docx_extension(filename)
    if not os.path.exists(filename):
        return f"Document {filename} does not exist"

    if not output_filename:
        base_name, _ = os.path.splitext(filename)
        output_filename = f"{base_name}.txt"
    elif not output_filename.lower().endswith('.txt'):
        output_filename = f"{output_filename}.txt"

    if not os.path.isabs(output_filename):
        output_filename = os.path.abspath(output_filename)

    os.makedirs(os.path.dirname(output_filename) or os.path.abspath('.'), exist_ok=True)

    is_writeable, error_message = check_file_writeable(output_filename)
    if not is_writeable:
        return f"Cannot create TXT: {error_message} (Path: {output_filename})"

    try:
        from word_document_server.utils.document_utils import extract_document_text
        text = extract_document_text(filename)
        if isinstance(text, str) and text.startswith("Failed"):
            return text
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(text)
        return f"Document successfully converted to TXT: {output_filename}"
    except Exception as e:
        return f"Failed to convert document to TXT: {str(e)}"

async def convert_to_html(filename: str, output_filename: Optional[str] = None) -> str:
    filename = ensure_docx_extension(filename)
    if not os.path.exists(filename):
        return f"Document {filename} does not exist"

    if not output_filename:
        base_name, _ = os.path.splitext(filename)
        output_filename = f"{base_name}.html"
    elif not output_filename.lower().endswith('.html'):
        output_filename = f"{output_filename}.html"

    if not os.path.isabs(output_filename):
        output_filename = os.path.abspath(output_filename)

    os.makedirs(os.path.dirname(output_filename) or os.path.abspath('.'), exist_ok=True)

    is_writeable, error_message = check_file_writeable(output_filename)
    if not is_writeable:
        return f"Cannot create HTML: {error_message} (Path: {output_filename})"

    try:
        try:
            import mammoth  # type: ignore
        except ImportError:
            return "Failed to convert document to HTML: mammoth is not installed. Please install 'mammoth'."

        with open(filename, 'rb') as docx_file:
            result = mammoth.convert_to_html(docx_file)
            html = result.value
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(html)
        return f"Document successfully converted to HTML: {output_filename}"
    except Exception as e:
        return f"Failed to convert document to HTML: {str(e)}"

async def convert_to_markdown(filename: str, output_filename: Optional[str] = None) -> str:
    filename = ensure_docx_extension(filename)
    if not os.path.exists(filename):
        return f"Document {filename} does not exist"

    if not output_filename:
        base_name, _ = os.path.splitext(filename)
        output_filename = f"{base_name}.md"
    elif not output_filename.lower().endswith('.md'):
        output_filename = f"{output_filename}.md"

    if not os.path.isabs(output_filename):
        output_filename = os.path.abspath(output_filename)

    os.makedirs(os.path.dirname(output_filename) or os.path.abspath('.'), exist_ok=True)

    is_writeable, error_message = check_file_writeable(output_filename)
    if not is_writeable:
        return f"Cannot create Markdown: {error_message} (Path: {output_filename})"

    try:
        try:
            import mammoth  # type: ignore
        except ImportError:
            return "Failed to convert document to Markdown: mammoth is not installed. Please install 'mammoth'."
        try:
            from markdownify import markdownify as md  # type: ignore
        except ImportError:
            return "Failed to convert document to Markdown: markdownify is not installed. Please install 'markdownify'."

        with open(filename, 'rb') as docx_file:
            result = mammoth.convert_to_html(docx_file)
            html = result.value
        markdown = md(html)
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(markdown)
        return f"Document successfully converted to Markdown: {output_filename}"
    except Exception as e:
        return f"Failed to convert document to Markdown: {str(e)}"

async def convert_html_to_markdown(input_path: str, output_path: Optional[str] = None) -> str:
    if not os.path.exists(input_path):
        return f"Document {input_path} does not exist"
    if not output_path:
        base_name, _ = os.path.splitext(input_path)
        output_path = f"{base_name}.md"
    elif not output_path.lower().endswith('.md'):
        output_path = f"{output_path}.md"
    if not os.path.isabs(output_path):
        output_path = os.path.abspath(output_path)
    os.makedirs(os.path.dirname(output_path) or os.path.abspath('.'), exist_ok=True)
    is_writeable, error_message = check_file_writeable(output_path)
    if not is_writeable:
        return f"Cannot create Markdown: {error_message} (Path: {output_path})"
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            html = f.read()
        try:
            from markdownify import markdownify as md  # type: ignore
        except ImportError:
            return "Failed to convert HTML to Markdown: markdownify is not installed. Please install 'markdownify'."
        markdown = md(html)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown)
        return f"Document successfully converted to Markdown: {output_path}"
    except Exception as e:
        return f"Failed to convert HTML to Markdown: {str(e)}"

async def convert_markdown_to_html(input_path: str, output_path: Optional[str] = None) -> str:
    if not os.path.exists(input_path):
        return f"Document {input_path} does not exist"
    if not output_path:
        base_name, _ = os.path.splitext(input_path)
        output_path = f"{base_name}.html"
    elif not output_path.lower().endswith('.html'):
        output_path = f"{output_path}.html"
    if not os.path.isabs(output_path):
        output_path = os.path.abspath(output_path)
    os.makedirs(os.path.dirname(output_path) or os.path.abspath('.'), exist_ok=True)
    is_writeable, error_message = check_file_writeable(output_path)
    if not is_writeable:
        return f"Cannot create HTML: {error_message} (Path: {output_path})"
    try:
        try:
            import markdown  # type: ignore
        except ImportError:
            return "Failed to convert Markdown to HTML: markdown is not installed. Please install 'markdown'."
        with open(input_path, 'r', encoding='utf-8') as f:
            md_text = f.read()
        html = markdown.markdown(md_text, output_format='html5')
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        return f"Document successfully converted to HTML: {output_path}"
    except Exception as e:
        return f"Failed to convert Markdown to HTML: {str(e)}"

async def convert_html_to_pdf(input_path: str, output_path: Optional[str] = None) -> str:
    if not os.path.exists(input_path):
        return f"Document {input_path} does not exist"
    if not output_path:
        base_name, _ = os.path.splitext(input_path)
        output_path = f"{base_name}.pdf"
    elif not output_path.lower().endswith('.pdf'):
        output_path = f"{output_path}.pdf"
    if not os.path.isabs(output_path):
        output_path = os.path.abspath(output_path)
    output_dir = os.path.dirname(output_path) or os.path.abspath('.')
    os.makedirs(output_dir, exist_ok=True)
    is_writeable, error_message = check_file_writeable(output_path)
    if not is_writeable:
        return f"Cannot create PDF: {error_message} (Path: {output_path}, Dir: {output_dir})"
    try:
        system = platform.system()
        candidates = []
        if system == 'Windows':
            candidates = [
                'soffice',
                r'C:\\Program Files\\LibreOffice\\program\\soffice.exe',
                r'C:\\Program Files (x86)\\LibreOffice\\program\\soffice.exe'
            ]
        elif system == 'Darwin':
            candidates = ['soffice', '/Applications/LibreOffice.app/Contents/MacOS/soffice']
        else:
            candidates = ['libreoffice', 'soffice']
        errors = []
        for cmd_name in candidates:
            try:
                cmd = [cmd_name, '--headless', '--convert-to', 'pdf', '--outdir', output_dir, input_path]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=60, check=False)
                if result.returncode == 0:
                    base_name = os.path.splitext(os.path.basename(input_path))[0]
                    created_pdf_path = os.path.join(output_dir, f'{base_name}.pdf')
                    if os.path.exists(created_pdf_path):
                        if created_pdf_path != output_path:
                            shutil.move(created_pdf_path, output_path)
                        if os.path.exists(output_path):
                            return f"Document successfully converted to PDF via {cmd_name}: {output_path}"
                    errors.append(f"{cmd_name} returned success code, but output file '{created_pdf_path}' was not found.")
                else:
                    errors.append(f"{cmd_name} failed. Stderr: {result.stderr.strip()}")
            except FileNotFoundError:
                errors.append(f"Command '{cmd_name}' not found.")
            except Exception as e:
                errors.append(f"An error occurred with {cmd_name}: {str(e)}")
        error_summary = "Failed to convert HTML to PDF using LibreOffice. " + "; ".join(errors)
        return error_summary
    except Exception as e:
        return f"Failed to convert HTML to PDF: {str(e)}"

async def convert_markdown_to_pdf(input_path: str, output_path: Optional[str] = None) -> str:
    if not os.path.exists(input_path):
        return f"Document {input_path} does not exist"
    # Determine final PDF path
    if not output_path:
        base_name, _ = os.path.splitext(input_path)
        output_path = f"{base_name}.pdf"
    elif not output_path.lower().endswith('.pdf'):
        output_path = f"{output_path}.pdf"
    # Generate a temporary HTML path in the same directory
    tmp_html_path = os.path.join(os.path.dirname(output_path) or os.path.abspath('.'), '__tmp_md_to_html__.html')
    # First convert MD to HTML
    md_to_html_result = await convert_markdown_to_html(input_path, tmp_html_path)
    if not os.path.exists(tmp_html_path):
        return f"Failed to convert Markdown to HTML: {md_to_html_result}"
    # Then convert HTML to PDF
    html_to_pdf_result = await convert_html_to_pdf(tmp_html_path, output_path)
    try:
        if os.path.exists(tmp_html_path):
            os.remove(tmp_html_path)
    except Exception:
        pass
    return html_to_pdf_result
