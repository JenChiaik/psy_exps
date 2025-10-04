'''
使用 pygame 重写的手柄控制模块。
相比于 psychopy，可以读取 D-Pad、扳机、摇杆状态了。
'''

import time
import pygame

class JS:

    def __init__(self):

        pygame.init()
        pygame.joystick.init()



class soloJS(JS):
    '''
    处理单手柄的输入。
    '''

    def __init__(self):

        super().__init__()

        if pygame.joystick.get_count() >= 1:
            self.js0 = pygame.joystick.Joystick(0)
            self.js0.init()
        else:
            raise IOError(f'no joystick detected! current joystick number: {pygame.joystick.get_count()}')

        self._pressed_time = 0
        self._pressed_name = None
        self._js_before = [False] * self.js0.get_numbuttons()
        self._hat_before = (0, 0)

    def check_js(self, comb_time:float=2.0) -> str:
        '''
        轮询手柄状态，返回按键名称。
        - comb_time: 组合按键允许的间隔时间。
        '''
        
        pygame.event.pump()
        _js0_current = [self.js0.get_button(i) for i in range(self.js0.get_numbuttons())]
        hat = self.js0.get_hat(0)
        pressed_0 = None

        def __check(_last_pressed:list=[0, None]):
            nonlocal hat
            pressed = None

            for i, (before, current) in enumerate(zip(self._js_before, _js0_current)):
                if current and (not before):
                    self._js_before[i] = True
                    self._pressed_time = time.time()
                    if i == 3:  # Y
                        pressed = 'Y'
                        self._pressed_name = 'Y'
                    elif i == 0:  # A
                        if (self._pressed_time - _last_pressed[0] <= comb_time) and (_last_pressed[1] == 'Y'):
                            pressed = 'Y_A'
                            self._pressed_name = None
                            self._pressed_time = 0
                            _last_pressed[1] = None
                        else:
                            pressed = 'A'
                            self._pressed_name = 'A'
                    elif i == 2:  # X
                        pressed = 'X'
                        self._pressed_name = 'X'
                    elif i == 1:  # B
                        pressed = 'B'
                        self._pressed_name = 'B'
                    elif i == 4:  # LB
                        pressed = 'LB'
                        self._pressed_name = 'LB'
                    elif i == 5:  # RB
                        pressed = 'RB'
                        self._pressed_name = 'RB'
                    elif i == 7:  # Start
                        pressed = 'start'
                        self._pressed_name = 'start'
                    elif i == 6:  # Back
                        pressed = 'back'
                        self._pressed_name = 'back'

                elif before and (not current):
                    self._js_before[i] = False

            if hat != self._hat_before:
                self._pressed_time = time.time()
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
                self._hat_before = hat

            _last_pressed[0] = self._pressed_time
            return pressed

        pressed_0 = __check(_last_pressed=[self._pressed_time, self._pressed_name])
        return pressed_0



class dualJS(JS):
    '''
    处理双手柄的输入。
    '''

    def __init__(self):

        super().__init__()

        self._pressed_time = [0, 0]
        self._pressed_name = [None, None]

        count = pygame.joystick.get_count()
        if count >= 2:
            self.js0 = pygame.joystick.Joystick(0)
            self.js1 = pygame.joystick.Joystick(1)
        elif count == 1:
            self.js0 = pygame.joystick.Joystick(0)
            self.js1 = pygame.joystick.Joystick(0)
        else:
            raise IOError(f'invalid hardware(s), current joystick number: {count}')

        self.js0.init()
        self.js1.init()

        self._js0_before = [False] * self.js0.get_numbuttons()
        self._js1_before = [False] * self.js1.get_numbuttons()
        self._hat_before = [(0, 0), (0, 0)]

    def check_js(self, interval:float=2) -> list[str]:
        '''
        轮询手柄状态，返回按键名称列表 [pressed_0, pressed_1]。
        - interval: 组合按键允许的间隔时间，单位为秒。
        '''

        pygame.event.pump()

        _js0_current = [self.js0.get_button(i) for i in range(self.js0.get_numbuttons())]
        _js1_current = [self.js1.get_button(i) for i in range(self.js1.get_numbuttons())]
        hat0 = self.js0.get_hat(0)
        hat1 = self.js1.get_hat(0)

        pressed_0, pressed_1 = None, None

        def __check(js, js_index, _js_before, _js_current, hat):
            pressed = None

            for i, (before, current) in enumerate(zip(_js_before, _js_current)):
                if current and (not before):
                    _js_before[i] = True
                    self._pressed_time[js_index] = time.time()
                    if i == 3:
                        pressed = 'Y'
                        self._pressed_name[js_index] = 'Y'
                    elif i == 0:
                        if (self._pressed_time[js_index] - self._pressed_time[js_index] <= interval) and (self._pressed_name[js_index] == 'Y'):
                            pressed = 'Y_A'
                            self._pressed_name[js_index] = None
                            self._pressed_time[js_index] = 0
                        else:
                            pressed = 'A'
                            self._pressed_name[js_index] = 'A'
                    elif i == 2:
                        pressed = 'X'
                        self._pressed_name[js_index] = 'X'
                    elif i == 1:
                        pressed = 'B'
                        self._pressed_name[js_index] = 'B'
                    elif i == 4:
                        pressed = 'LB'
                        self._pressed_name[js_index] = 'LB'
                    elif i == 5:
                        pressed = 'RB'
                        self._pressed_name[js_index] = 'RB'
                    elif i == 7:
                        pressed = 'start'
                        self._pressed_name[js_index] = 'start'
                    elif i == 6:
                        pressed = 'back'
                        self._pressed_name[js_index] = 'back'
                elif before and (not current):
                    _js_before[i] = False

            if hat != self._hat_before[js_index]:
                self._pressed_time[js_index] = time.time()
                if hat == (0, 1):
                    pressed = 'dpad_U'
                elif hat == (0, -1):
                    pressed = 'dpad_D'
                elif hat == (-1, 0):
                    pressed = 'dpad_L'
                elif hat == (1, 0):
                    pressed = 'dpad_R'
                self._hat_before[js_index] = hat

            return pressed

        pressed_0 = __check(self.js0, 0, self._js0_before, _js0_current, hat0)
        pressed_1 = __check(self.js1, 1, self._js1_before, _js1_current, hat1)

        return [pressed_0, pressed_1]
    


    class trioJS(JS):
        '''
        处理三手柄的输入。
        '''

        pass



# 用例测试
if __name__ == '__main__':

    # solo = solo_JS()
    # while True:
    #     _pressed = solo.check_js()
    #     if _pressed:
    #         print(f'pressed_0: {_pressed}')
    #         if _pressed == 'start':
    #             break
    #     time.sleep(0.01)

    dual = dualJS()
    while True:
        _pressed_0, _pressed_1 = dual.check_js()
        if _pressed_0 or _pressed_1:
            if (_pressed_0 == 'start') or (_pressed_1 == 'start'):
                print('Break.')
                break
            else:
                print(f'pressed_0: {_pressed_0}, pressed_1: {_pressed_1}')
        else:
            pass
        time.sleep(0.01)
