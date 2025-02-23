import os
import platform
import logging
import shutil

logger = logging.getLogger(__name__)

def find_soffice():
    """查找 LibreOffice 可执行文件的路径"""
    if platform.system() == "Windows":
        # Windows 下可能的安装路径
        possible_paths = [
            r"C:\Program Files\LibreOffice\program\soffice.exe",
            r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
            r"C:\Program Files (x86)\OpenOffice\program\soffice.exe",
            r"C:\Program Files\OpenOffice\program\soffice.exe",
        ]
        for path in possible_paths:
            if os.path.exists(path):
                return path
    else:
        # Linux/Unix 系统
        possible_commands = ['soffice', 'libreoffice']
        for cmd in possible_commands:
            path = shutil.which(cmd)
            if path:
                return path
    return None

# 根据操作系统动态导入依赖
try:
    from docx import Document
except ImportError:
    logger.warning("python-docx not installed. Word conversion features will be limited.")
    Document = None

if platform.system() == "Windows":
    try:
        from docx2pdf import convert as docx2pdf_convert
    except ImportError:
        logger.warning("docx2pdf not installed. PDF conversion will be limited on Windows.")
        docx2pdf_convert = None
else:
    # Linux 系统使用 LibreOffice 转换
    docx2pdf_convert = None

try:
    import pypandoc
except ImportError:
    logger.warning("pypandoc not installed. Some conversion features will be limited.")
    pypandoc = None

from .base import BaseConverter
from .xmind_converter import XmindToMarkdownConverter  # 添加这行导入

class DocxToPDFConverter(BaseConverter):
    def __init__(self):
        super().__init__()
        self.supported_input_formats = ['.docx', '.doc']
        self.supported_output_formats = ['.pdf']
        self.soffice_path = find_soffice()
    
    def convert(self, input_path: str, output_path: str) -> bool:
        try:
            if platform.system() == "Windows" and docx2pdf_convert:
                # Windows 优先使用 docx2pdf
                docx2pdf_convert(input_path, output_path)
            else:
                # 使用 LibreOffice 进行转换
                if not self.soffice_path:
                    raise Exception(
                        "找不到 LibreOffice。请安装 LibreOffice:\n"
                        "- Windows: 从 https://www.libreoffice.org 下载安装\n"
                        "- Linux (Ubuntu): sudo apt-get install libreoffice\n"
                        "- Linux (CentOS): sudo yum install libreoffice"
                    )
                
                import subprocess
                input_path = os.path.abspath(input_path)
                output_dir = os.path.abspath(os.path.dirname(output_path))
                
                cmd = [
                    self.soffice_path,
                    '--headless',
                    '--convert-to', 'pdf',
                    '--outdir', output_dir,
                    input_path
                ]
                
                logger.info(f"执行命令: {' '.join(cmd)}")
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    check=False  # 不自动抛出异常
                )
                
                if result.returncode != 0:
                    error_msg = f"LibreOffice转换失败:\n命令: {' '.join(cmd)}\n错误: {result.stderr}"
                    logger.error(error_msg)
                    raise Exception(error_msg)
                
                # 重命名输出文件
                temp_pdf = os.path.splitext(os.path.basename(input_path))[0] + '.pdf'
                temp_pdf_path = os.path.join(output_dir, temp_pdf)
                
                if not os.path.exists(temp_pdf_path):
                    raise Exception(f"PDF文件未生成: {temp_pdf_path}")
                    
                os.rename(temp_pdf_path, output_path)
                logger.info(f"成功转换为PDF: {output_path}")
            
            return True
            
        except Exception as e:
            logger.error(f"转换失败: {str(e)}")
            return False

def check_pandoc():
    """检查pandoc是否已安装"""
    try:
        import subprocess
        result = subprocess.run(['pandoc', '--version'], capture_output=True, text=True)
        return result.returncode == 0
    except:
        return False

class DocxToMarkdownConverter(BaseConverter):
    def __init__(self):
        super().__init__()
        self.supported_input_formats = ['.docx', '.doc']
        self.supported_output_formats = ['.md']
    
    def convert(self, input_path: str, output_path: str) -> bool:
        try:
            if not check_pandoc():
                raise Exception(
                    "未找到pandoc，请安装pandoc：\n"
                    "Ubuntu: sudo apt-get install pandoc\n"
                    "CentOS: sudo yum install pandoc\n"
                    "或访问 https://pandoc.org/installing.html"
                )
            
            if pypandoc is None:
                raise Exception("pypandoc未正确安装，请重新安装：pip install pypandoc")
                
            # 使用绝对路径
            input_path = os.path.abspath(input_path)
            output_path = os.path.abspath(output_path)
            
            pypandoc.convert_file(input_path, 'markdown', outputfile=output_path)
            
            if not os.path.exists(output_path):
                raise Exception("转换后的文件未生成")
                
            return True
            
        except Exception as e:
            logger.error(f"转换失败: {str(e)}")
            return False

class MarkdownToDocxConverter(BaseConverter):
    def __init__(self):
        super().__init__()
        self.supported_input_formats = ['.md']
        self.supported_output_formats = ['.docx']
    
    def convert(self, input_path: str, output_path: str) -> bool:
        try:
            pypandoc.convert_file(input_path, 'docx', outputfile=output_path)
            return True
        except Exception as e:
            print(f"转换失败: {str(e)}")
            return False

class MarkdownToPDFConverter(BaseConverter):
    def __init__(self):
        super().__init__()
        self.supported_input_formats = ['.md']
        self.supported_output_formats = ['.pdf']
    
    def convert(self, input_path: str, output_path: str) -> bool:
        try:
            pypandoc.convert_file(input_path, 'pdf', outputfile=output_path)
            return True
        except Exception as e:
            print(f"转换失败: {str(e)}")
            return False

class XmindToDocxConverter(BaseConverter):
    def __init__(self):
        super().__init__()
        self.supported_input_formats = ['.xmind']
        self.supported_output_formats = ['.docx']
    
    def convert(self, input_path: str, output_path: str) -> bool:
        try:
            # 首先转换为markdown
            temp_md_path = output_path.replace('.docx', '_temp.md')
            xmind_converter = XmindToMarkdownConverter()
            if not xmind_converter.convert(input_path, temp_md_path):
                return False
                
            # 然后将markdown转换为docx
            md_converter = MarkdownToDocxConverter()
            result = md_converter.convert(temp_md_path, output_path)
            
            # 删除临时文件
            if os.path.exists(temp_md_path):
                os.remove(temp_md_path)
                
            return result
            
        except Exception as e:
            print(f"转换失败: {str(e)}")
            return False
