[中文版本](./README-ch.md) | English Version

# File Master

A versatile file conversion and processing tool with web interface.

## Features

### Document Conversion

- Convert DOCX/PDF/Markdown (any to any)
- Support batch conversion
- Preserve document formatting

### Spreadsheet Processing

- Excel/CSV/PDF conversion
- Multi-sheet handling
- Data validation support

### Mind Map Processing

- Convert between Xmind/Markdown/DOCX
- Preserve mind map structure
- Support attachments

## Technical Architecture

- Frontend:
  - Gradio UI Framework
  - Responsive design
- Backend:
  - Python 3.10+
  - FastAPI support
- Core Components:
  - Unified Converter API
  - Async Processing Engine
  - Format Detection

## Quick Start

### Requirements

- Python 3.10+
- Dependencies: gradio, xmind, markdown

### Installation

```bash
git clone https://github.com/fuxingwang/filemaster.git
cd FileMaster
pip install -r requirements.txt
```

### Running

```bash
python src/main_web.py
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
│   ├── main_web.py
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
