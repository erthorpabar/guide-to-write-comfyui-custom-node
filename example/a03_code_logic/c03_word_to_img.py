"""透明背景文字"""
import os
# 动态获取路径
this_dir = os.path.dirname(__file__) # 当前路径
last1 = os.path.basename(this_dir) # 当前文件夹名称
last2 = os.path.basename(os.path.dirname(this_dir)) # 上级文件夹名称
gategory=f"{last2}🦄🦄🦄/{last1}" # 在comfyui中的目录：上级文件夹名称/当前文件夹名称
# ————————————————————————————————————————————————
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import glob
from typing import List, Optional, Union
import torch
import numpy as np

def pil2tensor(image: Union[Image.Image, List[Image.Image]]) -> torch.Tensor:
    if isinstance(image, list):
        return torch.cat([pil2tensor(img) for img in image], dim=0)

    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)




# ——————————————————————————构建字体文件路径和字典——————————————————————————
fonts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ttfs") # 上级文件夹路径 下 的ttfs文件夹

suffix = ["*.ttf", "*.otf", "*.woff", "*.woff2", "*.eot"] # 需要搜索的后缀名称
fonts_path = []
for suf in suffix:
    found_fonts = glob.glob(os.path.join(fonts_dir, suf)) # 找到的文件的绝对路径str
    fonts_path.extend(found_fonts) # 添加路径到列表

dict = {}
for path in fonts_path:
    name = Path(path).stem # 转化成path文件，使用stem获取文件名称
    dict[name] = path

font_names = list(dict.keys()) # 获取字典的键，即字体名称




