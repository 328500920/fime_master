from .base import BaseConverter
import pandas as pd
import os
import zipfile
from typing import List

class ExcelToCSVConverter(BaseConverter):
    def __init__(self):
        super().__init__()
        self.supported_input_formats = ['.xlsx', '.xls']
        self.supported_output_formats = ['.csv', '.zip']
    
    def convert(self, input_path: str, output_path: str) -> bool:
        try:
            if not os.path.exists(input_path):
                print(f"输入文件不存在: {input_path}")
                return False
                
            # 创建输出目录
            output_dir = os.path.dirname(output_path)
            os.makedirs(output_dir, exist_ok=True)
            
            # 读取Excel文件的所有表格
            excel_file = pd.ExcelFile(input_path)
            sheet_names = excel_file.sheet_names
            
            # 如果只有一个表格，直接转换为CSV
            if len(sheet_names) == 1:
                df = pd.read_excel(input_path)
                df.to_csv(output_path, index=False, encoding='utf-8')
                return True
                
            # 如果有多个表格，创建临时目录存放CSV文件
            temp_dir = os.path.join(output_dir, "temp_csv")
            os.makedirs(temp_dir, exist_ok=True)
            
            csv_files = []
            try:
                # 转换每个表格为CSV
                for sheet in sheet_names:
                    df = pd.read_excel(input_path, sheet_name=sheet)
                    safe_sheet_name = "".join(x for x in sheet if x.isalnum() or x in "._- ")
                    csv_path = os.path.join(temp_dir, f"{safe_sheet_name}.csv")
                    df.to_csv(csv_path, index=False, encoding='utf-8')
                    csv_files.append(csv_path)
                
                # 创建ZIP文件（替换原始的output_path扩展名）
                zip_path = os.path.splitext(output_path)[0] + '.zip'
                with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for csv_file in csv_files:
                        # 将CSV文件添加到ZIP中，使用相对路径
                        arcname = os.path.basename(csv_file)
                        zipf.write(csv_file, arcname)
                
                # 更新输出路径为zip文件路径
                if os.path.exists(zip_path):
                    os.rename(zip_path, output_path)
                
                return True
                
            finally:
                # 清理临时文件和目录
                for csv_file in csv_files:
                    try:
                        if os.path.exists(csv_file):
                            os.remove(csv_file)
                    except:
                        pass
                try:
                    if os.path.exists(temp_dir):
                        os.rmdir(temp_dir)
                except:
                    pass
            
        except Exception as e:
            print(f"转换失败: {str(e)}")
            return False

class CSVToExcelConverter(BaseConverter):
    def __init__(self):
        super().__init__()
        self.supported_input_formats = ['.csv']
        self.supported_output_formats = ['.xlsx']
    
    def convert(self, input_path: str, output_path: str) -> bool:
        try:
            df = pd.read_csv(input_path, encoding='utf-8')
            df.to_excel(output_path, index=False)
            return True
            
        except Exception as e:
            print(f"转换失败: {str(e)}")
            return False

class ExcelToPDFConverter(BaseConverter):
    def __init__(self):
        super().__init__()
        self.supported_input_formats = ['.xlsx', '.xls']
        self.supported_output_formats = ['.pdf']
    
    def convert(self, input_path: str, output_path: str) -> bool:
        try:
            # 检测操作系统类型
            if os.name == 'nt':  # Windows
                return self._convert_windows(input_path, output_path)
            else:  # Linux/Unix
                return self._convert_linux(input_path, output_path)
                
        except Exception as e:
            print(f"转换失败: {str(e)}")
            return False
    
    def _convert_windows(self, input_path: str, output_path: str) -> bool:
        try:
            # 初始化COM环境
            import pythoncom
            import win32com.client
            
            pythoncom.CoInitialize()
            
            # 使用绝对路径
            input_path = os.path.abspath(input_path)
            output_path = os.path.abspath(output_path)
            
            # 使用Excel COM对象进行转换
            excel = win32com.client.Dispatch("Excel.Application")
            excel.Visible = False
            excel.DisplayAlerts = False
            
            try:
                wb = excel.Workbooks.Open(input_path)
                wb.ExportAsFixedFormat(0, output_path)
                return True
            finally:
                if 'wb' in locals():
                    wb.Close(SaveChanges=False)
                excel.Quit()
                pythoncom.CoUninitialize()
                
        except Exception as e:
            print(f"Windows转换失败: {str(e)}")
            return False
    
    def _convert_linux(self, input_path: str, output_path: str) -> bool:
        try:
            # 使用LibreOffice进行转换
            import subprocess
            
            # 确保输入输出路径是绝对路径
            input_path = os.path.abspath(input_path)
            output_path = os.path.abspath(output_path)
            
            # 使用soffice命令进行转换
            cmd = [
                'soffice',
                '--headless',
                '--convert-to', 'pdf',
                '--outdir', os.path.dirname(output_path),
                input_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"LibreOffice转换失败: {result.stderr}")
                return False
                
            # LibreOffice生成的PDF文件名可能与我们想要的不同，需要重命名
            generated_pdf = os.path.splitext(os.path.basename(input_path))[0] + '.pdf'
            generated_pdf_path = os.path.join(os.path.dirname(output_path), generated_pdf)
            
            if os.path.exists(generated_pdf_path):
                os.rename(generated_pdf_path, output_path)
                return True
            
            return False
            
        except Exception as e:
            print(f"Linux转换失败: {str(e)}")
            return False
