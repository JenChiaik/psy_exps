# 标准库
import os
import random as rd
import datetime as dt
from PIL import Image

# 自编模块
from config import config
# from trigger import Trigger

# Psychopy 库
from psychopy import gui, core, visual, event
from psychopy.visual import TextBox2
from psychopy.hardware import keyboard

class Event:

    '''
    包含所有实验事件。
    '''

    def __init__(self):

        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.script_dir = self.script_dir.replace('\\', '/')



    def overture(self, log_file_name='log.txt', data_file_dir='data'):
        '''
        创建日志、数据文件，录入被试信息。
        '''

        log_path = os.path.join(self.script_dir, log_file_name)
        with open(file=log_path, mode='r', encoding='utf-8') as log:
            exp_existed = 0
            for _ in log:
                exp_existed += 1
                
        self.exp_param = {'exp_num':exp_existed + 1, 
                          'condition_A':["null",1,2,3], #预留条件 A，暂时没用上
                          'condition_B':["null",1,2,3], #预留条件 B，暂时没用上
                          'condition_C':["null",1,2,3], #预留条件 C，暂时没用上
                          'disp_mode':['2160p_debug','2160p_flscr','1440p_debug','1440p_flscr'],
                          'note':'None'}
        exp_info = gui.DlgFromDict(dictionary=self.exp_param)

        if exp_info.OK:
            with open(file=log_path, mode='a', encoding='utf-8') as log:
                log_str = (
                    f"exp_num:{self.exp_param['exp_num']},"
                    f"disp_mode:{self.exp_param['disp_mode']},"
                    f"condition_A:{self.exp_param['condition_A']},"
                    f"condition_B:{self.exp_param['condition_B']},"
                    f"condition_C:{self.exp_param['condition_C']},"
                    f"time:{dt.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')},"
                    f"note:{self.exp_param['note']},\n"
                    )
                log.write(log_str)
        else:
            cancel = gui.warnDlg(prompt='已手动中止实验。')
            if cancel.OK:
                core.quit()

        data_dir = os.path.join(self.script_dir, data_file_dir)
        data_name = f"exp_{self.exp_param['exp_num']}.csv"
        self.image_path = os.path.join(data_dir, data_name)

        with open(file=self.image_path, mode='a', encoding='utf-8') as file:

            head = (
                'exp_num,disp_mode,manip_order,condition_B,condition_C,'
                'sys_time,exp_time,process_name,block_index,trial_index,'
                'disp_stim,target_stim,sub_react,sub_RT,'
                'note\n'
            )

            file.write(head)



    def prelude(self):
        '''
        初始化 i/o 设备。
        '''

        self.keyboard = keyboard.Keyboard()
        # self.marker = Trigger(mode='LSL')

        self.win0 = visual.Window(screen=0, title='sub_0', allowGUI=False, 
                                  size=config.windows_param[self.exp_param['disp_mode']]['res'], 
                                  fullscr=True if self.exp_param['disp_mode'] == '1440p_flscr' else False, 
                                  color=config.color_set['bg_white'])
        # self.win0.mouseVisible = False
        self.mouse = event.Mouse(visible=False)
        self.mouse.setPos(newPos=(-1, -1))

        self.clock_global = core.Clock()
        self.clock_local = core.Clock()

        self.win_ratio = config.windows_param[self.exp_param['disp_mode']]['res'][0] \
            / config.windows_param[self.exp_param['disp_mode']]['res'][1]
        
        try:
            import ctypes
            english_layout = ctypes.windll.user32.LoadKeyboardLayoutW("00000409", 1)
            ctypes.windll.user32.ActivateKeyboardLayout(english_layout, 0)
        except:
            print ('failed to set keyboard with ctypes.windll, try it with Apple script.')
            try:
                import subprocess
                script = '''
                tell application "System Events"
                    set current input source to input source "ABC"
                end tell
                '''
                subprocess.run(["osascript", "-e", script])
            except:
                print ('failed to set keyboard with Apple script.')



    def disp_text(self, 
                  wait:int, auto:bool, text_0:str, 
                  pos:tuple=(0,0), align:str='left', boxsize:tuple=(1.5,1.5), 
                  color:str=config.color_set['black'], textsize:int=config.stim_params['text_size']):
        '''
        - wait: 页面停留时间下限。
        - auto: 自动跳转。
        '''

        text_0 = TextBox2(win=self.win0, text=text_0, lineBreaking='uax14', 
                          pos=pos, size=boxsize, alignment=align, color=color, bold=True,
                          font='Source Han Serif SC', letterHeight=textsize, lineSpacing=1, 
                          units='norm', editable=False)
        text_0.draw()
        self.win0.flip()

        core.wait(wait)
        if auto:
            return
        else:
            self.__wait_kb(key=config.keys['next_page'])



    def disp_pic(self, 
                 pic_0:str, wait:float=1, auto:bool=False):
        '''
        - wait: 页面停留时间下限。
        - auto: 自动跳转。
        '''

        ratio_win = config.windows_param[self.exp_param['disp_mode']]['res'][0] / config.windows_param[self.exp_param['disp_mode']]['res'][1]
        image_dir = os.path.join(self.script_dir, 'image')
        image_name = pic_0
        image_path = os.path.join(image_dir, image_name)

        with Image.open(image_path) as img_0:
            ratio_pic_0 = img_0.size[0] / img_0.size[1]
        if ratio_pic_0 >= ratio_win: #超宽图片
            pic_x_0 = config.windows_param[self.exp_param['disp_mode']]['res'][0]
            pic_y_0 = img_0.size[1]*pic_x_0/img_0.size[0]
        else: #超高图片
            pic_y_0 = config.windows_param[self.exp_param['disp_mode']]['res'][1]
            pic_x_0 = img_0.size[0]*pic_y_0/img_0.size[1]
        content_win0 = visual.ImageStim(image=image_path, size=(pic_x_0, pic_y_0), units='pix', win=self.win0)
        content_win0.draw(win=self.win0)
        self.win0.flip()

        core.wait(wait)
        if auto:
            return
        else:
            self.__wait_kb(key=config.key_nextpage)

    

    def intermezzo(self, duration:int=config.duration['wait_intermezzo']):
        '''
        休息阶段：切黑屏，到时间自动跳转。
        '''

        self.win0.color = config.color_set['bg_black']
        self.win0.flip()
        self.disp_text(wait=duration, auto=True, 
                       text_0=config.text['intermezzo'], 
                       color=config.color_set['bg_white'])
        self.win0.color = config.color_set['bg_white']
        self.win0.flip()



    def block(self, block_index:int):
        '''
        每个 block 包含 1 个 GO 和 1 个 GNG。
        - block_index: 暂无练习阶段，0~5 为 6 个正式实验 block。
            - 奇数 block GNG 阶段的目标刺激为 p。
            - 偶数 block GNG 阶段的目标刺激为 q。
        '''
        stim_order_GO = [config.stim_obj['block_GO']['go']] * config.stim_num['block_GO']['go'] + \
                        [config.stim_obj['block_GO']['ng']] * config.stim_num['block_GO']['ng']
        if block_index % 2 == 0:
            stim_order_GNG = [config.stim_obj['block_GNG_p']['go']] * config.stim_num['block_GNG_p']['go'] + \
                             [config.stim_obj['block_GNG_p']['ng']] * config.stim_num['block_GNG_p']['ng']
        elif block_index % 2 == 1:
            stim_order_GNG = [config.stim_obj['block_GNG_q']['go']] * config.stim_num['block_GNG_q']['go'] + \
                             [config.stim_obj['block_GNG_q']['ng']] * config.stim_num['block_GNG_q']['ng']
        rd.shuffle(stim_order_GO)
        rd.shuffle(stim_order_GNG)

        # GO
        self.disp_text(wait=config.duration['wait_intro'], auto=False, 
                       text_0=config.text['intro_GO'])
        self.disp_text(wait=config.duration['wait_ready'], auto=False, 
                       text_0=config.text['ready_formal'])
        self.win0.color = config.color_set['bg_gray']
        for i,j in enumerate(stim_order_GO):
            self.__trial(block_index=block_index, trial_index=i, 
                         stim_obj=j, target='Any',
                         time_limit=config.duration['wait_stim'],
                         mode='GO')
        self.win0.color = config.color_set['bg_white']
        self.win0.flip()
        self.disp_text(wait=3, auto=True, text_0=config.text['end_semiblock'])

        # GO-NOGO
        self.disp_text(wait=config.duration['wait_intro'], auto=False, 
                       text_0=config.text['intro_GNG_p'] if block_index%2==0 else config.text['intro_GNG_q'])
        self.disp_text(wait=config.duration['wait_ready'], auto=False, 
                       text_0=config.text['ready_formal'])
        self.win0.color = config.color_set['bg_gray']
        for i,j in enumerate(stim_order_GNG):
            self.__trial(block_index=block_index, trial_index=i, 
                         stim_obj=j, 
                         target=config.stim_obj['block_GNG_p']['go'] if block_index%2==0 else config.stim_obj['block_GNG_q']['go'], 
                         time_limit=config.duration['wait_stim'],
                         mode='GNG')
        self.win0.color = config.color_set['bg_white']
        self.win0.flip()
        self.disp_text(wait=3, auto=True, text_0=config.text['end_semiblock'])
        
        

    def __trial(self, block_index:int, trial_index:int, 
                stim_obj:str, target:str, time_limit:float, mode:str):
        '''
        每个 trial 呈现 1 个对象，被试根据规则按键。
        - target: 目标刺激。
            - GO 阶段为 'Any'。
            - GNG 阶段为 'p' 或 'q'，取决于 block_index 的奇偶。
        '''

        self.disp_text(wait=config.duration['wait_fixation'], auto=True, 
                       text_0=config.text['fixation'], textsize=config.stim_params['stim_size'], align='center')

        stim = visual.TextBox2(win=self.win0, text=stim_obj, lineBreaking='uax14', 
                               pos=(0,0), alignment='center', color=config.color_set['black'], bold=True, 
                               font='Consolas', letterHeight=config.stim_params['stim_size'], lineSpacing=1, 
                               units='norm', editable=False)
        stim.draw(), self.win0.flip()

        self.keyboard.clearEvents()
        self.clock_local.reset()
        while self.clock_local.getTime() < time_limit:
            core.wait(0.01)
            pressed = self.keyboard.getKeys()

            if pressed:
                if pressed[0].name in config.keys['operation']:
                    self.record(process_name=mode,
                                block_index=block_index, trial_index=trial_index, 
                                disp_stim=stim_obj, target_stim=target, 
                                sub_react='yes', sub_RT=self.clock_local.getTime(), 
                                note='None')
                    return
            else:
                pass

        self.record(process_name=mode, 
                    block_index=block_index, trial_index=trial_index, 
                    disp_stim=stim_obj, target_stim=target, 
                    sub_react='no', sub_RT='None', 
                    note='None')
        return



    def __wait_kb(self, key:list|tuple|dict) -> str:
        '''
        返回按键，不改变外部状态。
        - key: 即可以传入按键字符串列表，也可以将按键字符串作为字典的值将整个字典传入。
        '''
        self.keyboard.clearEvents()

        while True:
            core.wait(0.01)
            pressed = self.keyboard.getKeys()
            if pressed:
                if isinstance(key, list) or isinstance(key, tuple):
                    if pressed[0].name in key:
                        break
                if isinstance(key, dict):
                    if pressed[0].name in key.values():
                        break
            else:
                core.wait(0.01)
                
        return pressed[0].name
    


    def record(self, 
               process_name:str, block_index:int, trial_index:int, 
               disp_stim:str, target_stim:str, sub_react:str, sub_RT:float, 
               note:str, 
               ):
        
        with open(file=self.image_path, mode='a', encoding='utf-8') as file:

            body = (
                f"{self.exp_param['exp_num']},{self.exp_param['disp_mode']},"
                f"{self.exp_param['condition_A']},{self.exp_param['condition_B']},{self.exp_param['condition_C']},"
                f"{dt.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')},{self.clock_global.getTime()},"
                f"{process_name},{block_index},{trial_index},"
                f"{disp_stim},{target_stim},{sub_react},{sub_RT},"
                f"{note}"
                f"\n"
            )

            file.write(body)



    def finale(self):

        self.disp_text(wait=config.duration['wait_finale'], auto=True, text_0=config.text['finale'])
