"""透明图叠加"""

import os
# 动态获取路径
this_dir = os.path.dirname(__file__) # 当前路径
last1 = os.path.basename(this_dir) # 当前文件夹名称
last2 = os.path.basename(os.path.dirname(this_dir)) # 上级文件夹名称
gategory=f"{last2}🦄🦄🦄/{last1}" # 在comfyui中的目录：上级文件夹名称/当前文件夹名称
# ————————————————————————————————————————————————
import torch
import numpy as np
from PIL import Image, ImageOps


# Tensor to PIL (grabbed from WAS Suite)
def tensor2pil(image: torch.Tensor) -> Image.Image:
    return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))

# Convert PIL to Tensor (grabbed from WAS Suite)
def pil2tensor(image: Image.Image) -> torch.Tensor:
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)


class io01_img_overlay:
    def __init__(self):
        pass
    CATEGORY = gategory

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "up_image": ("IMAGE",), # 叠加图
                "base_image": ("IMAGE",), # 底图
                "X": ("INT", {"default": 0, "min": -48000, "max": 48000, "step": 1}), # X轴偏移 = 底图宽-叠加图宽
                "Y": ("INT", {"default": 0, "min": -48000, "max": 48000, "step": 1}), # Y轴偏移 = 底图高-叠加图高
            },
            "optional": {
                "mask": ("MASK",), # 白色为改动区域，黑色为不改动区域。或者白色为透明区域，黑色为不透明区域。
            }
        }   
    
    OUTPUT_NODE = True
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)

    FUNCTION = "test"
    def test(self,up_image,base_image,X,Y,mask=None):

        # 叠加图 转换数据类型
        up_image = tensor2pil(up_image)

        # 为叠加图添加Alpha通道
        up_image = up_image.convert('RGBA')
        up_image.putalpha(Image.new("L", up_image.size, 255))

        # 如果连接了mask，检查叠加图是否有Alpha通道
        if mask is not None:
            mask = tensor2pil(mask)
            mask = mask.resize(up_image.size)
            up_image.putalpha(ImageOps.invert(mask))

        
        # 沿第一个维度分割基础图像张量，得到张量列表 torch.tensor
        base_image_list = torch.unbind(base_image, dim=0)

        # 批量处理叠加
        image_list = []
        for tensor in base_image_list:
            # 将张量转换为PIL图像
            image = tensor2pil(tensor)
            
            # 合并 底图和叠加图
            if mask is None:
                image.paste(up_image, (X,Y))
            else:
                image.paste(up_image, (X,Y), up_image)
            
            # 将PIL图像转换回张量
            processed_tensor = pil2tensor(image)

            # 添加到列表中
            image_list.append(processed_tensor)
        
        # 合并成整体tensor
        base_image = torch.stack([tensor.squeeze() for tensor in image_list])

        # 返回编辑后的基础图像
        return (base_image,)


NODE_CLASS_MAPPINGS = {"io01_img_overlay": io01_img_overlay,}
NODE_DISPLAY_NAME_MAPPINGS = {"io01_img_overlay":"img_overlay🦄",}
