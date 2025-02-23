import os
import xmindparser
import xmind
import sys
import json
import re
import argparse

def process_mmap_topic(topic, markdown_text, level):
    children = topic.get('children', [])
    for child in children:
        title = child.get('text', '')
        markdown_text += "#" * (level + 1) + " " + title + "\n\n"
        markdown_text = process_mmap_topic(child, markdown_text, level + 1)
    return markdown_text

def process_topic(topic, markdown_text, level):
    children = topic.get('topics', ())
    for child in children:
        title = child['title']
        markdown_text += "#" * (level + 1) + " " + title + "\n\n"
        markdown_text = process_topic(child, markdown_text, level + 1)
    return markdown_text

# ... (保留原有的xmind_to_md和mmap_to_md函数)
def xmind_to_md(xmind_file_path, md_file_path):
    try:
        content = xmindparser.xmind_to_dict(xmind_file_path)
        markdown_text = ""
        markdown_title = ""
        for sheet in content:
            root_topic = sheet["topic"]
            markdown_title += f"# {root_topic['title']}\n\n"
            markdown_text += process_topic(root_topic, markdown_title, 1)
        with open(md_file_path, 'w', encoding='utf-8') as f:
            f.write(markdown_text)
        print(f"成功将 {xmind_file_path} 转换为 {md_file_path}")
    except Exception as e:
        print(f"转换 {xmind_file_path} 为 {md_file_path} 时出错: {str(e)}")

def mmap_to_md(mmap_file_path, md_file_path):
    try:
        encodings = ['utf-8', 'gbk', 'utf-16']
        content = None
        for encoding in encodings:
            try:
                with open(mmap_file_path, 'r', encoding=encoding) as f:
                    content = json.load(f)
                break
            except UnicodeDecodeError:
                continue
        if content is None:
            raise ValueError("Unable to read the file with any supported encoding")
        markdown_text = ""
        markdown_title = f"# {content['root']['text']}\n\n"
        markdown_text += process_mmap_topic(content['root'], markdown_title, 1)
        with open(md_file_path, 'w', encoding='utf-8') as f:
            f.write(markdown_text)
        print(f"成功将 {mmap_file_path} 转换为 {md_file_path}")
    except Exception as e:
        print(f"转换 {mmap_file_path} 为 {md_file_path} 时出错: {str(e)}")

