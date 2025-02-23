import gradio as gr
import os
import tempfile
import shutil
import datetime
import hashlib
import json
from file_master_core import xmind_to_md, markdown_to_xmind
import logging
from config import Config
from factory import ConverterFactory

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

INPUT_DIR = os.path.join(os.path.dirname(__file__), "./../data/input")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "./../data/output")
DEFAULT_USER = {
    "settle": hashlib.md5("Start#1900**".encode()).hexdigest()
}


class FileProcessingSystem:
    def __init__(self):
        self.config = Config()
        self.setup_ui()
    
    def setup_ui(self):
        # ... 现有的UI设置代码 ...
        pass
    
    def convert_file(self, file_obj, conversion_type):
        try:
            converter = ConverterFactory.get_converter(conversion_type)
            # ... 文件处理逻辑 ...
        except Exception as e:
            logger.error(f"转换失败: {str(e)}")
            return None, str(e)
    
    # ... 其他方法 ...

def check_login(username, password):
    """验证用户登录"""
    # 检查输入是否为空
    if not username or not password:
        return False, "用户名和密码不能为空"
        
    # 检查用户名是否存在
    if username not in DEFAULT_USER:
        return False, "用户名不存在"
        
    # 验证密码
    hashed_pwd = hashlib.md5(password.encode()).hexdigest()
    if hashed_pwd == DEFAULT_USER[username]:
        return True, "登录成功"
    return False, "密码错误"

def ensure_dirs():
    """确保输入输出目录存在"""
    for dir_path in [INPUT_DIR, OUTPUT_DIR]:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            logger.info(f"创建目录: {dir_path}")

def get_timestamp():
    """生成时间戳字符串"""
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

def get_filename_with_timestamp(filename):
    """为文件名添加时间戳"""
    name, ext = os.path.splitext(filename)
    return f"{name}_{get_timestamp()}{ext}"

def convert_file_web(file_obj, menu_option):
    """处理文件转换"""
    try:
        ensure_dirs()
        if file_obj is None:
            return None, "请选择要转换的文件"
            
        original_filename = os.path.basename(file_obj.name)
        timestamped_filename = get_filename_with_timestamp(original_filename)
        file_name, file_ext = os.path.splitext(original_filename)
        input_path = os.path.join(INPUT_DIR, timestamped_filename)
        shutil.copy2(file_obj.name, input_path)

        # 根据菜单选项执行对应转换
        if menu_option == "Xmind转Markdown":
            if not file_ext.lower() == '.xmind':
                return None, "请上传.xmind文件"
            output_path = os.path.join(OUTPUT_DIR, f"{file_name}_{get_timestamp()}.md")
            xmind_to_md(input_path, output_path)
            
        elif menu_option == "Markdown转Xmind":
            if not file_ext.lower() == '.md':
                return None, "请上传.md文件"
            output_path = os.path.join(OUTPUT_DIR, f"{file_name}_{get_timestamp()}.xmind")
            markdown_to_xmind(input_path, output_path)
            
        elif menu_option == "docx转PDF":
            if not file_ext.lower() in ['.doc', '.docx']:
                return None, "请上传Word文件"
            output_path = os.path.join(OUTPUT_DIR, f"{file_name}_{get_timestamp()}.pdf")
            word_to_pdf(input_path, output_path)
            
        # ...其他转换类型的处理...
            
        return output_path, "转换成功"
        
    except Exception as e:
        return None, f"转换失败: {str(e)}"

def update_conversion_type(file_obj):
    """根据上传文件类型自动设置转换类型"""
    if file_obj is None:
        return gr.update()
    
    file_ext = os.path.splitext(file_obj.name)[1].lower()
    if file_ext == '.xmind':
        return gr.update(value="XMind to Markdown")
    elif file_ext == '.md':
        return gr.update(value="Markdown to XMind")
    return gr.update()

