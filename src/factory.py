from converters.mindmap_converter import XmindToMarkdownConverter, MarkdownToXmindConverter
# 导入其他转换器...

class ConverterFactory:
    _converters = {
        'xmind_to_md': XmindToMarkdownConverter,
        'md_to_xmind': MarkdownToXmindConverter,
        # 注册其他转换器...
    }
    
    @classmethod
    def get_converter(cls, converter_type: str):
        converter_class = cls._converters.get(converter_type)
        if not converter_class:
            raise ValueError(f"不支持的转换类型: {converter_type}")
        return converter_class()
