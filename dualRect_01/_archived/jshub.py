import time
from psychopy import visual
from psychopy.hardware import joystick as js

class JS:

    def __init__(self, mode: str = 'XboxController'):

        self.win_flipper = visual.Window(size=(400, 300), screen=0, color='#000000', title='.flip()', winType='pyglet')
        js.backend = 'pyglet'
        self.mode = mode
        if mode not in ['XboxController', ]:
            raise IOError(f'unknown hardware parameter.')



class solo_JS(JS):

    def __init__(self, mode: str='XboxController'):

        super().__init__(mode)
        
        self._pressed_time = 0
        self._pressed_name = None
        self._js_before = [False] * len(js.XboxController(0).getAllButtons())

        if js.getNumJoysticks() >= 1:
            self.js0 = js.XboxController(0)
        else:
            raise IOError(f'\nno joystick detected! \ncurrent joystick number: {js.getNumJoysticks()}.\n')

    def check_js(self, interval: float = 2) -> str:

        _js0_current = self.js0.getAllButtons()
        pressed_0 = None

        def __check(_last_pressed: list = [0, None]):
            js = self.js0
            pressed = None

            for i, (before, current) in enumerate(zip(self._js_before, _js0_current)):
                if current and (not before):
                    self._js_before[i] = True
                    self._pressed_time = time.time()
                    if js.get_y():
                        pressed = 'Y'
                        self._pressed_name = 'Y'
                    elif js.get_a():
                        if (self._pressed_time - _last_pressed[0] <= interval) and (_last_pressed[1] == 'Y'):
                            pressed = 'Y_A'
                            self._pressed_name = None
                            self._pressed_time = 0
                            _last_pressed[1] = None
                        else:
                            pressed = 'A'
                            self._pressed_name = 'A'
                    elif js.get_x():
                        pressed = 'X'
                        self._pressed_name = 'X'
                    elif js.get_b():
                        pressed = 'B'
                        self._pressed_name = 'B'
                    elif js.get_left_shoulder():
                        pressed = 'LB'
                        self._pressed_name = 'LB'
                    elif js.get_right_shoulder():
                        pressed = 'RB'
                        self._pressed_name = 'RB'
                    elif js.get_start():
                        pressed = 'start'
                        self._pressed_name = 'start'
                    elif js.get_back():
                        pressed = 'back'
                        self._pressed_name = 'back'
                    # 读取十字键（D-Pad）状态
                    elif hasattr(js, 'get_hat'):
                        hat = js.get_hat()
                        if hat == (0, 1):
                            pressed = 'dpad_up'
                            self._pressed_name = 'dpad_up'
                        elif hat == (0, -1):
                            pressed = 'dpad_down'
                            self._pressed_name = 'dpad_down'
                        elif hat == (-1, 0):
                            pressed = 'dpad_left'
                            self._pressed_name = 'dpad_left'
                        elif hat == (1, 0):
                            pressed = 'dpad_right'
                            self._pressed_name = 'dpad_right'
                elif before and (not current):
                    self._js_before[i] = False

                _last_pressed[0] = self._pressed_time

            return pressed
        
        pressed_0 = __check(_last_pressed=[self._pressed_time, self._pressed_name])
        return pressed_0



