"""代码执行器"""
import os
# 动态获取路径
this_dir = os.path.dirname(__file__) # 当前路径
last1 = os.path.basename(this_dir) # 当前文件夹名称
last2 = os.path.basename(os.path.dirname(this_dir)) # 上级文件夹名称
gategory=f"{last2}🦄🦄🦄/{last1}" # 在comfyui中的目录：上级文件夹名称/当前文件夹名称
# ————————————————————————————————————————————————
import ast

class m05_math_interpreter:
    def __init__(self):
        pass
    CATEGORY = gategory

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "code": ("STRING", {"multiline": True, "dynamicPrompts": False,}),
            },
            "optional": {
                "a": ("INT",),
                "b": ("INT",),
                "c": ("INT",),
            },
        }   
    
    OUTPUT_NODE = True
    RETURN_TYPES = ("INT","FLOAT")
    RETURN_NAMES = ("int","float")

    FUNCTION = "test"
    def test(self,code,a=0,b=0,c=0):
        # ——————检测代码安全性——————
        unsafe_keywords = ['import', 'exec', 'eval', 'open', 'file','system', 'os', 'subprocess']
        if any(keyword in code for keyword in unsafe_keywords):
            raise ValueError("代码中包含不安全的操作")

        # ——————执行代码——————
        safe_locals = {'a': a,'b': b,'c': c,}
        safe_builtins = {
            'abs': abs, # 绝对值
            'max': max, # 最大值
            'min': min, # 最小值
            'pow': pow, # 幂运算
            'round': round, # 四舍五入
            'int': int, # 整数
            'float': float, # 浮点数
        }

        tree = ast.parse(code,mode='eval')
        compiled_code = compile(tree, '<string>', 'eval')
        result = eval(compiled_code, {"__builtins__": safe_builtins}, safe_locals)

        return {"ui": {"value": [result]}, "result": (int(result), float(result),)}


NODE_CLASS_MAPPINGS = {"m05_math_interpreter": m05_math_interpreter,}
NODE_DISPLAY_NAME_MAPPINGS = {"m05_math_interpreter":"math_interpreter🦄",}

'''
表达式必须是单行
1 max(a,b)
2 a>b
'''