def parse_menu_file(file_path):
    """解析markdown菜单文件为三级树形结构"""
    menu_tree = []
    current_l1 = None
    current_l2 = None
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#') and not line.startswith('##'):
                    continue
                    
                if line.startswith('## '):
                    # 一级菜单
                    l1_name = line.split('.')[1].strip()
                    current_l1 = {"name": l1_name, "children": []}
                    menu_tree.append(current_l1)
                    current_l2 = None
                elif line.startswith('### '):
                    # 二级菜单
                    if current_l1:
                        l2_name = line.split('.')[1].strip()
                        current_l2 = {"name": l2_name, "children": []}
                        current_l1["children"].append(current_l2)
                elif line.startswith('- '):
                    # 三级菜单项
                    if current_l2:
                        l3_name = line.replace('- ', '').strip()
                        current_l2["children"].append({
                            "name": l3_name,
                            "action": l3_name.lower().replace(' ', '_')
                        })
    except Exception as e:
        print(f"解析菜单文件出错: {str(e)}")
        return []
        
    return menu_tree

def get_menu_items():
    """获取主菜单项"""
    menu_file = os.path.join(os.path.dirname(__file__), "文件处理系统菜单.md")
    menu_structure = parse_menu_file(menu_file)
    return list(menu_structure.keys())

def get_submenu_items(menu_selection):
    """获取子菜单项"""
    menu_file = os.path.join(os.path.dirname(__file__), "文件处理系统菜单.md")
    menu_structure = parse_menu_file(menu_file)
    if menu_selection in menu_structure:
        return list(menu_structure[menu_selection].keys())
    return []

def get_submenu_options(menu_selection, submenu_selection):
    """获取子菜单选项"""
    menu_file = os.path.join(os.path.dirname(__file__), "文件处理系统菜单.md")
    menu_structure = parse_menu_file(menu_file)
    if (menu_selection in menu_structure and 
        submenu_selection in menu_structure[menu_selection]):
        return menu_structure[menu_selection][submenu_selection]
    return []

def create_menu_structure(menu_data):
    """将菜单数据转换为Accordion组件结构"""
    menu_items = []
    for item in menu_data:
        if "children" in item:
            menu_items.append([item["name"], item["children"]])
    return menu_items

custom_css = """
.gradio-container {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
}

.main-header {
    text-align: center;
    color: #2c3e50;
    margin: 2rem 0;
}

.menu-panel {
    background: #f8f9fa;
    padding: 1rem;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    min-width: 200px;
}

.menu-title {
    font-size: 1.2em;
    font-weight: bold;
    margin-bottom: 1rem;
    color: #2c3e50;
}

.menu-group {
    margin-bottom: 1rem;
    padding: 0.5rem;
    border-radius: 4px;
}

.content-panel {
    background: white;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.login-container {
    max-width: 400px;
    margin: 100px auto;
    padding: 2rem;
    background: white;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

"""

