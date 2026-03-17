"""int转float"""
import os
# 动态获取路径
this_dir = os.path.dirname(__file__) # 当前路径
last1 = os.path.basename(this_dir) # 当前文件夹名称
last2 = os.path.basename(os.path.dirname(this_dir)) # 上级文件夹名称
gategory=f"{last2}🦄🦄🦄/{last1}" # 在comfyui中的目录：上级文件夹名称/当前文件夹名称
# ————————————————————————————————————————————————

class c02_int_to_float:
    def __init__(self):
        pass
    CATEGORY = gategory

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input_int": ("INT",),
            },
        }   
    
    OUTPUT_NODE = True
    RETURN_TYPES = ("FLOAT",)
    RETURN_NAMES = ("float",)

    FUNCTION = "test"
    def test(self,input_int):
        return {"result": (float(input_int),)}


NODE_CLASS_MAPPINGS = {"c02_int_to_float": c02_int_to_float,}
NODE_DISPLAY_NAME_MAPPINGS = {"c02_int_to_float":"int_to_float🦄",}