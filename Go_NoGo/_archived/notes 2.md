# Go/NoGo 实验
> renjiayi, 20250523

- 环境准备：
    - Windows 10/11
    - 安装 [Python 3.10](https://www.python.org/ftp/python/3.10.8/python-3.10.8-amd64.exe)
    - Windows 终端（命令提示符）中执行 `pip install psychopy`
        - 不要在官网安装 standalone 版本，运行不了
    - 终端中继续 pip install 下列依赖：numpy
    - 如果有自动打 mark 需求（手动 mark 不需要执行）：
        - 须额外 pip install 下列依赖：serial、pylsl
        - 须在 `kernel.py` 中导入写好的 `trigger.py` 模块中的 `Trigger`类，并在 `Event` 类中创建实例，调用 `.send` 方法。
    - 直接运行 __main.py__ 即可。

调整 config.py 中对应的键值可以按需修改下述参数。
- 实验默认参数配置：
    - 6 blocks，每个 block 包含 1 Go + 1 NoGo。
        - block 数量可在 `.stim_params` 方法中的 `block` 键中调整。
    - Go：看见字母 b 或 d 便按空格键；NoGo：奇数 block 只对 p 按键反应，偶数 block 只对 q 按键反应。共 24 个 trial，两种字母各占一半。
        - 按键（空格键）可在 `.keys` 方法中调整。
        - 呈现的刺激字母（p 或 q）可在 `.stim_obj` 方法中调整。
        - 刺激的尺寸大小可在 `.stim_params` 方法中的 `stim_size` 键中调整。
    - Go 与 NoGo 阶段共 24 个 trial，两种字母各占一半。
        - 刺激数量可在 `.stim_num` 方法中调整。
    - 实验开始前休息 30s，block 之间间隔 5s。
        - 上述参数可在 `.duration` 方法中调整。