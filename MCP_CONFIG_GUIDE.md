# LuLab Convert MCP Server - 配置指南

## 🚀 快速开始 - 直接使用PyPI包

无需下载任何代码，直接使用PyPI上发布的包！

### 1. 安装包

```bash
# 使用 pip 安装
pip install lulab-convert-mcp-server

# 或使用 uv 安装 (推荐)
uv pip install lulab-convert-mcp-server
```

### 2. MCP 客户端配置

#### 方法 1: 使用 uvx (推荐)

**Claude Desktop 配置:**
```json
{
  "mcpServers": {
    "lulab-convert-mcp-server": {
      "command": "uvx",
      "args": [
        "--from",
        "lulab-convert-mcp-server",
        "lulab-convert-mcp-server"
      ],
      "env": {
        "MCP_TRANSPORT": "stdio"
      }
    }
  }
}
```

**Cline (VS Code扩展) 配置:**
```json
{
  "mcpServers": {
    "lulab-convert-mcp-server": {
      "command": "uvx",
      "args": [
        "--from",
        "lulab-convert-mcp-server",
        "lulab-convert-mcp-server"
      ],
      "env": {
        "MCP_TRANSPORT": "stdio"
      }
    }
  }
}
```

#### 方法 2: 直接命令 (需要先安装包)

```json
{
  "mcpServers": {
    "lulab-convert-mcp-server": {
      "command": "lulab-convert-mcp-server",
      "args": [],
      "env": {
        "MCP_TRANSPORT": "stdio"
      }
    }
  }
}
```

### 3. 配置文件位置

#### Claude Desktop
- **Windows**: `%APPDATA%\\Claude\\claude_desktop_config.json`
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

#### Cline (VS Code扩展)
在VS Code中打开设置，搜索"Cline MCP Settings"，然后添加上述配置。

### 4. 验证安装

重启Claude Desktop或VS Code，然后在对话中询问：
```
请列出可用的MCP工具
```

你应该能看到文档转换相关的工具列表。

## 🛠️ 可用工具

安装成功后，你将获得以下文档转换工具：

### 基础转换工具
- `convert_to_pdf` - 将DOCX转换为PDF
- `convert_to_txt` - 将DOCX转换为纯文本
- `convert_to_html` - 将DOCX转换为HTML
- `convert_to_markdown` - 将DOCX转换为Markdown
- `convert_to_rtf` - 将DOCX转换为RTF
- `convert_to_odt` - 将DOCX转换为ODT

### 高级转换工具
- `convert_html_to_markdown` - HTML转Markdown
- `convert_markdown_to_html` - Markdown转HTML
- `convert_html_to_pdf` - HTML转PDF
- `convert_markdown_to_pdf` - Markdown转PDF
- `convert_txt_to_docx` - 纯文本转DOCX
- `convert_html_to_docx` - HTML转DOCX
- `convert_markdown_to_docx` - Markdown转DOCX

### 文档操作工具
- `create_document` - 创建新的Word文档
- `add_heading` - 添加标题
- `add_paragraph` - 添加段落
- `add_table` - 添加表格
- `format_text` - 格式化文本
- 以及更多...

## 🔧 环境变量配置 (可选)

你可以通过环境变量自定义服务器行为：

```json
{
  "mcpServers": {
    "lulab-convert-mcp-server": {
      "command": "uvx",
      "args": [
        "lulab-convert-mcp-server"
      ],
      "env": {
        "MCP_TRANSPORT": "stdio",
        "MCP_DEBUG": "false",
        "MCP_HOST": "0.0.0.0",
        "MCP_PORT": "8000"
      }
    }
  }
}
```

## 📋 系统要求

- Python 3.8+
- 对于某些转换功能，可能需要安装LibreOffice

## 🆘 故障排除

### 1. 命令未找到
确保已正确安装包：
```bash
pip list | grep lulab-convert-mcp-server
```

### 2. 权限问题
在Windows上，可能需要以管理员身份运行：
```bash
pip install --user lulab-convert-mcp-server
```

### 3. 转换失败
某些转换功能需要LibreOffice，请确保已安装：
- Windows: 从官网下载安装
- macOS: `brew install --cask libreoffice`
- Linux: `sudo apt-get install libreoffice`

## 📚 更多信息

- **PyPI页面**: https://pypi.org/project/lulab-convert-mcp-server/
- **GitHub仓库**: https://github.com/your-repo/lulab-convert-mcp-server
- **问题反馈**: https://github.com/your-repo/lulab-convert-mcp-server/issues

## 🎉 开始使用

配置完成后，你就可以在Claude Desktop或Cline中使用强大的文档转换功能了！

示例对话：
```
用户: 请将这个Word文档转换为PDF格式
AI: 我来帮你转换文档。请提供Word文档的路径，我将使用convert_to_pdf工具为你转换。
```