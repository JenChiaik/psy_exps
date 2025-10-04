# 标准库
import os, json
import datetime as dt
import numpy as np
from PIL import Image

# 自编模块
from config import config

# Psychopy 库
from psychopy import gui, core, visual, event
from psychopy.visual import rect, TextBox2
from psychopy.hardware import keyboard

class Event:

    '''
    包含所有实验事件。
    '''

    def __init__(self, json_file_name:str='random_array.json'):
        '''
        初始化时，须解包一个 json 文件。
        - json: 记录各个 trial 的前景矩形高度信息的 json 文件路径。
        '''

        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.script_dir = self.script_dir.replace('\\', '/')
        json_file_path = os.path.join(self.script_dir, json_file_name)

        with open(file=json_file_path, mode='r', encoding='utf-8') as file:

            dict_arrays = json.load(file) # 静态刺激总字典

            self.block_0_S = dict_arrays['block_0_S'] #练习阶段
            self.block_0_N = dict_arrays['block_0_N'] #练习阶段

            self.block_1_S = dict_arrays['block_1_S'] #阶段 1：中性
            self.block_1_N = dict_arrays['block_1_N'] #阶段 1：中性

            self.block_2_S = dict_arrays['block_2_S'] #阶段 2：诱导 (conterbanlanced)
            self.block_2_N = dict_arrays['block_2_N'] #阶段 2：诱导 (conterbanlanced)

            self.block_3_S = dict_arrays['block_3_S'] #阶段 3：诱导 (conterbanlanced)
            self.block_3_N = dict_arrays['block_3_N'] #阶段 3：诱导 (conterbanlanced)

        self.reward = 0.00



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
                          'manip_order':[1,2], #手动设置 block 2 / 3 的诱导顺序。1 表示先激进再保守；2 表示先保守再激进。
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
                    f"manip_order:{self.exp_param['manip_order']},"
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
                'sys_time,exp_time,process_name,lure,block_index,trial_index,stim_index,'
                'duration,rt,sn,choice,confidence,'
                'note\n'
            )

            file.write(head)



    def prelude(self):
        '''
        初始化 i/o 设备。
        '''

        self.keyboard = keyboard.Keyboard()
        # self.JS = jshub.solo_JS()

        self.win0 = visual.Window(screen=0, title='sub_0', allowGUI=False, 
                                  size=config.windows_param[self.exp_param['disp_mode']]['res'], 
                                #   pos=config.windows_param[self.exp_param['disp_mode']]['pos'][0],
                                  fullscr=True if self.exp_param['disp_mode'] == '1440p_flscr' else False, 
                                  color=config.color_set['bg_white'])

        self.clock_global = core.Clock()
        self.clock_local = core.Clock()

        self.win_ratio = config.windows_param[self.exp_param['disp_mode']]['res'][0] \
            / config.windows_param[self.exp_param['disp_mode']]['res'][1]
        
        # 切换美式键盘布局
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
                    tell process "SystemUIServer"
                        key code 49 using {control down, option down, command down}
                    end tell
                end tell
                '''
                subprocess.run(["osascript", "-e", script])
            except:
                print ('failed to set keyboard with Apple script.')



    def disp_text(self, 
                  wait:int, auto:bool, text_0:str, 
                  pos:tuple=(0,0), align:str='left', boxsize:tuple=(1.5,1.5), 
                  color:str=config.color_set['black'], textsize:int=config.size['text']):
        '''
        - wait: 页面停留时间下限。
        - auto: 自动跳转。
        '''
        try:
            import ctypes
            ctypes.windll.LoadKeyboardLayoutW("00000409", 1)
        except:
            pass

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
            self.__wait_kb(key=config.key_nextpage)



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

    
    
    def dyrect(self, dict_obj:dict, stim_index:int, array_index:int, 
               rect_num:int=config.stim_params['rect_num']):
        '''
        返回每个 trial 中，各个动态矩形（前景）的高度和位置信息；静态矩形（背景）的横坐标亦可通过该方法计算。
        返回值格式： -> dict[str:list[float, float]]
        - dict_obj: 指定解包后的 json_dict, 例如 self.block_2_N 。
        - stim_index: 每种刺激的 index 序数。
        - array_index: 每个 trial 的图形序数。
        - rect_num: 每个 trial 包含的图形数量。
        '''

        width = config.size['rect'][0]
        height = round(number=dict_obj[str(stim_index)][array_index], ndigits=3) #每个动态矩形的高度

        location_x = np.linspace(start=-0.6, stop=0.6, num=rect_num)[array_index]
        location_y = (-config.size['rect'][1] + height)/2

        return {'size':[width, height], 'loca':[location_x, location_y]}



    def block_SD(self, 
                 process_name:str, block_index:int, 
                 signal_num:int, noise_num:int, 
                 rect_num:int=config.stim_params['rect_num'], 
                 duration:float=config.stim_params['duration_stim']):
        '''
        - block_index: 写入文件的标记数据。
        - signal_num / noise_num: 信号 / 噪音刺激的数量，不能超过 .json 对应数组的长度。
        '''

        _map_lure = { #(manip_order, block_index)
            (1, 0):'neutral', 
            (1, 1):'neutral', 
            (1, 2):'punish_MS', #激进
            (1, 3):'punish_FA', #保守
            (2, 0):'neutral',
            (2, 1):'neutral',
            (2, 2):'punish_FA', #激进
            (2, 3):'punish_MS', #保守
        }

        SN_order = np.array([1]*signal_num + [0]*noise_num)
        np.random.shuffle(SN_order)

        trial_index = 0
        S_index = 0
        N_index = 0

        while trial_index < len(SN_order):
            print(f"[DEBUG] Start trial {trial_index} at {self.clock_global.getTime():.4f}")
            self.__trial_SD(lure=_map_lure[(int(self.exp_param['manip_order']), block_index)], 
                            process_name=process_name, block_index=block_index, trial_index=trial_index, 
                            stim_index=S_index if SN_order[trial_index] == 1 else N_index, 
                            sn=SN_order[trial_index], 
                            rect_num=rect_num, stim_duration=duration)
            S_index += 1 if SN_order[trial_index] == 1 else 0
            N_index += 1 if SN_order[trial_index] == 0 else 0
            trial_index += 1
            print(f"[DEBUG] End trial {trial_index} at {self.clock_global.getTime():.4f}")

        # 练习阶段结束时清空收益
        if block_index == 0:
            self.reward = 0

        self.disp_text(wait=2, auto=True, 
                       text_0=config.text['stage_end'])



    def __trial_SD(self, lure:str, process_name:str, block_index:int, trial_index:int, stim_index:int, 
                   sn:int, rect_num:int, stim_duration:int):
        '''
        一个完整 trial，包含刺激呈现、选择操作、收益计算、结果反馈。包含的私有方法调用：
        （1）.__trial_wait: 准备响应；
        （2）.__trial_stim: 呈现刺激；
        （3）.__trial_report: 选择报告；
        （4）.__trial_result: 结果呈现。
        - lure: 
            - 'neutral'，正确奖励，错误无惩罚。
            - 'punish_MS'，激进标准，正确（HT 或 CR）奖励，仅 MS 类错误惩罚。
            - 'punish_FA'，保守标准，正确（HT 或 CR）奖励，仅 FA 类错误惩罚。
        - trial_index: S 和 N 累计的 index，**不可以**用它从 json 解包的字典中调用图形序列，仅用于写入数据。
        - stim_index: S 或 N 独立的 index，可以直接用它从 json 解包的字典中调用图形序列。
        - sn: 0 为噪音，1 为信号。
        - rect_num: 每个 trial 包含的图形序列中矩形的数量，不能超过 .json 中对应数组的长度。
        - scale: 置信度评级的尺度（单向，实际为 2 倍）。
        - stim_duration: 刺激呈现时间。
        '''

        _map_reward_matrix = { #lure:reward_matrix
            'neutral':config.reward_matrix['neutral'], 
            'punish_MS':config.reward_matrix['punish_MS'], 
            'punish_FA':config.reward_matrix['punish_FA'], 
        }

        # 0 被试按键，准备响应当前 trial。
        print(f"→ trial_wait at {self.clock_global.getTime():.4f}")
        self.__trial_wait()

        # 1 呈现注视点
        print(f"→ fixation shown at {self.clock_global.getTime():.4f}")
        self.disp_text(wait=config.stim_params['duration_fixation'], auto=True, text_0='+', 
                       align='center', textsize=config.size['fixation'])

        # 2 呈现刺激
        print(f"→ stim shown at {self.clock_global.getTime():.4f}")
        self.__trial_stim(block_index=block_index, stim_index=stim_index, 
                          sn=sn, rect_num=rect_num, stim_duration=stim_duration)
        
        # 3 选择响应和置信度
        _confidence = 0
        _choice = None

        self.__trial_report(lure=lure, confidence=_confidence)
        self.clock_local.reset()

        while True:

            core.wait(0.01)
            _pressed = self.__wait_kb(key=config.key_operation)

            if _pressed == config.key_operation['s_HC']:
                _confidence = 2
                self.__trial_report(lure=lure, confidence=_confidence)
            elif _pressed == config.key_operation['s_LC']:
                _confidence = 1
                self.__trial_report(lure=lure, confidence=_confidence)
            elif _pressed == config.key_operation['n_LC']:
                _confidence = -1
                self.__trial_report(lure=lure, confidence=_confidence)
            elif _pressed == config.key_operation['n_HC']:
                _confidence = -2
                self.__trial_report(lure=lure, confidence=_confidence)
            elif (_pressed == config.key_operation['confirm']) and (_confidence != 0):
                _choice = 1 if _confidence > 0 else 0
                break
            else:
                continue

        # 4 记录响应，计算收益，展示结果
        self.record(process_name=process_name, lure=lure, 
                    block_index=block_index, trial_index=trial_index, stim_index=stim_index, 
                    stim_duration=stim_duration, rt=self.clock_local.getTime(), 
                    sn=sn, choice=_choice, confidence=_confidence, note='null')

        self.reward += _map_reward_matrix[lure][(sn, _choice)] if sn == _choice \
            else -_map_reward_matrix[lure][(sn, _choice)] # config 中惩罚金额为正值
        self.__trial_result(lure=lure, 
                            sn=sn, choice=_choice, 
                            duration=config.stim_params['duration_result'])



    def __trial_wait(self,
                     text_ready:str=config.text['trial_wait'],
                     text_ready_state:str=config.text['trial_ready_state'],
                     allowed_key:tuple=config.key_nextpage,
                     allowed_bt:tuple=config.jsbt_nextpage,
                     delay:float=config.stim_params['duration_ready_delay']):
        '''
        呈现提示按键准备的界面。
        '''
        _ready = visual.TextBox2(win=self.win0, text=text_ready, 
                                 pos=config.pos['trial_wait'], 
                                 size=(1.5,0.5), alignment='center', 
                                 color=config.color_set['black'], bold=True, 
                                 font='Source Han Serif SC', letterHeight=config.size['text'], lineSpacing=1, 
                                 lineBreaking='uax14', units='norm', editable=False)
        _ready_state = visual.TextBox2(win=self.win0, text=text_ready_state, 
                                       pos=config.pos['trial_ready_state'], 
                                       size=(1.5,0.5), alignment='center', 
                                       color=config.color_set['B'], bold=True, 
                                       font='Source Han Serif SC', letterHeight=config.size['text'], 
                                       lineSpacing=1, units='norm', editable=False)
        
        _ready.draw()
        t0 = self.clock_global.getTime()
        self.win0.flip()
        print(f"[DEBUG] win.flip() took {self.clock_global.getTime()-t0:.4f}s")
        core.wait(delay)
        self.__wait_kb(key=allowed_key)

        _ready.draw(), _ready_state.draw()
        t0 = self.clock_global.getTime()
        self.win0.flip()
        print(f"[DEBUG] win.flip() took {self.clock_global.getTime()-t0:.4f}s")
        core.wait(delay)
    


    def __trial_stim(self, 
                     block_index:int, stim_index:int, 
                     sn:int, rect_num:int, stim_duration:float):
        '''
        呈现刺激。
        '''

        _map_block = { # (block_index, s/n) : block_dict (from .json)
            (0, 1):self.block_0_S, (0, 0):self.block_0_N, 
            (1, 1):self.block_1_S, (1, 0):self.block_1_N, 
            (2, 1):self.block_2_S, (2, 0):self.block_2_N, 
            (3, 1):self.block_3_S, (3, 0):self.block_3_N, 
        }

        bg_rects = [rect.Rect(win=self.win0, 
                            width=config.size['rect'][0], height=config.size['rect'][1], 
                            pos=(np.linspace(start=-0.6, stop=0.6, num=rect_num)[i], 0), 
                            fillColor=config.color_set['bg_white'], 
                            lineColor=config.color_set['black'], 
                            lineWidth=config.size['rect_stroke'], 
                            units='norm') for i in range(rect_num)]
        
        if self.exp_param['note'] == 'renjiayi':
            sn_rects = [rect.Rect(win=self.win0, 
                                width=self.dyrect(dict_obj=_map_block[block_index, sn], 
                                                    stim_index=stim_index, array_index=i, rect_num=rect_num)['size'][0], 
                                height=self.dyrect(dict_obj=_map_block[block_index, sn], 
                                                    stim_index=stim_index, array_index=i, rect_num=rect_num)['size'][1],
                                pos=[np.linspace(start=-0.6, stop=0.6, num=rect_num)[i], 
                                     self.dyrect(dict_obj=_map_block[block_index, sn], 
                                                 stim_index=stim_index, array_index=i, rect_num=rect_num)['loca'][1]], 
                                fillColor=config.color_set['G'] if sn==1 \
                                    else config.color_set['R'], ## 测试用作弊模式
                                lineColor=None, 
                                units='norm') for i in range(rect_num)]
            
            print(f"mean={format(np.mean([self.dyrect(dict_obj=_map_block[block_index, sn], stim_index=stim_index, array_index=i, rect_num=rect_num)['size'][1] for i in range(rect_num)]),'.4f')}")

        else:
            sn_rects = [rect.Rect(win=self.win0, 
                                width=self.dyrect(dict_obj=_map_block[block_index, sn], 
                                                    stim_index=stim_index, array_index=i, rect_num=rect_num)['size'][0], 
                                height=self.dyrect(dict_obj=_map_block[block_index, sn], 
                                                    stim_index=stim_index, array_index=i, rect_num=rect_num)['size'][1],
                                pos=[np.linspace(start=-0.6, stop=0.6, num=rect_num)[i], 
                                    self.dyrect(dict_obj=_map_block[block_index, sn], 
                                                stim_index=stim_index, array_index=i, rect_num=rect_num)['loca'][1]], 
                                fillColor=config.color_set['black'], lineColor=None, 
                                units='norm') for i in range(rect_num)]

        for _ in bg_rects:
            _.draw()
        for _ in sn_rects:
            _.draw()

        self.win0.flip()
        core.wait(stim_duration)


    
    def __trial_report(self, lure:str, confidence:int):
        '''
        渲染并显示报告页面。
        '''
        _map_rule = { # lure : rule_text
            'neutral':config.text['rule_neutral'], 
            'punish_MS':config.text['rule_punish_MS'], 
            'punish_FA':config.text['rule_punish_FA'], 
        }
        _map_sn = { # sn : [text, pos, dyeing_condition, dyeing_color]
            's':[config.text['option_s'], config.pos['trial_scale_sn']['option_s'], lambda confidence:confidence>0, config.color_set['G']], 
            'n':[config.text['option_n'], config.pos['trial_scale_sn']['option_n'], lambda confidence:confidence<0, config.color_set['R']], 
        }
        _map_cf = { # sn_cf : [text, pos, dyeing_condition, dyeing_color]
            's_HC':[config.text['option_HC'], config.pos['trial_scale_cf']['s_HC'], lambda confidence:confidence==2, config.color_set['G']], 
            's_LC':[config.text['option_LC'], config.pos['trial_scale_cf']['s_LC'], lambda confidence:confidence==1, config.color_set['G']], 
            'n_LC':[config.text['option_LC'], config.pos['trial_scale_cf']['n_LC'], lambda confidence:confidence==-1, config.color_set['R']], 
            'n_HC':[config.text['option_HC'], config.pos['trial_scale_cf']['n_HC'], lambda confidence:confidence==-2, config.color_set['R']], 
        }
        _map_key = { # sn_cf : [text, pos, dyeing_condition, dyeing_color]
            's_HC':[f"[ {config.key_operation['s_HC'].capitalize()} ]", config.pos['trial_scale_key']['s_HC'], lambda confidence:confidence==2, config.color_set['G']], 
            's_LC':[f"[ {config.key_operation['s_LC'].capitalize()} ]", config.pos['trial_scale_key']['s_LC'], lambda confidence:confidence==1, config.color_set['G']], 
            'n_LC':[f"[ {config.key_operation['n_LC'].capitalize()} ]", config.pos['trial_scale_key']['n_LC'], lambda confidence:confidence==-1, config.color_set['R']], 
            'n_HC':[f"[ {config.key_operation['n_HC'].capitalize()} ]", config.pos['trial_scale_key']['n_HC'], lambda confidence:confidence==-2, config.color_set['R']], 
        }
        _map_frame = { # cf : frame_pos
            2:(config.pos['trial_scale_cf']['s_HC'][0], config.pos['trial_selected_y']), 
            1:(config.pos['trial_scale_cf']['s_LC'][0], config.pos['trial_selected_y']), 
            -1:(config.pos['trial_scale_cf']['n_LC'][0], config.pos['trial_selected_y']), 
            -2:(config.pos['trial_scale_cf']['n_HC'][0], config.pos['trial_selected_y']), 
        }
        
        _title = visual.TextBox2(win=self.win0, text=config.text['trial_title'], 
                                 lineBreaking='uax14', pos=config.pos['trial_title'], alignment='center', 
                                 color=config.color_set['black'], bold=True, font='Source Han Serif SC', 
                                 letterHeight=config.size['text'], lineSpacing=1, units='norm')
        _rule = visual.TextBox2(win=self.win0, text=_map_rule[lure], 
                                lineBreaking='uax14', pos=config.pos['trial_rule'], alignment='center', 
                                color=config.color_set['B'], bold=True, font='Source Han Serif SC', 
                                letterHeight=config.size['text_small'], lineSpacing=1, units='norm')
        _scale_sn = [visual.TextBox2(win=self.win0, 
                                     text=_map_sn[i][0], pos=_map_sn[i][1], 
                                     color=_map_sn[i][3] if _map_sn[i][2](confidence) else config.color_set['black'], 
                                     alignment='center', bold=True, font='Source Han Serif SC', 
                                     letterHeight=config.size['text_large'], 
                                     lineSpacing=1, units='norm')
                                     for i in _map_sn.keys()]
        _scale_cf = [visual.TextBox2(win=self.win0, 
                                     text=_map_cf[i][0], pos=_map_cf[i][1], 
                                     color=_map_cf[i][3] if _map_cf[i][2](confidence) else config.color_set['black'], 
                                     alignment='center', bold=True, font='Source Han Serif SC', 
                                     letterHeight=config.size['text'], 
                                     lineSpacing=1, units='norm')
                                     for i in _map_cf.keys()]
        _scale_key = [visual.TextBox2(win=self.win0, 
                                      text=_map_key[i][0], pos=_map_key[i][1], 
                                      color=_map_key[i][3] if _map_key[i][2](confidence) else config.color_set['black'], 
                                      alignment='center', bold=True, font='Consolas', 
                                      letterHeight=config.size['text_small'], 
                                      lineSpacing=1, units='norm')
                                      for i in _map_key.keys()]
        _tips = visual.TextBox2(win=self.win0, 
                        text=config.text['wait_confirm'] if confidence else config.text['wait_choice'], 
                        lineBreaking='uax14', pos=config.pos['trial_tips'], alignment='center', 
                        color=config.color_set['black'], bold=True, font='Source Han Serif SC', 
                        letterHeight=config.size['text'], lineSpacing=1, units='norm')
        _reward = visual.TextBox2(win=self.win0, text=f"{config.text['reward']}{format(round(self.reward, 1),'.1f')}", 
                                  pos=config.pos['total_reward'], alignment='center', 
                                  color=config.color_set['B'], bold=True, font='Source Han Serif SC', 
                                  letterHeight=config.size['text_small'], lineSpacing=1, units='norm')
        
        if confidence:
            _frame = rect.Rect(win=self.win0, 
                               width=config.size['selected'][0], height=config.size['selected'][1], 
                               fillColor=None, 
                               lineColor=config.color_set['G'] if confidence > 0 \
                                else config.color_set['R'], 
                               lineWidth=config.size['selected_stroke'], 
                               pos=_map_frame[confidence], 
                               units='norm')
            
        _title.draw(), _rule.draw()
        _tips.draw(), _reward.draw()
        for _ in _scale_sn:
            _.draw()
        for _ in _scale_cf:
            _.draw()
        for _ in _scale_key:
            _.draw()
        if confidence:
            _frame.draw()

        self.win0.flip()


    
    def __trial_result(self, 
                       lure:str, 
                       sn:int, choice:int, 
                       duration:float=config.stim_params['duration_result']):
        '''
        渲染并呈现结果反馈，展示收益情况。
        '''

        _map_rule = { # lure : rule_text
            'neutral':config.text['rule_neutral'], 
            'punish_MS':config.text['rule_punish_MS'], 
            'punish_FA':config.text['rule_punish_FA'], 
        }
        _map_actual = {
            1:config.text['actual_s'], 0:config.text['actual_n']
        }
        _map_choice = {
            1:config.text['choice_s'], 0:config.text['choice_n']
        }
        _map_reward = { # (lure, actual, choice) : (reward_text, colorset)
            ('neutral',1,1):(config.text['reward_plus'], config.color_set['B']), 
            ('neutral',0,0):(config.text['reward_plus'], config.color_set['B']), 
            ('neutral',1,0):(config.text['reward_none'], config.color_set['black']), 
            ('neutral',0,1):(config.text['reward_none'], config.color_set['black']), 
            ('punish_MS',1,1):(config.text['reward_plus'], config.color_set['B']), 
            ('punish_MS',0,0):(config.text['reward_plus'], config.color_set['B']), 
            ('punish_MS',1,0):(config.text['reward_lose'], config.color_set['gray']), #惩罚 miss
            ('punish_MS',0,1):(config.text['reward_none'], config.color_set['black']), #不影响 false alarm
            ('punish_FA',1,1):(config.text['reward_plus'], config.color_set['B']), 
            ('punish_FA',0,0):(config.text['reward_plus'], config.color_set['B']), 
            ('punish_FA',1,0):(config.text['reward_none'], config.color_set['black']), #不影响 miss
            ('punish_FA',0,1):(config.text['reward_lose'], config.color_set['gray']), #惩罚 false alarm
        }
        
        _rule = visual.TextBox2(win=self.win0, text=_map_rule[lure], 
                                lineBreaking='uax14', pos=config.pos['trial_rule'], alignment='center', 
                                color=config.color_set['B'], bold=True, font='Source Han Serif SC', 
                                letterHeight=config.size['text_small'], lineSpacing=1, units='norm')
        _actual = visual.TextBox2(win=self.win0, text=_map_actual[sn], 
                                  pos=config.pos['result_actual'], alignment='center', 
                                  color=config.color_set['G'] if sn == 1 else config.color_set['R'], 
                                  bold=True, font='Source Han Serif SC', 
                                  letterHeight=config.size['text'], lineSpacing=1, units='norm')
        _choice = visual.TextBox2(win=self.win0, text=_map_choice[choice], 
                                  pos=config.pos['result_choice'], alignment='center', 
                                  color=config.color_set['G'] if choice == 1 else config.color_set['R'], 
                                  bold=True, font='Source Han Serif SC', 
                                  letterHeight=config.size['text'], lineSpacing=1, units='norm')
        _result = visual.TextBox2(win=self.win0, text=_map_reward[(lure,sn,choice)][0], 
                                  pos=config.pos['result_reward'], alignment='center', 
                                  color=_map_reward[(lure,sn,choice)][1], 
                                  bold=True, font='Source Han Serif SC', 
                                  letterHeight=config.size['text'], lineSpacing=1, units='norm')
        _reward = visual.TextBox2(win=self.win0, text=f"{config.text['reward']}{format(round(self.reward, 1),'.1f')}", 
                                  pos=config.pos['total_reward'], alignment='center', 
                                  color=config.color_set['B'], bold=True, font='Source Han Serif SC', 
                                  letterHeight=config.size['text_small'], lineSpacing=1, units='norm')

        _rule.draw(), _choice.draw(), _actual.draw(), _result.draw(), _reward.draw()
        self.win0.flip()
        core.wait(duration)



    def intermezzo(self, duration:int=config.stim_params['duration_rest']):
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


    
    def record(self, 
               process_name:str, lure:str, block_index:int, trial_index:int, stim_index:int, 
               stim_duration:float, rt:float, sn:int, choice:int, confidence:int, 
               note:str, 
               ):
        '''
        将每个 trial 的数据记录进单个 .csv 文件。
        - rt: 当前 __trial_report 阶段实际用时。
        '''

        with open(file=self.image_path, mode='a', encoding='utf-8') as file:

            body = (
                f"{self.exp_param['exp_num']},{self.exp_param['disp_mode']},"
                f"{self.exp_param['manip_order']},{self.exp_param['condition_B']},{self.exp_param['condition_C']},"
                f"{dt.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')},{self.clock_global.getTime()},"
                f"{process_name},{lure},{block_index},{trial_index},{stim_index},{stim_duration},{rt},"
                f"{sn},{choice},{confidence},"
                f"{note}"
                f"\n"
            )

            file.write(body)



    def finale(self):
        '''
        实验结束：计算收益。
        '''

        adj_reward = int(max([config.basic_reward, self.reward, self.clock_global.getTime()//60]))

        finale_1 = visual.TextBox2(win=self.win0, text=config.text['finale_1'], 
                                   pos=config.pos['finale_1'], size=(1.5, 1.5), 
                                   color=config.color_set['black'], bold=True, 
                                   font='Source Han Serif SC', 
                                   letterHeight=config.size['text'], lineSpacing=1, 
                                   lineBreaking='uax14', alignment='left', 
                                   units='norm', editable=False)
        finale_2 = visual.TextBox2(win=self.win0, text=f"{config.text['finale_2']}{adj_reward}", 
                                   pos=config.pos['finale_2'], size=(1.5, 1.5), 
                                   color=config.color_set['B'], bold=True, 
                                   font='Source Han Serif SC', 
                                   letterHeight=config.size['text_large'], lineSpacing=1, 
                                   lineBreaking='uax14', alignment='left', 
                                   units='norm', editable=False)
        finale_3 = visual.TextBox2(win=self.win0, text=config.text['finale_3'], 
                                   pos=config.pos['finale_3'], size=(1.5, 1.5), 
                                   color=config.color_set['black'], bold=True, 
                                   font='Source Han Serif SC', 
                                   letterHeight=config.size['text_small'], lineSpacing=1, 
                                   lineBreaking='uax14', alignment='left', 
                                   units='norm', editable=False)
        finale_4 = visual.TextBox2(win=self.win0, text=config.text['finale_4'], 
                                   pos=config.pos['finale_4'], size=(1.5, 1.5), 
                                   color=config.color_set['B'], bold=True, 
                                   font='Source Han Serif SC', 
                                   letterHeight=config.size['text'], lineSpacing=1, 
                                   lineBreaking='uax14', alignment='left', 
                                   units='norm', editable=False)
        
        finale_1.draw(), finale_2.draw(), finale_3.draw(), finale_4.draw()
        self.win0.flip()

        self.__wait_kb(key=config.key_nextpage)
        core.quit()



    def __wait_kb(self, key: list|tuple|dict) -> str:
        '''
        返回按键，不改变外部状态。
        - key: 即可以传入按键字符串列表，也可以将按键字符串作为字典的值将整个字典传入。
        '''
                
        # if self.use_iohub_kb:
        self.keyboard.clearEvents()
        timer = core.Clock()
        while True:
            now = timer.getTime()
            pressed = self.keyboard.getKeys()
            if pressed:
                for p in pressed:
                    print(f"[DEBUG] key={p.name} at iohubTime={p.rt:.4f}, loopTime={now:.4f}")
                    k = p.name
                    if isinstance(key, (list, tuple)) and k in key:
                        return k
                    elif isinstance(key, dict) and k in key.values():
                        return k
        # else:
        #     while True:
        #         core.wait(0.01)
        #         pressed = event.getKeys()
        #         if pressed:
        #             k = pressed[0]
        #             if isinstance(key, (list, tuple)) and k in key:
        #                 return k
        #             elif isinstance(key, dict) and k in key.values():
        #                 return k

    # def __wait_kb(self, key:list|tuple|dict) -> str:
    #     '''
    #     返回按键，不改变外部状态。
    #     - key: 即可以传入按键字符串列表，也可以将按键字符串作为字典的值将整个字典传入。
    #     '''

    #     self.keyboard.clearEvents()

    #     while True:
    #         core.wait(0.01)
    #         pressed = self.keyboard.getKeys()
    #         if pressed:
    #             if isinstance(key, list) or isinstance(key, tuple):
    #                 print (pressed)
    #                 if pressed[0].name in key:
    #                     break
    #             if isinstance(key, dict):
    #                 if pressed[0].name in key.values():
    #                     break
    #         else:
    #             core.wait(0.01)
                
    #     return pressed[0].name

    

if __name__ == '__main__':

    exp = Event()

    exp.overture(log_file_name='log.txt', data_file_dir='data')
    exp.prelude()

    # exp.disp_pic(pic_0='intro_1.png')

    exp.disp_text(wait=1, auto=True, text_0='block=0')
    exp.block_SD(process_name='练习，s2 + n2', block_index=0, signal_num=1, noise_num=1)
    exp.disp_text(wait=1, auto=False, text_0='即将开始。\n按空格键继续。')

    exp.disp_text(wait=1, auto=True, text_0='block=1')
    exp.block_SD(process_name='正式 1，s4',block_index=1, signal_num=3, noise_num=3)
    exp.intermezzo(duration=3)

    exp.disp_text(wait=1, auto=True, text_0='block=2')
    exp.block_SD(process_name='正式 2，n4',block_index=2, signal_num=4, noise_num=2)
    exp.intermezzo(duration=3)

    exp.disp_text(wait=1, auto=True, text_0='block=3')
    exp.block_SD(process_name='正式 3，n4',block_index=3, signal_num=2, noise_num=4)

    exp.finale()
