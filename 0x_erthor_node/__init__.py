# 从py中引入一个类作为引用依据
# from py名称 import 类1，类2，类3
from .a000_example.a1基础格式 import a1
from .a000_example.a2基础数据类型 import a2
from .a000_example.a3基础调用流程 import a3
from .a000_example.a4一个可以运行的节点 import a4
from .a000_example.a5最简格式 import a5


# （必填）填写 import的类名称，命名需要唯一，key或value与其他插件冲突可能引用不了。这是决定是否能引用的关键。
# key(自定义):value(import的类名称)
NODE_CLASS_MAPPINGS = {
    # a000_example
    "a1": a1,"a2": a2,"a3": a3,"a4":a4,"a5":a5,

}


# （可不写）填写 ui界面显示名称，命名会显示在节点ui左上角，如不写会用类的名称显示在节点ui上
# key(自定义):value(ui显示的名称)
NODE_DISPLAY_NAME_MAPPINGS = {
    # a000_example
    "a1": "a1基础格式~","a2": "a2基础数据类型~","a3": "a3基础调用流程~","a4":"a4一个可以运行的节点~","a5":"a5最简格式~",

}


# 引入以上两个字典的内容
all = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']