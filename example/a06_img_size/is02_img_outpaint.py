"""扩图向外添加像素"""
import os
# 动态获取路径
this_dir = os.path.dirname(__file__) # 当前路径
last1 = os.path.basename(this_dir) # 当前文件夹名称
last2 = os.path.basename(os.path.dirname(this_dir)) # 上级文件夹名称
gategory=f"{last2}🦄🦄🦄/{last1}" # 在comfyui中的目录：上级文件夹名称/当前文件夹名称
# ————————————————————————————————————————————————
import torch
import torch.nn.functional as F


class is02_img_outpaint:
    def __init__(self):
        pass
    CATEGORY = gategory

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "left": ("INT", {"default": 0, "min": 0, "max": 1024, "step": 8}),    # 左侧填充像素
                "top": ("INT", {"default": 0, "min": 0, "max": 1024, "step": 8}),     # 顶部填充像素
                "right": ("INT", {"default": 0, "min": 0, "max": 1024, "step": 8}),   # 右侧填充像素
                "bottom": ("INT", {"default": 0, "min": 0, "max": 1024, "step": 8}),  # 底部填充像素

                "feathering": ("INT", {"default": 0, "min": 0, "max": 1024, "step": 8}),  # 羽化效果的像素范围
            },
            # "optional": {
            #     "mask": ("MASK",),  # 可选的遮罩输入
            # }
        }   
    
    OUTPUT_NODE = True
    RETURN_TYPES = ("IMAGE","MASK","INT","INT")
    RETURN_NAMES = ("image","mask","new_height","new_width")

    FUNCTION = "test"
    def test(self,image,left,top,right,bottom,feathering,mask=None):

        # ————————————————对 img的处理————————————————

        # 获取输入图像的尺寸
        B, H, W, C = image.size()

        # 创建新的扩展图像，填充值为0.5（灰色）
        new_image = torch.ones((B, H + top + bottom, W + left + right, C),dtype=torch.float32,) * 0.5

        # 将原始图像复制到新图像的中心位置
        new_image[:, top:top + H, left:left + W, :] = image

        # ————————————————对 mask的处理————————————————
        # 如果是全黑mask，则视为None
        if mask is not None:
            if torch.allclose(mask, torch.zeros_like(mask)): 
                mask = None

        if mask is None:
            new_mask = torch.ones((B, H + top + bottom, W + left + right),dtype=torch.float32,) # 扩图后的大小，白mask
            t = torch.zeros((B, H, W),dtype=torch.float32,) # 原图大小，黑色mask
        else: # 如果提供了mask，则对其进行扩展
            mask = F.pad(mask, (left, right, top, bottom), mode='constant', value=0)
            mask = 1 - mask
            t = torch.zeros_like(mask)

        # 处理羽化效果
        if feathering > 0 and feathering * 2 < H and feathering * 2 < W:
            # 遍历图像的每个像素，计算羽化效果
            for i in range(H):
                for j in range(W):
                    dt = i if top != 0 else H
                    db = H - i if bottom != 0 else H
                    dl = j if left != 0 else W
                    dr = W - j if right != 0 else W

                    d = min(dt, db, dl, dr)

                    if d >= feathering:
                        continue

                    v = (feathering - d) / feathering   

                    if mask is None:
                        t[:, i, j] = v * v
                    else:
                        t[:, top + i, left + j] = v * v
                    


        # ————————————————返回————————————————
        _, new_height, new_width, _ = new_image.shape
        if mask is None:
            new_mask[:, top:top + H, left:left + W] = t
            return (new_image,new_mask,new_height,new_width)
        else:
            return (new_image,mask,new_height,new_width)


NODE_CLASS_MAPPINGS = {"is02_img_outpaint": is02_img_outpaint,}
NODE_DISPLAY_NAME_MAPPINGS = {"is02_img_outpaint":"img_outpaint🦄",}