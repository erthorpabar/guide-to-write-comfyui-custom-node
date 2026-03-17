"""输入int"""
import os
# 动态获取路径
this_dir = os.path.dirname(__file__) # 当前路径
last1 = os.path.basename(this_dir) # 当前文件夹名称
last2 = os.path.basename(os.path.dirname(this_dir)) # 上级文件夹名称
gategory=f"{last2}🦄🦄🦄/{last1}" # 在comfyui中的目录：上级文件夹名称/当前文件夹名称
# ————————————————————————————————————————————————

class in02_input_int:
    def __init__(self):
        pass
    CATEGORY = gategory

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                 "input_int": ("INT", {
                    "default": 0,  # 默认
                    "min": -10000,
                    "max": 10000,
                    "step": 1,  # 步长
                    "display": "number"}),  # 数值调整

            },
        }   
    
    OUTPUT_NODE = True
    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("int",)

    FUNCTION = "test"
    def test(self,input_int):
        return {"result": (input_int,)}


NODE_CLASS_MAPPINGS = {"in02_input_int": in02_input_int,}
NODE_DISPLAY_NAME_MAPPINGS = {"in02_input_int":"input_int🦄",}