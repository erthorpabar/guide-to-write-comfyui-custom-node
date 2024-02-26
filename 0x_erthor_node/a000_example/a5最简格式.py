import os
# 动态获取路径
dir = os.path.dirname(__file__) # 当前脚本目录
last1=os.path.basename(dir) # 最后一个目录
last2=os.path.basename(os.path.dirname(dir)) # 倒数第二个目录
gategory=f"{last2}👾👾👾/{last1}" # 动态获取的当前文件夹路径

class a5:
    def __init__(self):
        pass
    CATEGORY = gategory

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {

            },
        }

    OUTPUT_NODE = True
    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("1整数",)

    FUNCTION = "test"
    def test(self,):
        pass
