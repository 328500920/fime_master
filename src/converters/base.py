from abc import ABC, abstractmethod

class BaseConverter(ABC):
    def __init__(self):
        self.supported_input_formats = []
        self.supported_output_formats = []
    
    @abstractmethod
    def convert(self, input_path: str, output_path: str) -> bool:
        pass
    
    def validate_format(self, file_path: str, is_input: bool = True) -> bool:
        formats = self.supported_input_formats if is_input else self.supported_output_formats
        return any(file_path.lower().endswith(fmt) for fmt in formats)
