"""获取图片尺寸"""
import os
# 动态获取路径
this_dir = os.path.dirname(__file__) # 当前路径
last1 = os.path.basename(this_dir) # 当前文件夹名称
last2 = os.path.basename(os.path.dirname(this_dir)) # 上级文件夹名称
gategory=f"{last2}🦄🦄🦄/{last1}" # 在comfyui中的目录：上级文件夹名称/当前文件夹名称
# ————————————————————————————————————————————————

class is03_img_get_size:
    def __init__(self):
        pass
    CATEGORY = gategory

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),

            },
        }   
    
    OUTPUT_NODE = True
    RETURN_TYPES = ("INT", "INT", "INT",)
    RETURN_NAMES = ("width", "height", "count")

    FUNCTION = "test"
    def test(self,image):
        return (image.shape[2], image.shape[1], image.shape[0])


NODE_CLASS_MAPPINGS = {"is03_img_get_size": is03_img_get_size,}
NODE_DISPLAY_NAME_MAPPINGS = {"is03_img_get_size":"img_get_size🦄",}