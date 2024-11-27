
'''
双手柄输入测试脚本。
'''

from psychopy import core, visual
from psychopy.hardware import joystick as js

class Solo:

    button_dict = {0:'A', 1:'B', 2:'X', 3:'Y', 4:'LB', 5:'RB', 
                   6:'back', 7:'start', 8:'LS', 9:'RS'}

    def __init__(self):
        js.backend = 'pyglet'
        self.win = visual.Window(winType='pyglet')
        if js.getNumJoysticks() < 1:
            raise RuntimeError(f'\n未检测到足够数量的手柄。\n当前手柄数量：{js.getNumJoysticks()}。')
        self.js1 = js.XboxController(0)

        # 初始化每个按键的状态为False（未按下）
        self.states_before = [False] * len(self.js1.getAllButtons())

    def solo_check(self):
        '''
        轮询并记录单手柄的按键状态信息，每个按键从未按下变为按下时，只记录一次。
        '''
        while True:
            states_current = self.js1.getAllButtons()
            for i, (j, k) in enumerate(zip(states_current, self.states_before)):
                if (j) and (not k): #此前没有按，当前按下。
                    print (self.js1.a)
                    print(f'Button {Solo.button_dict[i]} id:{i} pressed') # <--- 将这一行改为 kernel 中的实现即可。
                    self.states_before[i] = True #将此前状态 (k) 设为 True
                elif (k) and (not j): #此前按下，当前释放。
                    self.states_before[i] = False #将此前状态 (k) 设为 False
            self.win.flip()
            core.wait(0.01)

    def check_other(self):
        while True:
            k = (self.js1.getAllAxes())
            print(k)
            core.wait(0.5)

class Dual:

    button_dict = {0:'A', 1:'B', 2:'X', 3:'Y', 4:'LB', 5:'RB', 
                   6:'back', 7:'start', 8:'LS', 9:'RS'}

    def __init__(self):
        js.backend = 'pyglet'
        self.win = visual.Window(winType='pyglet')
        # self.win_trash = visual.Window(winType='pyglet')
        if js.getNumJoysticks() < 2:
            raise RuntimeError(f'\n未检测到足够数量的手柄。\n当前手柄数量：{js.getNumJoysticks()}。')
        self.js1 = js.XboxController(0)
        self.js2 = js.XboxController(1)

        # 初始化每个按键的状态为False（未按下）
        self.states_before_0 = [False] * len(self.js1.getAllButtons())
        self.states_before_1 = [False] * len(self.js2.getAllButtons())

    def dual_check(self):
        '''
        轮询并记录单手柄的按键状态信息，每个按键从未按下变为按下时，只记录一次。
        '''
        while True:

            states_current_0 = self.js1.getAllButtons()
            states_current_1 = self.js2.getAllButtons()

            for i, (j, k) in enumerate(zip(states_current_0, self.states_before_0)):
                if (j) and (not k): #此前没有按，当前按下。
                    self.states_before_0[i] = True #将此前状态 (k) 设为 True
                    print(f'Joystick 0: Button {Solo.button_dict[i]} id:{i} pressed') # <--- 将这一行改为 render_graph / render_hud 即可。
                elif (k) and (not j): #此前按下，当前释放。
                    self.states_before_0[i] = False #将此前状态 (k) 设为 False
                else:
                    pass

            for i, (j, k) in enumerate(zip(states_current_1, self.states_before_1)):
                if (j) and (not k): #此前没有按，当前按下。
                    self.states_before_1[i] = True #将此前状态 (k) 设为 True
                    print(f'Joystick 1: Button {Solo.button_dict[i]} id:{i} pressed') # <--- 将这一行改为 render_graph / render_hud 即可。
                elif (k) and (not j): #此前按下，当前释放。
                    self.states_before_1[i] = False #将此前状态 (k) 设为 False
                else:
                    pass

            self.win.flip()
            core.wait(0.01)

    def dual_catch(self):
        '''
        根据捕获到的双手柄按键，更改外部状态。
        '''
        while True:

            states_current_0 = self.js1.getAllButtons()
            states_current_1 = self.js2.getAllButtons()

            print (self.states_before_0)
            print (self.states_before_1)
            print (states_current_0)
            print (states_current_1)

            for i, (j, k) in enumerate(zip(states_current_0, self.states_before_0)):
                if (j) and (not k): #此前没有按，当前按下。
                    self.states_before_0[i] = True #将此前状态 (k) 设为 True
                    if self.js1.get_right_shoulder():
                        print('RB')
                    elif self.js1.get_left_shoulder():
                        print("LB")
                    elif self.js1.get_a():
                        print('A')
                    elif self.js1.get_b():
                        print('B')
                    elif self.js1.get_x():
                        print('X')
                elif (k) and (not j): #此前按下，当前释放。
                    self.states_before_0[i] = False #将此前状态 (k) 设为 False
                else:
                    pass

            for i, (j, k) in enumerate(zip(states_current_1, self.states_before_1)):
                if (j) and (not k): #此前没有按，当前按下。
                    self.states_before_1[i] = True #将此前状态 (k) 设为 True
                    if self.js2.get_right_shoulder():
                        print('RB')
                    elif self.js2.get_left_shoulder():
                        print("LB")
                    elif self.js2.get_a():
                        print('A')
                    elif self.js2.get_b():
                        print('B')
                    elif self.js2.get_x():
                        print('X')
                elif (k) and (not j): #此前按下，当前释放。
                    self.states_before_1[i] = False #将此前状态 (k) 设为 False
                else:
                    pass

            self.win.flip()
            core.wait(0.1)


if __name__ == '__main__':

    solo = Solo()
    solo.solo_check()
    # solo.check_other()

    dual = Dual()
    # dual.dual_check()
    # dual.dual_catch()
    
