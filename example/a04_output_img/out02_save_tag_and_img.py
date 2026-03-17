"""保存tag和图片"""
import os
# 动态获取路径
this_dir = os.path.dirname(__file__) # 当前路径
last1 = os.path.basename(this_dir) # 当前文件夹名称
last2 = os.path.basename(os.path.dirname(this_dir)) # 上级文件夹名称
gategory=f"{last2}🦄🦄🦄/{last1}" # 在comfyui中的目录：上级文件夹名称/当前文件夹名称
# ————————————————————————————————————————————————
from PIL import Image
import numpy as np
import folder_paths
import re

class out02_save_tag_and_img:
    def __init__(self):
        pass
    CATEGORY = gategory

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "tag": ("STRING", {"default": "","forceInput": True}),
                "folder_name": ("STRING", {"default": "tag_img"}),
                "pre_fix": ("STRING", {"default": "aaa"}),
                "img_format": (["png", "jpg"],),

            },
        }   
    
    OUTPUT_NODE = True
    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("int",)

    FUNCTION = "test"
    def test(self,image,tag,folder_name,pre_fix,img_format):

        # 计数器和输出路径
        output = folder_paths.get_output_directory() # 输出根目录
        # 输出文件夹,没有则创建
        output = os.path.join(output, folder_name)
        os.makedirs(output, exist_ok=True) 
        print(f"输出根目录: {output}")
        a = 0  # 计数器
        matcher = re.compile(f"{re.escape(pre_fix)}_(\d+)_?\.[a-zA-Z0-9]+")
        for fff in os.listdir(output):
            match = matcher.fullmatch(fff)
            if match:
                a = max(a,int(match.group(1)))
        a += 1

        a = f"{a:05}" # 显示为5位数

        filename = f"{pre_fix}_{a}.{img_format}" # 图片名称
        img_output_file = os.path.join(output, filename) # 图片完整输出路径
        img_output_file = os.path.normpath(img_output_file) # 规范化路径
        tag_filename = f"{pre_fix}_{a}.txt" # tag对应名称
        tag_output_file = os.path.join(output, tag_filename) # tag完整输出路径
        tag_output_file = os.path.normpath(tag_output_file) # 规范化路径


        # 保存tag.txt
        with open(tag_output_file, "w") as f:
            f.write(tag)

        # 保存图片
        i = 255. * image[0].cpu().numpy()
        img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))

        # png为无损压缩
        if img_format == "png":
            img.save(img_output_file, format="PNG", compress_level=0)  # 使用无损压缩
        # jpg为有损压缩
        elif img_format == "jpg":
            if img.mode == "RGBA": # 透明图转换
                img = img.convert("RGB")
            img.save(img_output_file, format="JPEG", quality=100, optimize=False, subsampling=0)  # 最高质量JPEG设置

        
        results = [{"filename":filename,
                   "subfolder":folder_name,
                   "type":"output"}]

        return { "ui": { "images": results } }


NODE_CLASS_MAPPINGS = {"out02_save_tag_and_img": out02_save_tag_and_img,}
NODE_DISPLAY_NAME_MAPPINGS = {"out02_save_tag_and_img":"save_tag_and_img🦄",}