class c03_word_to_img:
    def __init__(self):
        pass

    CATEGORY = gategory

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "font": (font_names,),
                "font_size": ("INT", {"default": 100, "min": 1, "max": 1000, "step": 1}), # 文字大小
                "text": ("STRING", {"default": "",}), # 文字
                "font_color_hex_str": ("STRING", {"default": "#FFFFFF"}), # 文字颜色
                "outline_size": ("INT", {"default": 1, "min": 0, "max": 20, "step": 1}), # 边框宽度，20为纯色背景
                "outline_color_hex_str": ("STRING", {"default": "#000000"}), # 边框颜色
            },
        }

    OUTPUT_NODE = True
    RETURN_TYPES = ("IMAGE","INT","INT")
    RETURN_NAMES = ("image-rgba","width","height")

    FUNCTION = "test"
    def test(self, font, font_size, text, font_color_hex_str, outline_size, outline_color_hex_str):
        #————————————————————————字体加载————————————————————————
        # 字体路径
        font_path = dict[font]

        # 加载字体 = 字体路径 + 文字大小 
        font = ImageFont.truetype(font_path, font_size)

        #————————————————————————创建临时画布————————————————————————
        # RGBA模式：R红,G绿,B蓝,A透明度
        # 创建1x1像素的临时图像用于计算文字尺寸
        # (0,0,0,0)表示完全透明
        temp_img = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
        temp_draw = ImageDraw.Draw(temp_img)

        #————————————————————————分析多行文本————————————————————————
        # 分割多行文本
        lines = text.split('\n')
        
        # 计算每行文本的边界框，找出最大宽度和总高度
        max_width = 0
        total_height = 0
        line_bboxes = []
        line_heights = []
        
        for line in lines:
            # 即使是空行，也要计算其高度
            measure_line = " " if not line else line
            bbox = temp_draw.textbbox((0, 0), measure_line, font=font)
            line_width = bbox[2] - bbox[0]
            line_height = bbox[3] - bbox[1]
            
            max_width = max(max_width, line_width)
            line_bboxes.append(bbox)
            line_heights.append(line_height)
            
            # 第一行直接设置高度，后续行累加（包括行间距）
            if total_height == 0:
                total_height = line_height
            else:
                # 行间距设为字体高度的0.5 - 这里可能需要增加行间距
                line_spacing = int(line_height * 0.5)  # 增加到0.5，使换行更明显
                total_height += line_height + line_spacing

        #————————————————————————计算最终尺寸————————————————————————
        # 预留描边空间和额外底部空间
        padding_sides = outline_size * 2 + 10  # 左右两侧的padding，增加额外空间
        padding_top = outline_size * 2 + 10    # 顶部padding，增加额外空间
        padding_bottom = outline_size * 4 + 20  # 底部额外padding，大幅增加以防止切割
        
        # 计算最终图像尺寸
        img_width = max_width + padding_sides
        img_height = total_height + padding_top + padding_bottom
        
        #————————————————————————创建最终图像————————————————————————
        # 创建一个能容纳所有文字的透明图像
        img = Image.new("RGBA", (int(img_width), int(img_height)), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        #————————————————————————绘制文字————————————————————————
        # 绘制每行文字
        y_offset = padding_top  # 初始垂直偏移，从顶部padding开始
        
        for i, line in enumerate(lines):
            bbox = line_bboxes[i]
            line_height = line_heights[i]
            
            # 添加调试信息，打印每行文本内容
            print(f"绘制第{i+1}行: '{line}', y_offset={y_offset}")
            
            # 绘制当前行文字（即使是空行也保留其位置）
            draw.text(
                (-bbox[0] + padding_sides // 2, y_offset), 
                line,  # 直接使用原始行，包括空行
                fill=font_color_hex_str, 
                font=font,
                stroke_width=outline_size,
                stroke_fill=outline_color_hex_str
            )
            
            # 更新下一行的垂直偏移
            if i < len(lines) - 1:
                line_spacing = int(line_height * 0.5)  # 增加行间距，与上面保持一致
                y_offset += line_height + line_spacing

        #————————————————————————返回结果————————————————————————
        # 将PIL图像转换为ComfyUI可用的张量格式
        return (pil2tensor(img), int(img_width), int(img_height))

        # # textbbox返回文字的边界框坐标
        # # (0,0)是计算的参考点
        # # 返回值为(left, top, right, bottom)
        # text_bbox = temp_draw.textbbox((0, 0), text, font=font,) 


        # # 预留描边空间
        # padding = outline_size * 1
        
        # # 计算文字的实际宽度和高度，并为描边预留空间
        # text_width = text_bbox[2] - text_bbox[0] + padding   # 左右各预留outline_size的空间
        # text_height = text_bbox[3] - text_bbox[1] + padding  # 上下各预留outline_size的空间

        # # 创建一个刚好能容纳文字的透明图像
        # img = Image.new("RGBA", (int(text_width), int(text_height)), (0, 0, 0, 0))
        # draw = ImageDraw.Draw(img)

        # # 绘制文字
        # # -text_bbox[0]和-text_bbox[1]是为了补偿字体的基线偏移
        # # 比如某些字体可能有负的left或top值，需要向左或向上偏移以显示完整
        # draw.text(
        #     (-text_bbox[0] + outline_size, -text_bbox[1] + outline_size), 
        #     text, 
        #     fill=font_color_hex_str, 
        #     font=font,
        #     stroke_width=outline_size,
        #     stroke_fill=outline_color_hex_str
        # )

        # # 将PIL图像转换为ComfyUI可用的张量格式
        # return (pil2tensor(img),int(text_width),int(text_height))


NODE_CLASS_MAPPINGS = {"c03_word_to_img": c03_word_to_img,}
NODE_DISPLAY_NAME_MAPPINGS = {"c03_word_to_img":"word_to_img🦄",}













# class CR_SimpleBanner:
    
#     @classmethod
#     def INPUT_TYPES(s):
#         # 获取字体目录路径
#         font_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "fonts")       
#         # 获取所有TTF字体文件列表
#         file_list = [f for f in os.listdir(font_dir) if os.path.isfile(os.path.join(font_dir, f)) and f.lower().endswith(".ttf")]     
        
#         return {"required": {
#                     "image": ("IMAGE",),  # 输入图像
#                     #"image_opacity": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.1}),  # 已注释的图像透明度选项
#                     "banner_text": ("STRING", {"multiline": True, "default": "text"}),  # 横幅文字内容，支持多行
#                     "font_name": (file_list,),  # 字体选择，从字体目录获取
#                     "max_font_size": ("INT", {"default": 150, "min": 20, "max": 2048}),  # 最大字体大小
#                     "font_color": (COLORS,),  # 字体颜色，从预定义颜色列表中选择                
#                     "outline_thickness": ("INT", {"default": 0, "min": 0, "max": 500}),  # 文字轮廓粗细
#                     "outline_color": (COLORS,),  # 轮廓颜色
#                     # 以下是已注释的其他选项
#                     #"text_opacity": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.1}),
#                     #"drop_shadow_angle": ("INT", {"default": 0, "min": 0, "max": 500}),
#                     #"drop_shadow_offset": ("INT", {"default": 0, "min": 0, "max": 500}),
#                     #"drop_shadow_color": (COLORS,),
#                     #"drop_shadow_opacity": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.1}),
#                     #"wrap_text": (["true", "false"],),
#                     "margin_size": ("INT", {"default": 0, "min": 0, "max": 500}),  # 边距大小
#                 },
#                 "optional": {
#                     "font_color_hex": ("STRING", {"multiline": False, "default": "#000000"}),  # 可选的十六进制字体颜色
#                     "outline_color_hex": ("STRING", {"multiline": False, "default": "#000000"}),  # 可选的十六进制轮廓颜色
#                 }         
#     }

#     # 定义返回类型和名称
#     RETURN_TYPES = ("IMAGE", "STRING", )  # 返回处理后的图像和帮助信息
#     RETURN_NAMES = ("image", "show_help", )
#     FUNCTION = "make_banner"  # 指定处理函数
#     CATEGORY = icons.get("Comfyroll/Graphics/Template")  # 节点分类

#     def make_banner(self, image, banner_text,
#                   font_name, max_font_size, font_color,
#                   outline_thickness, outline_color, margin_size,
#                   font_color_hex='#000000', outline_color_hex='#000000'):

#         # 获取文字和轮廓的RGB颜色值
#         text_color = get_color_values(font_color, font_color_hex, color_mapping)  # 从预设颜色或十六进制值获取文字颜色
#         outline_color = get_color_values(outline_color, outline_color_hex, color_mapping)  # 从预设颜色或十六进制值获取轮廓颜色
        
#         total_images = []  # 存储处理后的所有图像
        
#         # 处理每一张输入图像
#         for img in image:
                    
#             # 将张量转换为PIL图像，并确保为RGBA模式（支持透明度）
#             back_image = tensor2pil(img).convert("RGBA")
#             size = back_image.width, back_image.height
#             #result_image = Image.new("RGB", size)  # 已注释的创建新图像

#             # 构建字体文件的完整路径
#             font_file = os.path.join("fonts", font_name)
#             resolved_font_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), font_file)
        
#             # 创建绘图上下文
#             draw = ImageDraw.Draw(back_image)
            
#             # 计算可绘制区域的宽度和高度（考虑边距）
#             area_width = back_image.width - (margin_size * 2)
#             area_height = back_image.width - (margin_size * 2)  # 注意：这里使用了width而不是height，可能是错误
     
#             # 获取适合区域的字体大小
#             font = get_font_size(draw, banner_text, area_width, area_height, resolved_font_path, max_font_size)

#             # 计算文字绘制位置（居中）
#             x = back_image.width // 2
#             y = back_image.height // 2

#             # 绘制文字，根据是否有轮廓选择不同的绘制方式
#             if outline_thickness > 0:
#                 # 带轮廓的文字
#                 draw.text((x, y), banner_text, fill=text_color, font=font, anchor='mm', 
#                           stroke_width=outline_thickness, stroke_fill=outline_color)
#             else:    
#                 # 无轮廓的文字
#                 draw.text((x, y), banner_text, fill=text_color, font=font, anchor='mm')

#             # 将PIL图像转换回张量格式
#             # 注意：这里将RGBA转换为RGB，丢失了透明通道
#             out_image = np.array(back_image.convert("RGB")).astype(np.float32) / 255.0
#             out_image = torch.from_numpy(out_image).unsqueeze(0)  # 添加批次维度
#             total_images.append(out_image)  # 添加到结果列表

#         # 将所有图像合并为一个批次
#         images_out = torch.cat(total_images, 0)

#         # 帮助文档链接class CR_SimpleBanner:
    
#     @classmethod
#     def INPUT_TYPES(s):
#         # 获取字体目录路径
#         font_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "fonts")       
#         # 获取所有TTF字体文件列表
#         file_list = [f for f in os.listdir(font_dir) if os.path.isfile(os.path.join(font_dir, f)) and f.lower().endswith(".ttf")]     
        
#         return {"required": {
#                     "image": ("IMAGE",),  # 输入图像
#                     #"image_opacity": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.1}),  # 已注释的图像透明度选项
#                     "banner_text": ("STRING", {"multiline": True, "default": "text"}),  # 横幅文字内容，支持多行
#                     "font_name": (file_list,),  # 字体选择，从字体目录获取
#                     "max_font_size": ("INT", {"default": 150, "min": 20, "max": 2048}),  # 最大字体大小
#                     "font_color": (COLORS,),  # 字体颜色，从预定义颜色列表中选择                
#                     "outline_thickness": ("INT", {"default": 0, "min": 0, "max": 500}),  # 文字轮廓粗细
#                     "outline_color": (COLORS,),  # 轮廓颜色
#                     # 以下是已注释的其他选项
#                     #"text_opacity": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.1}),
#                     #"drop_shadow_angle": ("INT", {"default": 0, "min": 0, "max": 500}),
#                     #"drop_shadow_offset": ("INT", {"default": 0, "min": 0, "max": 500}),
#                     #"drop_shadow_color": (COLORS,),
#                     #"drop_shadow_opacity": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.1}),
#                     #"wrap_text": (["true", "false"],),
#                     "margin_size": ("INT", {"default": 0, "min": 0, "max": 500}),  # 边距大小
#                 },
#                 "optional": {
#                     "font_color_hex": ("STRING", {"multiline": False, "default": "#000000"}),  # 可选的十六进制字体颜色
#                     "outline_color_hex": ("STRING", {"multiline": False, "default": "#000000"}),  # 可选的十六进制轮廓颜色
#                 }         
#     }

#     # 定义返回类型和名称
#     RETURN_TYPES = ("IMAGE", "STRING", )  # 返回处理后的图像和帮助信息
#     RETURN_NAMES = ("image", "show_help", )
#     FUNCTION = "make_banner"  # 指定处理函数
#     CATEGORY = icons.get("Comfyroll/Graphics/Template")  # 节点分类

#     def make_banner(self, image, banner_text,
#                   font_name, max_font_size, font_color,
#                   outline_thickness, outline_color, margin_size,
#                   font_color_hex='#000000', outline_color_hex='#000000'):

#         # 获取文字和轮廓的RGB颜色值
#         text_color = get_color_values(font_color, font_color_hex, color_mapping)  # 从预设颜色或十六进制值获取文字颜色
#         outline_color = get_color_values(outline_color, outline_color_hex, color_mapping)  # 从预设颜色或十六进制值获取轮廓颜色
        
#         total_images = []  # 存储处理后的所有图像
        
#         # 处理每一张输入图像
#         for img in image:
                    
#             # 将张量转换为PIL图像，并确保为RGBA模式（支持透明度）
#             back_image = tensor2pil(img).convert("RGBA")
#             size = back_image.width, back_image.height
#             #result_image = Image.new("RGB", size)  # 已注释的创建新图像

#             # 构建字体文件的完整路径
#             font_file = os.path.join("fonts", font_name)
#             resolved_font_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), font_file)
        
#             # 创建绘图上下文
#             draw = ImageDraw.Draw(back_image)
            
#             # 计算可绘制区域的宽度和高度（考虑边距）
#             area_width = back_image.width - (margin_size * 2)
#             area_height = back_image.width - (margin_size * 2)  # 注意：这里使用了width而不是height，可能是错误
     
#             # 获取适合区域的字体大小
#             font = get_font_size(draw, banner_text, area_width, area_height, resolved_font_path, max_font_size)

#             # 计算文字绘制位置（居中）
#             x = back_image.width // 2
#             y = back_image.height // 2

#             # 绘制文字，根据是否有轮廓选择不同的绘制方式
#             if outline_thickness > 0:
#                 # 带轮廓的文字
#                 draw.text((x, y), banner_text, fill=text_color, font=font, anchor='mm', 
#                           stroke_width=outline_thickness, stroke_fill=outline_color)
#             else:    
#                 # 无轮廓的文字
#                 draw.text((x, y), banner_text, fill=text_color, font=font, anchor='mm')

#             # 将PIL图像转换回张量格式
#             # 注意：这里将RGBA转换为RGB，丢失了透明通道
#             out_image = np.array(back_image.convert("RGB")).astype(np.float32) / 255.0
#             out_image = torch.from_numpy(out_image).unsqueeze(0)  # 添加批次维度
#             total_images.append(out_image)  # 添加到结果列表

#         # 将所有图像合并为一个批次
#         images_out = torch.cat(total_images, 0)

#         # 帮助文档链接
#         show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Template-Nodes#cr-simple-banner"
          
#         return (images_out, show_help, )  # 返回处理后的图像和帮助信息
#         show_help = "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes/wiki/Template-Nodes#cr-simple-banner"
          
#         return (images_out, show_help, )  # 返回处理后的图像和帮助信息