中文版本 | [English Version](./readme.md)

# FileMaster - 多功能文件处理系统

FileMaster是一个基于Python的文件处理Web应用系统，提供丰富的文件转换、处理功能，采用模块化设计，支持多种文件格式的转换与处理。

## 功能特性

- 文档转换

  - Word/PDF互转
  - Markdown格式转换
  - 思维导图转换
- 表格处理

  - Excel/CSV互转
  - Excel分表处理
  - 表格合并功能
- 思维导图处理

  - Xmind与Markdown互转
  - 思维导图格式转换
- 文件安全

  - PDF加密解密
  - 水印添加/移除
  - 文件数字签名

## 技术架构

- 前端：Gradio UI框架
- 后端：Python
- 设计模式：工厂模式、单例模式
- 核心组件：
  - 转换器工厂
  - 文件处理引擎
  - 配置管理器

## 快速开始

### 环境要求

- Python 3.7+
- 依赖包：gradio, xmind, markdown

### 安装

```bash
git clone [repository-url]
cd FileMaster
pip install -r requirements.txt
```

### 运行

```bash
python src/file_master_web.py
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
│   ├── file_master_web.py
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
