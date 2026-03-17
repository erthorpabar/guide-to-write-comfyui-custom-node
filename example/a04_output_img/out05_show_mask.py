"""展示mask"""
import os

# 动态获取路径
this_dir = os.path.dirname(__file__) # 当前路径
last1 = os.path.basename(this_dir) # 当前文件夹名称
last2 = os.path.basename(os.path.dirname(this_dir)) # 上级文件夹名称
gategory=f"{last2}🦄🦄🦄/{last1}" # 在comfyui中的目录：上级文件夹名称/当前文件夹名称
# ————————————————————————————————————————————————
from nodes import SaveImage
import folder_paths

import torch
import random


class out05_show_mask(SaveImage):
    def __init__(self):
        self.output_dir = folder_paths.get_temp_directory()
        self.type = "temp"
        self.prefix_append = "_temp_" + ''.join(random.choice("abcdefghijklmnopqrstupvxyz1234567890") for x in range(5))
        self.compress_level = 4

    CATEGORY = gategory

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                 "mask": ("MASK",),
            },
        }   
    
    OUTPUT_NODE = True

    FUNCTION = "test"
    def test(self, mask):
        if mask.dim() == 2:
            mask = torch.unsqueeze(mask, 0)
        preview = mask.reshape((-1, 1, mask.shape[-2], mask.shape[-1])).movedim(1, -1).expand(-1, -1, -1, 3)
        return self.save_images(preview, "MaskPreview")

NODE_CLASS_MAPPINGS = {"out05_show_mask": out05_show_mask,}
NODE_DISPLAY_NAME_MAPPINGS = {"out05_show_mask":"show_mask🦄",}
