# 提醒，需要把python解释器地址锁定到comfyui本身的python.exe上，才可以引用以下包
import folder_paths # comfyui对模型名称的调用（ckpt，vae，clip，lora等）
import comfy.samplers # comfyui对采样器，调度器的调用
import comfy.model_management # comfyui对模型加载进行操作

class a3:
    def __init__(self):
        pass

    CATEGORY = "0x_erthor_node👾👾👾/a000_example"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                # 1 调用本地参数模型============================================================
                "获取本地checkpoint": (["None"] + folder_paths.get_filename_list("checkpoints"),),
                "获取本地vae": (["None"] + folder_paths.get_filename_list("vae"),),
                "获取本地lora": (["None"] + folder_paths.get_filename_list("loras"),),

                "获取本地sampler": (comfy.samplers.KSampler.SAMPLERS,),  # 采样器
                "获取本地scheduler": (comfy.samplers.KSampler.SCHEDULERS,),  # 调度器

                # 随机种子
                # 种子会占两行，第二行会决定种子使用过后如何变化
                "seed": ("INT", {"default": 123, "min": 0, "max": 0xffffffffffffffff, "step": 1}),
            },
        }


    OUTPUT_NODE = True
    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("1整数",)



    FUNCTION = "test"
    def test(self,):
        # 2 对加载模型进行操作=====================================================================

        # 在现存中清除所有加载的模型
        comfy.model_management.unload_all_models()

        # 获取当前可用的设备
        device = comfy.model_management.get_torch_device()

        # 设置随机种子
        seed = '123'
        torch.manual_seed(seed)

        pass
