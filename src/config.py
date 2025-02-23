import os
import json

class Config:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._init_config()
        return cls._instance
    
    def _init_config(self):
        self.INPUT_DIR = "/home/subt/tools_web/input"
        self.OUTPUT_DIR = "/home/subt/tools_web/output"
        self.TEMP_DIR = "/home/subt/tools_web/temp"
        
        # 用户配置
        self.DEFAULT_USER = {
            "settle": "md5_hashed_password"
        }
        
        # 支持的文件转换类型
        self.SUPPORTED_CONVERSIONS = {
            'xmind_to_md': {'input': '.xmind', 'output': '.md'},
            'md_to_xmind': {'input': '.md', 'output': '.xmind'},
            'word_to_pdf': {'input': ['.doc', '.docx'], 'output': '.pdf'},
            'excel_to_csv': {'input': ['.xls', '.xlsx'], 'output': '.csv'},
            # ... 其他转换类型配置
        }
        
        self._ensure_directories()
    
    def _ensure_directories(self):
        for dir_path in [self.INPUT_DIR, self.OUTPUT_DIR, self.TEMP_DIR]:
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
