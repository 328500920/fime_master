from .base import BaseConverter
import xmindparser
import xmind
import re

class XmindToMarkdownConverter(BaseConverter):
    def __init__(self):
        super().__init__()
        self.supported_input_formats = ['.xmind']
        self.supported_output_formats = ['.md']
    
    def process_topic(self, topic, markdown_text, level):
        children = topic.get('topics', ())
        for child in children:
            title = child['title']
            markdown_text += "#" * (level + 1) + " " + title + "\n\n"
            markdown_text = self.process_topic(child, markdown_text, level + 1)
        return markdown_text
    
    def convert(self, input_path: str, output_path: str) -> bool:
        try:
            content = xmindparser.xmind_to_dict(input_path)
            markdown_text = ""
            markdown_title = ""
            for sheet in content:
                root_topic = sheet["topic"]
                markdown_title += f"# {root_topic['title']}\n\n"
                markdown_text += self.process_topic(root_topic, markdown_title, 1)
                
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(markdown_text)
            return True
            
        except Exception as e:
            print(f"转换失败: {str(e)}")
            return False

class MarkdownToXmindConverter(BaseConverter):
    def __init__(self):
        super().__init__()
        self.supported_input_formats = ['.md']
        self.supported_output_formats = ['.xmind']
    
    def convert(self, input_path: str, output_path: str) -> bool:
        try:
            # 读取markdown文件
            with open(input_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 创建xmind工作簿和工作表
            w = xmind.load(output_path)  # 如果文件不存在会创建新的
            s1 = w.getPrimarySheet()
            s1.setTitle("Sheet 1")
            
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
            xmind.save(w, path=output_path)
            return True
            
        except Exception as e:
            print(f"转换失败: {str(e)}")
            return False

# 其他转换器类（DocToPDF, ExcelToCSV等）也类似实现...
