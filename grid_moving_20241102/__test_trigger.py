'''
测试使用 LSL 数据流传输 event marker。
'''

import time, random as rd
from trigger import Trigger

class TriggerTest:

    def __init__(self):

        self.EventMarker = Trigger(mode='LSL')

    def test(self, duration:int=30):

        time_init = time.time()
        clock_init = 0

        while time.time() - time_init <= duration:

            self.interval = rd.uniform(0.5,5.0)
            self.marker_value = rd.randint(1,11)

            clock_init += self.interval
            self.EventMarker.send(value=self.marker_value)
            time.sleep(self.interval)

            print(f'\n --> Trigger {self.marker_value:>3} at {format(clock_init,".3f"):>7}s (after {format(self.interval,".3f"):>5}s).')

if __name__ == '__main__':

    test = TriggerTest()
    test.test(duration=30)

