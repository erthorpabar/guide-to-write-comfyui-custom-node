一个comfyui自定义节点的创建指南

安装：不需要安装任何其他包，只需要把0x_erthor_node文件夹复制到custom_nodes文件夹下，就能安装成功。

a1：展示了代码结构，表明了每一块代码的作用是什么，哪里是输入，哪里是参数栏，哪里是输出。

a2：如何加入各种comfyui支持的数据类型，包括img，latent等。👇

![111](https://github.com/ycc1519202717/guide-to-write-comfyui-custom-node/assets/114896778/69c00a28-abc5-404b-a0b3-1b03c3be4ae9)

a3：如何使用comfyui自带的库去索引参数，如ckpt，vae，clip等。👇

![333](https://github.com/ycc1519202717/guide-to-write-comfyui-custom-node/assets/114896778/a8005ca9-dbf0-4357-a5bd-e5ec11a9d540)

a4：一个最简的可以运行的节点，它创建一个空的torch.Tensor向量空间，并输出。需要连接最基础的previewimage节点才能展示出来。👇

![44](https://github.com/ycc1519202717/guide-to-write-comfyui-custom-node/assets/114896778/3051d914-c4fd-456d-88bd-db504c4a6f25)

a5：通用最简模板，日常编写节点可直接复制并在此基础上编写。



