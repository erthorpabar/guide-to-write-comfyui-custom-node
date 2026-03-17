"""调节图片大小，不裁剪
按照长或宽，等比缩放，不破坏比例
"""
import os
# 动态获取路径
this_dir = os.path.dirname(__file__) # 当前路径
last1 = os.path.basename(this_dir) # 当前文件夹名称
last2 = os.path.basename(os.path.dirname(this_dir)) # 上级文件夹名称
gategory=f"{last2}🦄🦄🦄/{last1}" # 在comfyui中的目录：上级文件夹名称/当前文件夹名称
# ————————————————————————————————————————————————
import torch

class is06_img_resize:
    def __init__(self):
        pass
    CATEGORY = gategory

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "to_width": ("INT",{"default":1024,"min":0}), # 裁剪目标尺寸
                "to_height": ("INT",{"default":1024,"min":0}), # 裁剪目标尺寸
                "mode": (["width_first","height_first"],{"default": 'width_first'}),
            },
        }   
    
    OUTPUT_NODE = True
    RETURN_TYPES = ("IMAGE","INT","INT")
    RETURN_NAMES = ("image","new_width","new_height")

    FUNCTION = "test"
    def test(self,image,to_width,to_height,mode):

        # 获取图片的宽高
        _, height, width, _ = image.shape

        # 根据模式调整宽高
        if mode == "width_first": # 宽度优先，则需要计算高度
            new_height = int(height * to_width / width)
            new_width = to_width
            image = image.permute(0, 3, 1, 2)  # [B,H,W,C] -> [B,C,H,W]
            image = torch.nn.functional.interpolate(image, size=(new_height, new_width), mode="bilinear")
            image = image.permute(0, 2, 3, 1)  # [B,C,H,W] -> [B,H,W,C]

        elif mode == "height_first": # 高度优先，则需要计算宽度
            new_width = int(width * to_height / height)
            new_height = to_height
            image = image.permute(0, 3, 1, 2)  # [B,H,W,C] -> [B,C,H,W]
            image = torch.nn.functional.interpolate(image, size=(new_height, new_width), mode="bilinear")
            image = image.permute(0, 2, 3, 1)  # [B,C,H,W] -> [B,H,W,C]

        return (image,new_width,new_height)
        


NODE_CLASS_MAPPINGS = {"is06_img_resize": is06_img_resize,}
NODE_DISPLAY_NAME_MAPPINGS = {"is06_img_resize":"img_resize🦄",}