
import time, serial
from psychopy import parallel
from pylsl import StreamInfo, StreamOutlet

class Trigger:

    def __init__(self, mode:str='LSL'):

        '''
        mode: 通过何种方式发送 trigger。
        - str: LSL / 通过 LAN 发送，用于 Aurora hyperscanning。
        - str: LPT / 通过 C-Pod 串并口转换器发送 trigger。
        - str: parallel / 通过原生并口发送 trigger。
        '''

        self.mode = mode

        if self.mode == 'LSL':
            self.info = StreamInfo(name='Trigger', type='Markers', channel_count=1,
                                   source_id='renjiayi')
            self.out = StreamOutlet(self.info)
        
        elif self.mode == 'LPT':
            self.port = serial.Serial(port='com8', baudrate=115200, timeout=1)
        
        elif self.mode == 'parallel':
            parallel.setPortAddress(address=0x0378)
            parallel.setData(0)

        else:
            raise ValueError(f'invalid trigger mode: {self.mode}')

    def send(self, value:int=0):

        if self.mode == 'LSL':
            self.out.push_sample([value])

        elif self.mode == 'LPT':
            # self.port.write([value.to_bytes(1, 'little')])
            self.port.write([value])

        elif self.mode == 'parallel':
            parallel.setData(value)
            time.sleep(0.1)
            parallel.setData(0)

if __name__ == '__main__':

    import random as rd

    EventMarker = Trigger(mode='LSL')

    time_init = time.time()
    clock_init = 0

    while time.time() - time_init <= 300:

        interval = rd.uniform(0.5,5.0)
        marker_value = rd.randint(1,11)

        clock_init += interval
        EventMarker.send(value=marker_value)
        print(f'\n --> Trigger {marker_value:>3} at {format(clock_init,".3f"):>7}s (after {format(interval,".3f"):>5}s).')

        time.sleep(interval)
