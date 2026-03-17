"""输入文本"""
import os
# 动态获取路径
this_dir = os.path.dirname(__file__) # 当前路径
last1 = os.path.basename(this_dir) # 当前文件夹名称
last2 = os.path.basename(os.path.dirname(this_dir)) # 上级文件夹名称
gategory=f"{last2}🦄🦄🦄/{last1}" # 在comfyui中的目录：上级文件夹名称/当前文件夹名称
# ————————————————————————————————————————————————

class in01_input_text:
    def __init__(self):
        pass
    CATEGORY = gategory

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input_str": ("STRING", {
                    "default": "",  # 默认存在内容
                    "multiline": True}),  # 是否允许多行输入

            },
        }   
    
    OUTPUT_NODE = True
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("str",)

    FUNCTION = "test"
    def test(self,input_str):
        return {"result": (input_str,)}


NODE_CLASS_MAPPINGS = {"in01_input_text": in01_input_text,}
NODE_DISPLAY_NAME_MAPPINGS = {"in01_input_text":"input_text🦄",}