class dualJS(JS):

    def __init__(self, mode: str='XboxController'):

        super().__init__(mode)

        self._pressed_time = [0, 0]
        self._pressed_name = [None, None]
        self._js0_before = [False] * len(js.XboxController(0).getAllButtons())
        self._js1_before = [False] * len(js.XboxController(1).getAllButtons())

        if js.getNumJoysticks() == 2:
            self.js0 = js.XboxController(0)
            self.js1 = js.XboxController(1)
        elif js.getNumJoysticks() == 1:
            self.js0 = js.XboxController(0)
            self.js1 = js.XboxController(0)
        else:
            raise IOError(f'\ninvalid hardware(s), \ncurrent joystick number: {js.getNumJoysticks()}.\n')

    def check_js(self, interval: float = 2) -> list:

        _js0_current = self.js0.getAllButtons()
        _js1_current = self.js1.getAllButtons()

        pressed_0, pressed_1 = None, None

        def __check(js_index: int, _last_pressed: list = [[0, None], [0, None]]):
            
            if js_index == 0:
                js = self.js0
                _js_before = self._js0_before
                _js_current = _js0_current
            elif js_index == 1:
                js = self.js1
                _js_before = self._js1_before
                _js_current = _js1_current
            else:
                raise ValueError(f'invalid js_index: {js_index}')

            pressed = None

            for i, (before, current) in enumerate(zip(_js_before, _js_current)):
                if current and (not before):
                    _js_before[i] = True
                    self._pressed_time[js_index] = time.time()
                    if js.get_y():
                        pressed = 'Y'
                        self._pressed_name[js_index] = 'Y'
                    elif js.get_a():
                        if (self._pressed_time[js_index] - _last_pressed[js_index][0] <= interval) and (_last_pressed[js_index][1] == 'Y'):
                            pressed = 'Y_A'
                            self._pressed_name[js_index] = None
                            self._pressed_time[js_index] = 0
                            _last_pressed[js_index][1] = None
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
                        self._pressed_name[js_index] = 'LB'
                    elif js.get_right_shoulder():
                        pressed = 'RB'
                        self._pressed_name[js_index] = 'RB'
                    elif js.get_start():
                        pressed = 'start'
                        self._pressed_name[js_index] = 'start'
                    elif js.get_back():
                        pressed = 'back'
                        self._pressed_name[js_index] = 'back'
                    # 读取十字键（D-Pad）状态
                    elif hasattr(js, 'get_hat'):
                        hat = js.get_hat()
                        if hat == (0, 1):
                            pressed = 'dpad_up'
                            self._pressed_name = 'dpad_up'
                        elif hat == (0, -1):
                            pressed = 'dpad_down'
                            self._pressed_name = 'dpad_down'
                        elif hat == (-1, 0):
                            pressed = 'dpad_left'
                            self._pressed_name = 'dpad_left'
                        elif hat == (1, 0):
                            pressed = 'dpad_right'
                            self._pressed_name = 'dpad_right'
                elif before and (not current):
                    _js_before[i] = False

                _last_pressed[js_index][0] = self._pressed_time[js_index]
                _last_pressed[js_index][1] = self._pressed_name[js_index]

            return pressed
        
        pressed_0 = __check(js_index=0, _last_pressed=[[self._pressed_time[0], self._pressed_name[0]], [self._pressed_time[1], self._pressed_name[1]]])
        pressed_1 = __check(js_index=1, _last_pressed=[[self._pressed_time[0], self._pressed_name[0]], [self._pressed_time[1], self._pressed_name[1]]])

        return [pressed_0, pressed_1]
    


class trio_JS:

    def __init__(self, mode:str='XboxController'):

        super().__init__(mode)



# 用例测试
if __name__ == '__main__':
    from psychopy import core

    ### 单手柄输入检测测试
    solo = solo_JS()

    while True:
        _pressed_0 = solo.check_js()
        if _pressed_0:
            if _pressed_0 == 'start':
                print('Break.')
                break
            else:
                print(f'pressed_0:{_pressed_0}')
        else:
            pass
        solo.win_flipper.flip()
        core.wait(0.01)

    # ## 双手柄输入检测测试
    # dual = dualJS()
    # while True:
    #     _pressed_0, _pressed_1 = dual.check_js()
    #     if _pressed_0 or _pressed_1:
    #         if (_pressed_0 == 'start') or (_pressed_1 == 'start'):
    #             print('Break.')
    #             break
    #         else:
    #             print(f'pressed_0: {_pressed_0}, pressed_1: {_pressed_1}')
    #     else:
    #         pass
    #     dual.win_flipper.flip()
    #     core.wait(0.01)
