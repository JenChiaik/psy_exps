
'''
键盘输入监听模块，不支持组合按键，并且默认忽略“按住”行为。
双人同时输入无法解决冲突问题，故只建议用于单人模式。
'''

from psychopy.hardware import keyboard as kb



class solo_KB:

    def __init__(self):

        self.keyboard = kb.Keyboard()

    def check_kb(self) -> str:

        self.keyboard.clearEvents()
        return self.keyboard.getKeys()
    
    def wait_key(self, key:list|tuple, stop:bool):

        while (not stop):

            pressed = self.check_kb()
            if pressed:
                key_name = pressed[0].name
                if key_name in key:
                    return key_name
            continue
        
        return None

    def wait_key(self, key:list|tuple, stop:callable) -> str:
        '''
        持续监听按键输入，直到满足停止条件或按下指定按键。
        - key: 合法的按键名称列表；
        - stop: 外部函数或 lambda，返回 True 则终止监听；
        '''
        while not stop():

            pressed = self.check_kb()
            if pressed:
                key_name = pressed[0].name
                if key_name in key:
                    return key_name
            continue

        return None
    
# 用例测试


