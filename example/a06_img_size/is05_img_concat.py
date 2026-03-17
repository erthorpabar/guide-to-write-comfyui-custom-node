"""图片合并，不裁剪"""
import os
# 动态获取路径
this_dir = os.path.dirname(__file__) # 当前路径
last1 = os.path.basename(this_dir) # 当前文件夹名称
last2 = os.path.basename(os.path.dirname(this_dir)) # 上级文件夹名称
gategory=f"{last2}🦄🦄🦄/{last1}" # 在comfyui中的目录：上级文件夹名称/当前文件夹名称
# ————————————————————————————————————————————————
import torch

class is05_img_concat:
    def __init__(self):
        pass
    CATEGORY = gategory

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image1": ("IMAGE",),
                "image2": ("IMAGE",),
                "position": (['right','down','left','up',],{"default": 'right'}),
            },
        }   
    
    OUTPUT_NODE = True
    RETURN_TYPES = ("IMAGE","INT","INT")
    RETURN_NAMES = ("image","new_height","new_width")

    FUNCTION = "test"
    def test(self, image1, image2, position):
        # 获取两张图片的尺寸
        _, height1, width1, _ = image1.shape
        _, height2, width2, _ = image2.shape

        # 在拼接前调整图片尺寸
        if position == 'right' or position == 'left': # 左右拼接，高度需要相等
            # 水平拼接时，需要确保高度相同
            if height1 != height2:
                new_width2 = int(width2 * height1 / height2) # 调整第二张图的宽度 h1/h2 是需要缩放的比例
                image2 = image2.permute(0, 3, 1, 2)  # [B,H,W,C] -> [B,C,H,W]
                image2 = torch.nn.functional.interpolate(image2, size=(height1, new_width2), mode="bilinear") # 缩放
                image2 = image2.permute(0, 2, 3, 1)  # [B,C,H,W] -> [B,H,W,C]


        elif position == 'down' or position == 'up': # 上下拼接，宽度需要相等
            # 垂直拼接时，需要确保宽度相同
            if width1 != width2:
                new_height2 = int(height2 * width1 / width2) # 调整第二张图的高度 w1/w2 是需要缩放的比例
                image2 = image2.permute(0, 3, 1, 2) # [B,H,W,C] -> [B,C,H,W]
                image2 = torch.nn.functional.interpolate(image2, size=(new_height2, width1), mode="bilinear") # 缩放
                image2 = image2.permute(0, 2, 3, 1) # [B,C,H,W] -> [B,H,W,C]
     

        # 拼接
        if position == 'right':
            image = torch.cat((image1, image2), dim=2)
        elif position == 'down':
            image = torch.cat((image1, image2), dim=1)
        elif position == 'left':
            image = torch.cat((image2, image1), dim=2)
        elif position == 'up':
            image = torch.cat((image2, image1), dim=1)

        _, new_height, new_width, _ = image.shape

        return (image,new_height,new_width)
         


NODE_CLASS_MAPPINGS = {"is05_img_concat": is05_img_concat,}
NODE_DISPLAY_NAME_MAPPINGS = {"is05_img_concat":"img_concat🦄",}