def markdown_to_xmind(md_file_path, xmind_file_path):
    try:
        # 读取markdown文件
        with open(md_file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 创建xmind工作簿和工作表 - 使用修正的API调用
        w = xmind.load(xmind_file_path)  # 如果文件不存在会创建新的
        s1 = w.getPrimarySheet()  # 获取第一个工作表
        s1.setTitle("Sheet 1")    # 设置工作表标题
        
        # 确保有根主题
        root = s1.getRootTopic()
        if root is None:
            root = s1.createRootTopic()

        # 解析markdown内容
        lines = content.split('\n')
        current_topics = {0: root}
        current_level = 0

        # 设置根节点标题
        for line in lines:
            if line.startswith('# ') and not line.startswith('## '):
                root.setTitle(line.replace('# ', '').strip())
                break

        # 处理其他标题
        for line in lines:
            if line.startswith('#'):
                level = len(re.match(r'^#+', line).group())
                title = line.replace('#' * level, '').strip()

                if level > current_level:
                    new_topic = current_topics[current_level].addSubTopic()
                    new_topic.setTitle(title)
                    current_topics[level] = new_topic
                else:
                    parent_level = level - 1
                    while parent_level not in current_topics and parent_level > 0:
                        parent_level -= 1
                    new_topic = current_topics[parent_level].addSubTopic()
                    new_topic.setTitle(title)
                    current_topics[level] = new_topic
                
                current_level = level

        # 保存xmind文件
        xmind.save(w, path=xmind_file_path)
        print(f"成功将 {md_file_path} 转换为 {xmind_file_path}")
    except Exception as e:
        print(f"转换 {md_file_path} 为 {xmind_file_path} 时出错: {str(e)}")

def convert_files_in_folder(root_folder, convert_to_md=True):
    print(f"Starting to process folder: {root_folder}")
    for root, dirs, files in os.walk(root_folder):
        print(f"Current directory: {root}")
        print(f"Found files: {files}")
        for file in files:
            print(f"Processing file: {file}")
            if convert_to_md:
                if file.endswith('.xmind'):
                    xmind_file_path = os.path.join(root, file)
                    md_file_name = file[:-6] + '.md'
                    md_file_path = os.path.join(root, md_file_name)
                    print(f"Converting xmind file: {xmind_file_path}")
                    xmind_to_md(xmind_file_path, md_file_path)
                elif file.endswith('.mmap'):
                    mmap_file_path = os.path.join(root, file)
                    md_file_name = file[:-5] + '.md'
                    md_file_path = os.path.join(root, md_file_name)
                    print(f"Converting mmap file: {mmap_file_path}")
                    mmap_to_md(mmap_file_path, md_file_path)
            else:
                if file.endswith('.md'):
                    md_file_path = os.path.join(root, file)
                    xmind_file_name = file[:-3] + '.xmind'
                    xmind_file_path = os.path.join(root, xmind_file_name)
                    print(f"Converting markdown file: {md_file_path}")
                    markdown_to_xmind(md_file_path, xmind_file_path)

def convert_file(input_path, output_path, convert_to_md=True):
    """转换单个文件"""
    try:
        if convert_to_md:
            if input_path.endswith('.xmind'):
                xmind_to_md(input_path, output_path)
            elif input_path.endswith('.mmap'):
                mmap_to_md(input_path, output_path)
        else:
            if input_path.endswith('.md'):
                markdown_to_xmind(input_path, output_path)
    except Exception as e:
        print(f"转换文件时出错: {str(e)}")

# 添加新的转换函数
def word_to_pdf(doc_path, pdf_path):
    """Word转PDF"""
    try:
        from docx2pdf import convert
        convert(doc_path, pdf_path)
        print(f"成功将 {doc_path} 转换为 {pdf_path}")
    except Exception as e:
        print(f"转换失败: {str(e)}")

def excel_to_csv(excel_path, csv_path):
    """Excel转CSV"""
    try:
        import pandas as pd
        df = pd.read_excel(excel_path)
        df.to_csv(csv_path, index=False)
        print(f"成功将 {excel_path} 转换为 {csv_path}")
    except Exception as e:
        print(f"转换失败: {str(e)}")


# 主函数
# 创建时间: 2025-02-18
# 最后修改时间: 2025-02-18
# 当前版本: v4.0
# 作者: 心敢比天高
# 说明: 该脚本支持将XMind文件转换为Markdown文件，或将Markdown文件转换为XMind文件
# 用法: python xmind2markdown_v4.py --input "E:\\baiduCloud\\我的笔记\vscode\\架构师\\工具类\\xmind2markdown\\input\\AI探索分享.xmind" --output "E:\\baiduCloud\\我的笔记\vscode\\架构师\\工具类\\xmind2markdown\\output\\AI探索分享.md" --to-md
# 用法: python xmind2markdown_v4.py --input "file.md" --output "file.xmind" --to-xmind
# 需要安装的python依赖包: xmind, xmindparser 
# pip install xmind xmindparser
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='XMind与Markdown文件转换工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
使用示例:
    # 将XMind转换为Markdown
    python xmind2markdown.py --input "file.xmind" --output "file.md" --to-md
    
    # 将Markdown转换为XMind
    python xmind2markdown.py --input "file.md" --output "file.xmind" --to-xmind
    
支持的文件格式:
    - 输入: .xmind, .md, .mmap
    - 输出: .xmind, .md
        '''
    )
    
    parser.add_argument(
        '--input',
        required=True,
        help='输入文件路径(支持 .xmind/.md/.mmap)'
    )
    
    parser.add_argument(
        '--output',
        required=True, 
        help='输出文件路径(支持 .xmind/.md)'
    )
    
    parser.add_argument(
        '--to-xmind',
        action='store_true',
        help='将输入文件转换为XMind格式'
    )
    
    parser.add_argument(
        '--to-md',
        action='store_true', 
        help='将输入文件转换为Markdown格式'
    )

    args = parser.parse_args()
    
    # 验证输入文件是否存在
    if not os.path.exists(args.input):
        print("输入文件不存在")
        sys.exit(1)
        
    # 验证转换方向参数
    if args.to_xmind == args.to_md:
        print("请指定一个转换方向: --to-xmind 或 --to-md")
        sys.exit(1)
        
    # 确保输出目录存在
    output_dir = os.path.dirname(args.output)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    # 执行转换
    convert_file(args.input, args.output, convert_to_md=args.to_md)