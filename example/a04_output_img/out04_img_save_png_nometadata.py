"""png保存无图片生成元数据"""
import os
# 动态获取路径
this_dir = os.path.dirname(__file__)  # 获取当前文件所在目录的路径
last1 = os.path.basename(this_dir)    # 获取当前文件夹的名称
last2 = os.path.basename(os.path.dirname(this_dir))  # 获取上级文件夹的名称
gategory=f"{last2}🦄🦄🦄/{last1}"    # 设置在comfyui中的目录路径
# ————————————————————————————————————————————————
# 导入必要的库
import folder_paths
from PIL import Image
import numpy as np


class out04_img_save_png_nometadata:
    def __init__(self):
        pass
    
    CATEGORY = gategory

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),
                "pic_level":  ("INT", {"default": 6, "min": 0, "max": 9, "step": 1}),
                "filename_prefix": ("STRING", {"default": "ComfyUI"}),
            },
        }

    RETURN_TYPES = ()
    OUTPUT_NODE = True

    FUNCTION = "save_images"
    def save_images(self, images, filename_prefix, pic_level):

        # （绝对路径，前缀，总数量，subfolder默认为空字符，前缀）
        p = folder_paths.get_save_image_path(filename_prefix, folder_paths.get_output_directory(), images[0].shape[1], images[0].shape[0])
        full_path = p[0]
        prefix = p[1]
        counter = p[2]
        subfolder = p[3]
        filename_prefix = p[4]
        
        
        results = list()

        for (batch_number, image) in enumerate(images):
            i = 255. * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))

            prefix_batch_num = prefix.replace("%batch_num%", str(batch_number))
            file_name = f"{prefix_batch_num}_{counter:05}_.png"  # 


            # ————————————保存————————————
            # 保存为png
            img.save(os.path.join(full_path, file_name), 
                     compress_level=pic_level
            )
            

            # 显示在ui上
            results.append({
                "filename": file_name,
                "subfolder": subfolder,
                "type": "output"
            })

            # 计数器+1
            counter += 1

        return { "ui": { "images": results } }


NODE_CLASS_MAPPINGS = {"out04_img_save_png_nometadata": out04_img_save_png_nometadata,}
NODE_DISPLAY_NAME_MAPPINGS = {"out04_img_save_png_nometadata":"img_save_png_nometadata🦄",}





