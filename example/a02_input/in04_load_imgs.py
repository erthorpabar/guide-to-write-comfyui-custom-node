"""批量加载图片"""
import os
# 动态获取路径
this_dir = os.path.dirname(__file__) # 当前路径
last1 = os.path.basename(this_dir) # 当前文件夹名称
last2 = os.path.basename(os.path.dirname(this_dir)) # 上级文件夹名称
gategory=f"{last2}🦄🦄🦄/{last1}" # 在comfyui中的目录：上级文件夹名称/当前文件夹名称
# ————————————————————————————————————————————————
import numpy as np
import torch
from PIL import Image, ImageOps


class in04_load_imgs:
    def __init__(self):
        pass
    CATEGORY = gategory

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image_path": ("STRING", {"default": ""}),
            },
            # "optional": {
            #     "image_load_cap": ("INT", {"default": 0, "min": 0, "step": 1}),
            #     "start_index": ("INT", {"default": 0, "min": 0, "step": 1}),
            #     "load_always": ("BOOLEAN", {"default": False, "label_on": "enabled", "label_off": "disabled"}),
            # }
        }   
    
    OUTPUT_IS_LIST = (True, True, True)
    RETURN_TYPES = ("IMAGE", "MASK", "STRING")
    RETURN_NAMES = ("image", "mask", "file_path")

    FUNCTION = "test"
    def test(self, image_path):
        if not os.path.isdir(image_path):
            raise FileNotFoundError(f"Directory '{image_path}' cannot be found.")
        dir_files = os.listdir(image_path)
        if len(dir_files) == 0:
            raise FileNotFoundError(f"No files in directory '{image_path}'.")

        # Filter files by extension
        valid_extensions = ['.jpg', '.jpeg', '.png', '.webp']
        dir_files = [f for f in dir_files if any(f.lower().endswith(ext) for ext in valid_extensions)]

        dir_files = sorted(dir_files)
        dir_files = [os.path.join(image_path, x) for x in dir_files]

        images = []
        masks = []
        file_paths = []

        for image_path in dir_files:
            if os.path.isdir(image_path):
                continue
            i = Image.open(image_path)
            i = ImageOps.exif_transpose(i)
            image = i.convert("RGB")
            image = np.array(image).astype(np.float32) / 255.0
            image = torch.from_numpy(image)[None,]

            if 'A' in i.getbands():
                mask = np.array(i.getchannel('A')).astype(np.float32) / 255.0
                mask = 1. - torch.from_numpy(mask)
            else:
                mask = torch.zeros((64, 64), dtype=torch.float32, device="cpu")

            images.append(image) 
            masks.append(mask)
            file_paths.append(str(image_path))

        return (images, masks, file_paths)
        # return (images,)

NODE_CLASS_MAPPINGS = {"in04_load_imgs": in04_load_imgs,}
NODE_DISPLAY_NAME_MAPPINGS = {"in04_load_imgs":"load_imgs🦄",}
