#!/usr/bin/env python3
"""
启动脚本：运行 DocumentAssistant MCP 服务器
支持本地项目和 GitHub 安装两种方式
"""
import subprocess
import sys
import os
from pathlib import Path

def try_github_install():
    """尝试从 GitHub 安装 DocumentAssistant"""
    try:
        print("🔄 尝试从 GitHub 安装 DocumentAssistant...")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", 
            "--quiet", "--force-reinstall",
            "git+https://github.com/proflulab/DocumentAssistant.git"
        ], timeout=30)
        print("✅ GitHub 安装成功")
        return True
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        print(f"⚠️  GitHub 安装失败: {e}")
        return False

def try_local_install():
    """尝试使用本地项目"""
    local_path = Path(__file__).parent / "DocumentAssistant"
    if local_path.exists():
        try:
            print(f"🔄 使用本地项目: {local_path}")
            # 添加本地项目到 Python 路径
            sys.path.insert(0, str(local_path / "src"))
            
            # 尝试安装本地项目的依赖
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", 
                "--quiet", "-e", str(local_path)
            ])
            print("✅ 本地项目配置成功")
            return True
        except subprocess.CalledProcessError as e:
            print(f"⚠️  本地项目配置失败: {e}")
            # 即使安装失败，也尝试直接导入
            sys.path.insert(0, str(local_path / "src"))
            return True
    return False

def run_server():
    """运行 MCP 服务器"""
    try:
        from document_assistant.server import create_server
        
        print("🚀 启动 DocumentAssistant MCP 服务器...")
        
        # 使用 Smithery 的方式启动 MCP 服务器
        server = create_server()
        
        # 检查是否有 stdio 运行方法
        if hasattr(server, 'run_stdio'):
            server.run_stdio()
        elif hasattr(server, 'run'):
            server.run()
        else:
            # 使用标准的 MCP stdio 运行方式
            import mcp.server.stdio
            if hasattr(mcp.server.stdio, 'run_server'):
                mcp.server.stdio.run_server(server)
            else:
                # 尝试新的 MCP API
                from mcp.server import Server
                from mcp.server.stdio import stdio_server
                
                async def main():
                    async with stdio_server() as (read_stream, write_stream):
                        await server.run(read_stream, write_stream)
                
                import asyncio
                asyncio.run(main())
                
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        print("请确保已正确安装 DocumentAssistant 或本地项目可用")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 服务器启动失败: {e}")
        print(f"错误详情: {type(e).__name__}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # 设置环境变量
    os.environ["MCP_TRANSPORT"] = "stdio"
    
    print("📦 DocumentAssistant MCP 服务器启动器")
    print("🔗 GitHub 仓库: https://github.com/proflulab/DocumentAssistant.git")
    
    # 优先尝试 GitHub 安装，失败则使用本地项目
    success = try_github_install()
    if not success:
        print("🔄 GitHub 不可用，尝试使用本地项目...")
        success = try_local_install()
    
    if success:
        run_server()
    else:
        print("❌ 无法启动服务器：GitHub 和本地项目都不可用")
        sys.exit(1)