with gr.Blocks(
    title="文件处理系统",
    css=custom_css,
    theme=gr.themes.Soft(
        primary_hue="blue",
        secondary_hue="gray",
        neutral_hue="gray",
        radius_size=gr.themes.sizes.radius_sm,
        font=[gr.themes.GoogleFont("Source Sans Pro"), "ui-sans-serif", "system-ui"]
    )
) as demo:
    # 登录状态
    logged_in = gr.State(False)
    
    # 登录页面
    with gr.Column(visible=True, elem_classes="login-container") as login_page:
        gr.Markdown("# 文件处理系统", elem_classes="main-header")
        with gr.Column(elem_classes="content-panel"):
            username = gr.Textbox(
                label="用户名",
                placeholder="请输入用户名",
                value="settle",  # 默认用户名
                elem_classes="input-field"
            )
            password = gr.Textbox(
                label="密码",
                type="password",
                placeholder="请输入密码",
                value="Start#1900**",  # 默认密码
                elem_classes="input-field"
            )
            with gr.Row():
                login_btn = gr.Button(
                    "登录",
                    variant="primary",
                    elem_classes="login-button"
                )
            login_msg = gr.Textbox(
                label="状态",
                interactive=False,
                visible=True,
                elem_classes="error-message"
            )
    
    # 主页面
    with gr.Column(visible=False) as main_page:
        gr.Markdown("# 文件处理系统", elem_classes="main-header")
        with gr.Row():
            # 左侧菜单
            with gr.Column(scale=1, elem_classes="menu-panel"):
                menu_file = os.path.join(os.path.dirname(__file__), "文件处理系统菜单.md")
                menu_tree = parse_menu_file(menu_file)
                
                gr.Markdown("### 功能导航", elem_classes="menu-title")
                
                # 一级菜单选择
                l1_choices = [item["name"] for item in menu_tree]
                l1_menu = gr.Radio(
                    choices=l1_choices,
                    label="主功能",
                    interactive=True,
                    elem_classes="menu-group"
                )
                
                # 二级菜单选择（动态更新）
                l2_menu = gr.Radio(
                    choices=[],
                    label="子功能",
                    interactive=True,
                    elem_classes="menu-group",
                    visible=False
                )
                
                # 三级菜单选择（动态更新）
                l3_menu = gr.Radio(
                    choices=[],
                    label="具体功能",
                    interactive=True,
                    elem_classes="menu-group",
                    visible=False
                )

            # 右侧内容区
            with gr.Column(scale=4, elem_classes="content-panel") as content_area:
                gr.Markdown("## 请从左侧选择功能")
                with gr.Group(visible=False) as content_group:
                    title = gr.Markdown("## 功能标题")
                    description = gr.Markdown("功能描述")
                    file_input = gr.File(label="选择文件")
                    convert_btn = gr.Button("开始处理", variant="primary")
                    output_msg = gr.Textbox(label="状态信息")
                    output_file = gr.File(label="处理结果")

    # 处理登录事件
    def handle_login(username, password):
        success, msg = check_login(username, password)
        if (success):
            return {
                login_page: gr.update(visible=False),
                main_page: gr.update(visible=True),
                login_msg: gr.update(value=msg, visible=True)
            }
        return {
            login_msg: gr.update(value=msg, visible=True)
        }
    
    login_btn.click(
        fn=handle_login,
        inputs=[username, password],
        outputs=[login_page, main_page, login_msg]
    )
    
    # # 文件上传时自动更新转换类型
    # file_input.change(
    #     fn=update_conversion_type,
    #     inputs=[file_input],
    #     outputs=[conversion_type]
    # )
    
    # 处理文件转换
    convert_btn.click(
        fn=convert_file_web,
        inputs=[file_input, l3_menu],
        outputs=[output_file, output_msg]
    )

    # 更新二级菜单选项
    def update_l2_menu(l1_selection):
        if not l1_selection:
            return gr.update(choices=[], visible=False), gr.update(choices=[], visible=False)
        
        for l1_item in menu_tree:
            if l1_item["name"] == l1_selection:
                l2_choices = [item["name"] for item in l1_item["children"]]
                return gr.update(choices=l2_choices, visible=True), gr.update(choices=[], visible=False)
        return gr.update(choices=[], visible=False), gr.update(choices=[], visible=False)

    # 更新三级菜单选项
    def update_l3_menu(l1_selection, l2_selection):
        if not l1_selection or not l2_selection:
            return gr.update(choices=[], visible=False)
            
        for l1_item in menu_tree:
            if l1_item["name"] == l1_selection:
                for l2_item in l1_item["children"]:
                    if l2_item["name"] == l2_selection:
                        l3_choices = [item["name"] for item in l2_item["children"]]
                        return gr.update(choices=l3_choices, visible=True)
        return gr.update(choices=[], visible=False)

    # 连接菜单事件
    l1_menu.change(
        fn=update_l2_menu,
        inputs=[l1_menu],
        outputs=[l2_menu, l3_menu]
    )
    
    l2_menu.change(
        fn=update_l3_menu,
        inputs=[l1_menu, l2_menu],
        outputs=[l3_menu]
    )
    
    # 更新内容区域
    def update_content_area(selected_option):
        if not selected_option:
            return (
                gr.update(visible=False),
                gr.update(value=""),
                gr.update(value="")
            )
        
        return (
            gr.update(visible=True),
            gr.update(value=f"## {selected_option}"),
            gr.update(value="请上传需要转换的文件")
        )

    # 绑定三级菜单变化事件
    l3_menu.change(
        fn=update_content_area,
        inputs=[l3_menu],
        outputs=[content_group, title, description]
    )

def main():
    try:
        system = FileProcessingSystem()
        demo.launch(
            server_name="127.0.0.1",  # 改为本地回环地址
            server_port=7860,
            share=True,             # 启用分享链接
            debug=True,
            show_api=False         # 关闭 API 文档
        )
    except Exception as e:
        logging.error(f"程序启动失败: {str(e)}")
        input("按任意键退出...")  # 防止窗口立即关闭

if __name__ == "__main__":
    main()