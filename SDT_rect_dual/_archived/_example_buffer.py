from psychopy import visual, core

# 创建窗口
win = visual.Window(size=(800, 600), color='black', units='pix')

# 创建图形对象
shape1 = visual.Rect(win, width=100, height=100, fillColor='red', pos=(-200, 0))
shape2 = visual.Circle(win, radius=50, fillColor='blue', pos=(0, 0))
shape3 = visual.Polygon(win, edges=5, radius=60, fillColor='green', pos=(200, 0))

# 创建缓冲图像（提前绘制）
buffer1 = visual.BufferImageStim(win, stim=[shape1])  # 缓存形状1
buffer2 = visual.BufferImageStim(win, stim=[shape2])  # 缓存形状2
buffer3 = visual.BufferImageStim(win, stim=[shape3])  # 缓存形状3

# 显示缓冲图像
buffer1.draw()
win.flip()  # 显示图形1
core.wait(0.5)  # 等待 0.5 秒

buffer2.draw()
win.flip()  # 显示图形2
core.wait(0.5)

buffer3.draw()
win.flip()  # 显示图形3
core.wait(0.5)

# 关闭窗口
win.close()
