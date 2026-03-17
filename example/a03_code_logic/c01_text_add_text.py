"""文本合并"""
import os
# 动态获取路径
this_dir = os.path.dirname(__file__) # 当前路径
last1 = os.path.basename(this_dir) # 当前文件夹名称
last2 = os.path.basename(os.path.dirname(this_dir)) # 上级文件夹名称
gategory=f"{last2}🦄🦄🦄/{last1}" # 在comfyui中的目录：上级文件夹名称/当前文件夹名称
# ————————————————————————————————————————————————

class c01_text_add_text:
    def __init__(self):
        pass
    CATEGORY = gategory

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "line_break": ("BOOLEAN", {"default": True}),

            },
            "optional": {
                "text_a": ("STRING", {"forceInput": True}),
                "text_b": ("STRING", {"forceInput": True}),
                "text_c": ("STRING", {"forceInput": True}),
                "text_d": ("STRING", {"forceInput": True}),
            },
        }   
    
    OUTPUT_NODE = True
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("str",)

    FUNCTION = "test"
    def test(self,line_break,text_a=None,text_b=None,text_c=None,text_d=None):

        if line_break:
            connect_symbol = "\n" # 换行
        else:
            connect_symbol = "," # 逗号连接
        
        text_inputs = [text_a,text_b,text_c,text_d]

        text = ""
        for i in text_inputs:
            if i:
                # 除去首尾空格
                i = i.strip()
                
                text += i + connect_symbol  # 使用 += 来累加文本

        return {"result": (text,)}


NODE_CLASS_MAPPINGS = {"c01_text_add_text": c01_text_add_text,}
NODE_DISPLAY_NAME_MAPPINGS = {"c01_text_add_text":"text_add_text🦄",}
























class WAS_Text_Concatenate:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "delimiter": ("STRING", {"default": ", "}),
                "clean_whitespace": (["true", "false"],),
            },
            "optional": {
                "text_a": ("STRING", {"forceInput": True}),
                "text_b": ("STRING", {"forceInput": True}),
                "text_c": ("STRING", {"forceInput": True}),
                "text_d": ("STRING", {"forceInput": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "text_concatenate"

    CATEGORY = "WAS Suite/Text"

    def text_concatenate(self, delimiter, clean_whitespace, **kwargs):
        text_inputs = []

        # Handle special case where delimiter is "\n" (literal newline).
        if delimiter in ("\n", "\\n"):
            delimiter = "\n"

        # Iterate over the received inputs in sorted order.
        for k in sorted(kwargs.keys()):
            v = kwargs[k]

            # Only process string input ports.
            if isinstance(v, str):
                if clean_whitespace == "true":
                    # Remove leading and trailing whitespace around this input.
                    v = v.strip()

                # Only use this input if it's a non-empty string, since it
                # never makes sense to concatenate totally empty inputs.
                # NOTE: If whitespace cleanup is disabled, inputs containing
                # 100% whitespace will be treated as if it's a non-empty input.
                if v != "":
                    text_inputs.append(v)

        # Merge the inputs. Will always generate an output, even if empty.
        merged_text = delimiter.join(text_inputs)

        return (merged_text,)
