[中文版本](./README-ch.md) | English Version

# FileMaster - Multipurpose File Processing System

FileMaster is a Python-based web application system for file processing, offering rich file conversion and processing capabilities with modular design and support for multiple file formats.

## Features

- Document Conversion
  - Word/PDF conversion
  - Markdown format conversion
  - Mind map conversion
- Spreadsheet Processing
  - Excel/CSV conversion
  - Excel sheet processing
  - Table merging
- Mind Map Processing
  - Xmind to Markdown conversion
  - Mind map format conversion
- File Security
  - PDF encryption/decryption
  - Watermark addition/removal
  - Digital signatures

## Technical Architecture

- Frontend: Gradio UI Framework
- Backend: Python
- Design Patterns: Factory Pattern, Singleton Pattern
- Core Components:
  - Converter Factory
  - File Processing Engine
  - Configuration Manager

## Quick Start

### Requirements

- Python 3.7+
- Dependencies: gradio, xmind, markdown

### Installation

```bash
git clone [repository-url]
cd FileMaster
pip install -r requirements.txt
```

### Running

```bash
python src/file_master_web.py
```

## API Usage

```python
from factory import ConverterFactory

# Create converter
converter = ConverterFactory.get_converter('xmind_to_md')

# Execute conversion
converter.convert('input.xmind', 'output.md')
```

## Project Structure

```
FileMaster/
├── src/
│   ├── converters/
│   │   ├── base.py
│   │   ├── mindmap_converter.py
│   │   └── ...
│   ├── factory.py
│   ├── config.py
│   ├── file_master_web.py
│   └── menu.md
├── requirements.txt
└── README.md
```

## Configuration

Configure in `config.py`:

- Input/output directories
- User authentication
- Supported file formats

## Development

To add new file converters:

1. Create new converter class in `converters` directory
2. Inherit from `BaseConverter` class
3. Register new converter in `ConverterFactory`

## Contributing

Welcome to submit Issues and Pull Requests. Please ensure:

- Code follows PEP 8 standards
- Add appropriate test cases
- Update relevant documentation

## License

MIT License

## Contact

- Maintainer: [fuxingwang]
- Email: [328500920@qq.com]
- GitHub: [fuxingwang]
