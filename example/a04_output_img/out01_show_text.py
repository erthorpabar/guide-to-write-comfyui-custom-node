"""显示文本"""
import os
# 动态获取路径
this_dir = os.path.dirname(__file__) # 当前路径
last1 = os.path.basename(this_dir) # 当前文件夹名称
last2 = os.path.basename(os.path.dirname(this_dir)) # 上级文件夹名称
gategory=f"{last2}🦄🦄🦄/{last1}" # 在comfyui中的目录：上级文件夹名称/当前文件夹名称
# ————————————————————————————————————————————————

class out01_show_text:
    def __init__(self):
        pass
    CATEGORY = gategory

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                 "text": ("STRING", {"forceInput": True}),
                 
            },
        }   
    
    OUTPUT_NODE = True
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("str",)

    FUNCTION = "test"
    def test(self,text=None):
        return {"ui": {"text": text}, "result": (text,)}


NODE_CLASS_MAPPINGS = {"out01_show_text": out01_show_text,}
NODE_DISPLAY_NAME_MAPPINGS = {"out01_show_text":"show_text🦄",}