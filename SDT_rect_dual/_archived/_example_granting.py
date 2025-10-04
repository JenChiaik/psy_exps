import numpy as np
from psychopy import visual, core

def display_gratings(signal: int):
    """
    显示六边形排列的光栅，其中一个光栅具有更高的对比度。
    
    参数：
        signal (int): 表示哪一个光栅的对比度更高，1~6 代表对应光栅，0 表示所有光栅相同。
    """
    # 创建窗口（16:9 比例）
    win = visual.Window(
        size=[1600, 900],
        units="pix",
        color=[0.5, 0.5, 0.5]  # 背景色 #808080 (归一化到 [0, 1])
    )

    # 参数设置
    r = 280  # 半径（像素）
    angles = [np.pi/2, np.pi/6, -np.pi/6, -np.pi/2, -5*np.pi/6, 5*np.pi/6]  # 六个点的角度
    positions = [(r * np.cos(a), r * np.sin(a)) for a in angles]  # 计算每个点的位置

    # 创建光栅
    gratings = []
    for i, pos in enumerate(positions):
        if signal == i + 1:  # 使 signal 对应的光栅对比度更高
            color = (0.5, 0.5, 0.5)  # 黑色基准值
            contrast = 1.0  # 最大对比度
        else:  # 其他光栅使用默认对比度和颜色
            color = (0.5, 0.5, 0.5)  # 中灰色基准值
            contrast = 0.5  # 默认对比度

        grating = visual.GratingStim(
            win=win,
            tex="sin",
            mask="gauss",  # 使用高斯遮罩实现羽化效果
            size=(350, 350),  # 设置光栅直径
            pos=pos,  # 每个光栅的位置
            sf=0.03,  # 空间频率
            colorSpace="rgb",  # 颜色空间
            contrast=contrast,  # 对比度
            color=color  # 基准颜色
        )
        gratings.append(grating)

    # 绘制中心的十字
    fixation = visual.TextStim(win, text="+", color="black", height=120)

    # 渲染光栅和十字
    fixation.draw()
    win.flip()
    core.wait(2)

    fixation.draw()
    for grating in gratings:
        grating.draw()
    win.flip()

    # 等待并退出
    core.wait(10)
    win.close()
    core.quit()


# 示例调用
# 显示第 2 个光栅对比度更高
display_gratings(signal=2)
