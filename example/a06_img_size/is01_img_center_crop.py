"""裁剪图片
在裁剪与缩放之间，选择最佳比例
保证输出为指定的长宽

"""


import os
# 动态获取路径
this_dir = os.path.dirname(__file__) # 当前路径
last1 = os.path.basename(this_dir) # 当前文件夹名称
last2 = os.path.basename(os.path.dirname(this_dir)) # 上级文件夹名称
gategory=f"{last2}🦄🦄🦄/{last1}" # 在comfyui中的目录：上级文件夹名称/当前文件夹名称
# ————————————————————————————————————————————————

import torch
import numpy as np
from PIL import Image

class is01_img_center_crop:
    def __init__(self):
        pass
    CATEGORY = gategory

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),
                "to_width": ("INT",{"default":1024,"min":0}), # 裁剪目标尺寸
                "to_height": ("INT",{"default":1024,"min":0}), # 裁剪目标尺寸
            },
        }   
    
    # OUTPUT_NODE = True
    RETURN_TYPES = ("IMAGE",)
    OUTPUT_IS_LIST = (True,)


    FUNCTION = "test"
    def test(self,images,to_width,to_height,):
        results = []

       
        for image in images:
            # 1 转换数据格式 torch -> numpy -> PIL
            i = 255. * image.cpu().numpy() # 转移到cpu，nnumpy格式，像素从[0-1]缩放到[0-255]
            # img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8)).convert("RGB") # 0-255防溢出，float->uint8，确认为rgb格式，numpy->pil图像

            # 检查通道数并相应处理
            if i.shape[2] == 4:  # 如果有4个通道（RGBA）
                img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8), 'RGBA')  # 0-255防溢出，float->uint8，确认为rgb格式，numpy->pil图像
            else:  # 如果是3通道（RGB）
                img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8), 'RGB') # 0-255防溢出，float->uint8，确认为rgb格式，numpy->pil图像

            # ————————————————计算与裁剪————————————————————
            # 2 缩放
            # 当前宽高 缩放至 目标宽高
            img_width, img_height = img.size # 当前宽高
            scale = img_width / img_height # 当前宽高比
            
            target_width, target_height = to_width, to_height # 目标宽高
            target_scale = target_width / target_height # 目标宽高比

            # 调整宽高的方法
            # 如果目标更宽
            if target_scale > scale: # 调整完更宽
                target_width = max(int(target_height * scale), to_width)
                target_height = int(img_height * (target_width / img_width))
            # 如果目标更高
            elif target_scale <= scale: # 调整完更高
                target_height = max(int(target_width / scale), to_height)
                target_width = int(img_width * (target_height / img_height))

            # 缩放 pil 格式
            crop_img = img.resize((target_width, target_height), Image.LANCZOS)

            # 3 对于超出输出尺寸的部分，进行居中裁剪
            if target_width > to_width or target_height > to_height:
                left = (target_width - to_width) // 2 # 左
                top = (target_height - to_height) // 2 # 上
                right = left + to_width # 右
                bottom = top + to_height # 下
                crop_img = crop_img.crop((left, top, right, bottom)) # 裁剪
            
            #——————————————————————————————————————————————————

            # 4 转换回数据格式 PIL -> numpy -> torch
            crop_img = np.array(crop_img).astype(np.float32) / 255.0 # PIL -> numpy 像素值缩放到[0-1]
            crop_img = torch.from_numpy(crop_img)[None,] # numpy -> torch 在第0维度增加一个维度，[h,w,c] -> [1,h,w,c]
            results.append(crop_img) # 添加到结果列表
        
        return (results,)

NODE_CLASS_MAPPINGS = {"is01_img_center_crop": is01_img_center_crop,}
NODE_DISPLAY_NAME_MAPPINGS = {"is01_img_center_crop":"img_center_crop🦄",}


"""调整图片大小的其他方法"""
# # 检查不同的调整选项
    # if overlay_resize != "None":  # 如果需要调整叠加图像的大小
    #     # 提取叠加图像的大小并存储在元组 "overlay_image_size" (宽x高)
    #     overlay_image_size = overlay_image.size()  # 获取叠加图像的尺寸
    #     overlay_image_size = (overlay_image_size[2], overlay_image_size[1])  # 转换为 (宽, 高)
    #     if overlay_resize == "Fit":  # 如果选择适应
    #         h_ratio = base_image.size()[1] / overlay_image_size[1]  # 计算高度比例
    #         w_ratio = base_image.size()[2] / overlay_image_size[0]  # 计算宽度比例
    #         ratio = min(h_ratio, w_ratio)  # 取最小比例以保持图像比例
    #         overlay_image_size = tuple(round(dimension * ratio) for dimension in overlay_image_size)  # 调整叠加图像大小
    #     elif overlay_resize == "Resize by rescale_factor":  # 如果选择按缩放因子调整
    #         overlay_image_size = tuple(int(dimension * rescale_factor) for dimension in overlay_image_size)  # 根据缩放因子调整大小
    #     elif overlay_resize == "Resize to width & heigth":  # 如果选择调整到指定宽高
    #         overlay_image_size = (size[0], size[1])  # 设置为指定的宽高

    #     samples = overlay_image.movedim(-1, 1)  # 调整维度以适应后续处理
    #     overlay_image = comfy.utils.common_upscale(samples, overlay_image_size[0], overlay_image_size[1], resize_method, False)  # 进行图像上采样
    #     overlay_image = overlay_image.movedim(1, -1)  # 恢复维度顺序











