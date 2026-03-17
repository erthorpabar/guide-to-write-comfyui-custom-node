"""生成随机整数"""
import os
# 动态获取路径
this_dir = os.path.dirname(__file__) # 当前路径
last1 = os.path.basename(this_dir) # 当前文件夹名称
last2 = os.path.basename(os.path.dirname(this_dir)) # 上级文件夹名称
gategory=f"{last2}🦄🦄🦄/{last1}" # 在comfyui中的目录：上级文件夹名称/当前文件夹名称
# ————————————————————————————————————————————————
import random
class in03_random_int:
    def __init__(self):
        pass
    CATEGORY = gategory

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "int": ("INT", {"default": 1,"step": 1}),
            },
        }   
    
    OUTPUT_NODE = True
    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("int",)

    FUNCTION = "test"
    def test(self,int):
        seed = random.randint(0, 0xffffffffffffffff) 
        print(int)
        return (seed,)


NODE_CLASS_MAPPINGS = {"in03_random_int": in03_random_int,}
NODE_DISPLAY_NAME_MAPPINGS = {"in03_random_int":"random_int🦄",}