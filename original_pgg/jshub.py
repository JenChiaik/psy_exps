
'''
双手柄输入监测模块。
- 两只手柄互不干扰地进行异步操作，并且忽略掉“按住”行为。
- 自带一个用于刷新 backend 的图形窗口，无需重复创建。
'''

import time
from psychopy import visual
from psychopy.hardware import joystick as js

class dual_JS:

    def __init__(self, mode:str='XboxController'):

        self.win_flipper = visual.Window(size=(400,300), screen=0, color='#000000', title='.flip()' ,winType='pyglet')
        
        # 记录双方上一次按键的时间和名称，用于检测双击或组合按键操作。
        self._pressed_time = [0, 0]
        self._pressed_name = [None, None]

        if mode == 'XboxController':

            if js.getNumJoysticks() == 2:
                self.js0 = js.XboxController(0)
                self.js1 = js.XboxController(1)

            elif js.getNumJoysticks() == 1:
                self.js0 = js.XboxController(0)
                self.js1 = js.XboxController(0)

            # elif js.getNumJoysticks() == 0:
            #     print('\nno joystick found, running in debug mode.\n')

            else:
                raise IOError(f'\ninvalid hardware(s), \ncurrent joystick number: {js.getNumJoysticks()}.\n')
            
            js.backend = 'pyglet'
            
        elif mode == 'Joystick':
            raise IOError(f'unsupported Joystick parameter currently.')

        else:
            raise IOError(f'unknown hardware parameter.')

    def check_js(self, _js0_before:list, _js1_before:list, interval:float=2) -> list:

        '''
        查询当前两个手柄按键状态，但如果上次按键状态与这次相同，则忽略重复“按住”操作。
        - js_before: 指定手柄之前的按键状态。
        - interval: 检测前-后组合按键的时间窗。
        返回当前手柄的按键名称（字符串元组）。
        使用时，外部应该以短间隔的循环形式调用此方法。
        '''

        _js0_current = self.js0.getAllButtons()
        _js1_current = self.js1.getAllButtons()

        pressed_0, pressed_1 = None, None

        def __check(js_index:int, _js_before:list, _js_current:list, 
                    _last_pressed:list=[[0,None],[0,None]]):
            '''
            查询单个手柄按键的私有函数。
            - last_pressed: [[_last_pressed_time_0，_last_pressed_name_0],[_last_pressed_time_1，_last_pressed_name_1]]
            '''
            if js_index == 0:
                js = self.js0
            elif js_index == 1:
                js = self.js1
            else:
                raise ValueError(f'invalid js_index: {js_index}')

            pressed = None

            for i,(before, current) in enumerate(zip(_js_before, _js_current)):
                if current and (not before):
                    _js_before[i] = True
                    self._pressed_time[js_index] = time.time()
                    if js.get_y():
                        pressed = 'Y'
                        self._pressed_name[js_index] = 'Y'
                    elif js.get_a():
                        if (self._pressed_time[js_index] - _last_pressed[js_index][0] <= interval)\
                            and (_last_pressed[js_index][1] == 'Y'):
                            pressed = 'Y_A'
                            self._pressed_name[js_index] = None
                        else:
                            pressed = 'A'
                            self._pressed_name[js_index] = 'A'
                    elif js.get_x():
                        pressed = 'X'
                        self._pressed_name[js_index] = 'X'
                    elif js.get_b():
                        pressed = 'B'
                        self._pressed_name[js_index] = 'B'
                    elif js.get_left_shoulder():
                        pressed = 'LB'
                    elif js.get_right_shoulder():
                        pressed = 'RB'
                    elif js.get_start():
                        pressed = 'start'
                        self._pressed_name[js_index] = 'start'
                    elif js.get_back():
                        pressed = 'back'
                        self._pressed_name[js_index] = 'back'
                elif before and (not current):
                    _js_before[i] = False
            return pressed
        
        pressed_0 = __check(js_index=0, _js_before=_js0_before, _js_current=_js0_current, 
                            _last_pressed = [[self._pressed_time[0], self._pressed_name[0]], [self._pressed_time[1], self._pressed_name[1]]])
        pressed_1 = __check(js_index=1, _js_before=_js1_before, _js_current=_js1_current,
                            _last_pressed = [[self._pressed_time[0], self._pressed_name[0]], [self._pressed_time[1], self._pressed_name[1]]])

        return [pressed_0, pressed_1]

# 用例测试
if __name__ == '__main__':

    from psychopy import core

    dual = dual_JS()

    _js0_before = [False]*len(dual.js0.getAllButtons())
    _js1_before = [False]*len(dual.js1.getAllButtons())

    while True:

        _pressed_0, _pressed_1 = dual.check_js(_js0_before=_js0_before, _js1_before=_js1_before)

        if _pressed_0 or _pressed_1:

            if (_pressed_0 == 'start') or (_pressed_1 == 'start'):
                print('Break.')
                break

            else:
                print(f'pressed_0: {_pressed_0}, pressed_1: {_pressed_1}')
        
        else:
            pass

        dual.win_flipper.flip()

        core.wait(0.01)

