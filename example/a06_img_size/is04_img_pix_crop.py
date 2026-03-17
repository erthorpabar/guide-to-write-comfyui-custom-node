"""按照像素裁剪
按横竖裁剪
"""
import os
# 动态获取路径
this_dir = os.path.dirname(__file__) # 当前路径
last1 = os.path.basename(this_dir) # 当前文件夹名称
last2 = os.path.basename(os.path.dirname(this_dir)) # 上级文件夹名称
gategory=f"{last2}🦄🦄🦄/{last1}" # 在comfyui中的目录：上级文件夹名称/当前文件夹名称
# ————————————————————————————————————————————————

class is04_img_pix_crop:
    def __init__(self):
        pass
    CATEGORY = gategory

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "left": ("INT", {"default": 0,"min": 0,"max": 4096,"step": 8}),
                "right": ("INT", {"default": 0,"min": 0,"max": 4096,"step": 8}),
                "top": ("INT", {"default": 0,"min": 0,"max": 4096,"step": 8}),
                "bottom": ("INT", {"default": 0,"min": 0,"max": 4096,"step": 8}),
            },
        }   
    
    OUTPUT_NODE = True
    RETURN_TYPES = ("IMAGE","INT","INT")
    RETURN_NAMES = ("image_a","a_height","a_width")

    FUNCTION = "test"
    def test(self,image,left,right,top,bottom):
        
        # 1 获取图像的宽高
        _,height,width,_ = image.shape 

        # 2 调整为8的倍数
        left = left // 8 * 8
        right = right // 8 * 8
        top = top // 8 * 8
        bottom = bottom // 8 * 8
        
        # 3 计算新边界，左上角为0，0，右下角为width，height
        # 0 值代表不动
        n_left = 0 + left
        n_right = width - right
        n_top = 0 + top
        n_bottom = height - bottom

        # 4 验证是否超出范围
        if n_left > n_right or n_top > n_bottom:
            raise ValueError(f"裁剪范围超出图像范围")

        # 5 选择的裁剪范围
        img_a = image[:, n_top:n_bottom, n_left:n_right, :]
        _, a_height, a_width, _ = img_a.shape


        return (img_a, a_height, a_width,)


NODE_CLASS_MAPPINGS = {"is04_img_pix_crop": is04_img_pix_crop,}
NODE_DISPLAY_NAME_MAPPINGS = {"is04_img_pix_crop":"img_pix_crop🦄",}







