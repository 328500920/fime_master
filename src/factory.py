import platform
import logging

logger = logging.getLogger(__name__)

class ConverterFactory:
    _converters = {}
    
    @classmethod
    def register_converters(cls):
        """根据环境注册可用的转换器"""
        from converters.xmind_converter import XmindToMarkdownConverter, MarkdownToXmindConverter
        from converters.document_converter import (
            DocxToMarkdownConverter,
            MarkdownToDocxConverter,
            MarkdownToPDFConverter,
            DocxToPDFConverter,
            XmindToDocxConverter
        )
        from converters.excel_converter import (
            ExcelToCSVConverter,
            CSVToExcelConverter,
            ExcelToPDFConverter
        )
        
        # 基础转换器
        cls._converters.update({
            'xmind_to_md': XmindToMarkdownConverter,
            'md_to_xmind': MarkdownToXmindConverter,
            'docx_to_md': DocxToMarkdownConverter,
            'md_to_docx': MarkdownToDocxConverter,
            'md_to_pdf': MarkdownToPDFConverter,
            'excel_to_csv': ExcelToCSVConverter,
            'csv_to_excel': CSVToExcelConverter,
            'xmind_to_docx': XmindToDocxConverter,
        })
        
        # 特定平台的转换器
        if platform.system() == "Windows":
            cls._converters.update({
                'docx_to_pdf': DocxToPDFConverter,
                'excel_to_pdf': ExcelToPDFConverter,
            })
        else:
            # Linux系统使用LibreOffice的转换器
            cls._converters.update({
                'docx_to_pdf': DocxToPDFConverter,
                'excel_to_pdf': ExcelToPDFConverter,
            })
    
    @classmethod
    def get_converter(cls, converter_type: str):
        if not cls._converters:
            cls.register_converters()
            
        converter_class = cls._converters.get(converter_type)
        if not converter_class:
            raise ValueError(f"不支持的转换类型: {converter_type}")
        return converter_class()

# 初始化时注册转换器
ConverterFactory.register_converters()
