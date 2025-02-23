中文版本 | [English Version](./README.md)

# FileMaster - 多功能文件处理系统

FileMaster是一个基于Python的文件处理Web应用系统，提供高效的文件转换与处理功能。

## 功能特性

### 文档转换

- DOCX/PDF/Markdown互转
- 批量转换支持
- 保持文档格式

### 表格处理

- Excel/CSV/PDF转换
- 多表格处理
- 数据校验支持

### 思维导图处理

- Xmind/Markdown/DOCX互转
- 保持思维导图结构
- 支持附件处理

## 技术架构

- 前端：
  - Gradio UI框架
  - 响应式设计
- 后端：
  - Python 3.10+
  - FastAPI支持
- 核心组件：
  - 统一转换器API
  - 异步处理引擎
  - 格式自动检测

## 快速开始

### 环境要求

- Python 3.10+
- 依赖包：gradio, xmind, markdown

### 安装

```bash
git clone https://github.com/fuxingwang/filemaster.git
cd FileMaster
conda create -n filemaster python=3.10
conda activate filemaster
pip install -r requirements.txt
```

### 运行

```bash
python src/main_web.py
```

## API使用说明

```python
from factory import ConverterFactory

# 创建转换器
converter = ConverterFactory.get_converter('xmind_to_md')

# 执行转换
converter.convert('input.xmind', 'output.md')
```

## 项目结构

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
│   └── 文件处理系统菜单.md
├── requirements.txt
└── README.md
```

## 配置说明

在 `config.py`中配置：

- 输入输出目录
- 用户认证信息
- 支持的文件格式

## 扩展开发

要添加新的文件转换器：

1. 在 `converters`目录下创建新的转换器类
2. 继承 `BaseConverter`类
3. 在 `ConverterFactory`中注册新转换器

## 贡献指南

欢迎提交Issue和Pull Request，请确保：

- 代码符合PEP 8规范
- 添加适当的测试用例
- 更新相关文档

## 许可证

MIT License

## 联系方式

- 项目维护者：[fuxingwang]
- Email：[328500920@qq.com]
- GitHub：[fuxingwang]
