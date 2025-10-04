
# 标准库
import os, json
import datetime as dt
import random as rd
import numpy as np
from PIL import Image
from scipy import stats

# 自编模块
import jshub
from config import config

# Psychopy 库
from psychopy import gui, core, visual
from psychopy.visual import rect, TextBox2
from psychopy.hardware import keyboard

class Event:

    '''
    包含所有实验事件。
    '''

    def __init__(self, json_file:str='random_array.json'):
        '''
        初始化时，须解包一个 json 文件。
        - json: 记录各个 trail 的前景矩形高度信息的 json 文件路径。
        '''

        with open(file=json_file, mode='r', encoding='utf-8') as file:

            array_dict = json.load(file)

            self.easy_S = array_dict['easy_S']
            self.easy_N = array_dict['easy_N']
            self.hard_S = array_dict['hard_S']
            self.hard_N = array_dict['hard_N']



    def overture(self):
        '''
        创建日志、数据文件，录入被试信息。
        '''

        with open(file='log.txt', mode='r', encoding='utf-8') as log:
            exp_existed = 0
            for _ in log:
                exp_existed += 1
                
        self.exp_param = {'exp_num':exp_existed + 1, 
                          'condition_A':[1,2,3], 'condition_B':[1,2,3], 'condition_C':[1,2,3], 
                          'mode':['2160p_debug','1440p_debug','1440p_flscr'],
                          'note':'None'}
        exp_info = gui.DlgFromDict(dictionary=self.exp_param, order=self.exp_param.keys())

        if exp_info.OK:
            with open(file='log.txt', mode='a', encoding='utf-8') as log:
                log_str = (
                    f"exp_num:{self.exp_param['exp_num']},"
                    f"launch_mode:{self.exp_param['mode']},"
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

        data_dir = os.path.join(os.getcwd(), 'data')
        data_name = f"exp_{self.exp_param['exp_num']}.csv"
        self.data_path = os.path.join(data_dir, data_name)

        with open(file=self.data_path, mode='a', encoding='utf-8') as file:

            head = (
                'exp_num,mode,condition_A,condition_B,condition_C,'
                'sys_time,exp_time,process_name,block_index,trail_index,duration,'
                'actual_stim,choice_0,choice_1,confidence_0,confidence_1,'
                'choice_dual,choice_role,harder_role,'
                'note\n'
            )

            file.write(head)



    def prelude(self):
        '''
        初始化 i/o 设备。
        '''

        self.keyboard = keyboard.Keyboard()
        self.DUAL = jshub.dual_JS()

        self.win0 = visual.Window(screen=0, title='sub_0',
                                  size=config.windows_param[self.exp_param['mode']]['res'], 
                                  pos=config.windows_param[self.exp_param['mode']]['pos'][0],
                                  fullscr=True if self.exp_param['mode'] == '1440p_flscr' else False, 
                                  color=config.color_set['bg_white'])
        self.win1 = visual.Window(screen=1, title='sub_1',
                                  size=config.windows_param[self.exp_param['mode']]['res'], 
                                  pos=config.windows_param[self.exp_param['mode']]['pos'][1],
                                  fullscr=True if self.exp_param['mode'] == '1440p_flscr' else False, 
                                  color=config.color_set['bg_white'])

        self.clock_global = core.Clock()
        self.clock_local = core.Clock()

        self.win_ratio = config.windows_param[self.exp_param['mode']]['res'][0] \
            / config.windows_param[self.exp_param['mode']]['res'][1]



    def disp_text(self, 
                  wait:int, auto:bool, text_0:str, text_1:str, 
                  pos:tuple=(0,0), align:str='left', boxsize:tuple=(1.5,1.5), 
                  color:str=config.color_set['black'], textsize:int=config.size['text']):
        '''
        - wait: 页面停留时间下限。
        - auto: 自动跳转。
        '''

        if text_0:
            text_0 = TextBox2(win=self.win0, text=text_0, lineBreaking='uax14', 
                              pos=pos, size=boxsize, alignment=align, color=color, bold=True,
                              font='Source Han Serif SC', letterHeight=textsize, lineSpacing=1, 
                              units='norm', editable=False)
            text_0.draw()
            self.win0.flip()
            
        if text_1:
            text_1 = TextBox2(win=self.win1, text=text_1, lineBreaking='uax14',
                              pos=pos, size=boxsize, alignment=align, color=color, bold=True, 
                              font='Source Han Serif SC', letterHeight=textsize, lineSpacing=1, 
                              units='norm', editable=False)
            text_1.draw()
            self.win1.flip()

        core.wait(wait)
        if auto:
            return
        else:
            self.__wait_kb()



    def disp_pic(self, 
                 pic_0:str, pic_1:str, wait:float=1, auto:bool=False):
        '''
        - wait: 页面停留时间下限。
        - auto: 自动跳转。
        '''

        ratio_win = config.windows_param[self.exp_param['mode']]['res'][0] / config.windows_param[self.exp_param['mode']]['res'][1]
        
        if pic_0:
            path_0 = 'image/' + pic_0
            with Image.open(path_0) as img_0:
                ratio_pic_0 = img_0.size[0] / img_0.size[1]
            if ratio_pic_0 >= ratio_win: #超宽图片
                pic_x_0 = config.windows_param[self.exp_param['mode']]['res'][0]
                pic_y_0 = img_0.size[1]*pic_x_0/img_0.size[0]
            else: #超高图片
                pic_y_0 = config.windows_param[self.exp_param['mode']]['res'][1]
                pic_x_0 = img_0.size[0]*pic_y_0/img_0.size[1]
            content_win0 = visual.ImageStim(image=path_0, size=(pic_x_0, pic_y_0), units='pix', win=self.win0)
            content_win0.draw(win=self.win0)
            self.win0.flip()
            
        if pic_1:
            path_1 = 'image/' + pic_1
            with Image.open(path_1) as img_1:
                ratio_pic_1 = img_1.size[0] / img_1.size[1]
            if ratio_pic_1 >= ratio_win: #超宽图片
                pic_x_1 = config.windows_param[self.exp_param['mode']]['res'][0]
                pic_y_1 = img_1.size[1]*pic_x_1/img_1.size[0]
            else: #超高图片
                pic_y_1 = config.windows_param[self.exp_param['mode']]['res'][1]
                pic_x_1 = img_1.size[0]*pic_y_1/img_1.size[1]
            content_win1 = visual.ImageStim(image=path_1, size=(pic_x_1, pic_y_1), units='pix', win=self.win1)
            content_win1.draw(win=self.win1)
            self.win1.flip()

        core.wait(wait)
        if auto:
            return
        else:
            self.__wait_kb()

    
    
    def dyrect(self, dict_obj:dict, trail_index:int, array_index:int, 
               rect_num:int=config.stim_param['rect_num']):
        '''
        返回每个 trail 中，各个动态矩形（前景）的高度和位置信息；静态矩形（背景）的横坐标亦可通过该方法计算。
        - dict_obj: 指定解包后的 json_dict, self.easy_S / self.easy_N / self.hard_S / self.hard_N。
        - trail_index: 0 ~ 199，每个 block 至多包含 400 个 trail（200 signal + 200 noise）。
        - array_index: 0 ~ 8，每个 trail 至多包含 9 个图形。
        - rect_num: 每个 trail 包含的图形数量。
        '''

        width = config.size['rect'][0]
        height = round(number=dict_obj[str(trail_index)][array_index], ndigits=3) #每个动态矩形的高度

        location_x = np.linspace(start=-0.6, stop=0.6, num=rect_num)[array_index]
        location_y = (-config.size['rect'][1] + height)/2

        return {'size':[width, height], 'loca':[location_x, location_y]}



    @property
    def solo_d(self):
        '''
        单人任务阶段的鉴别力指数。
        '''

        p_HT_0 = self.HT_0 / config.trail_num['solo'][0]
        p_FA_0 = self.FA_0 / config.trail_num['solo'][1]
        p_HT_1 = self.HT_1 / config.trail_num['solo'][0]
        p_FA_1 = self.FA_1 / config.trail_num['solo'][1]

        z_HT_0 = stats.norm.ppf(p_HT_0) if p_HT_0 != 0 else 0
        z_FA_0 = stats.norm.ppf(p_FA_0) if p_FA_0 != 0 else 0
        z_HT_1 = stats.norm.ppf(p_HT_1) if p_HT_1 != 0 else 0
        z_FA_1 = stats.norm.ppf(p_FA_1) if p_FA_1 != 0 else 0

        d_0 = z_HT_0 - z_FA_0
        d_1 = z_HT_1 - z_FA_1

        return d_0, d_1



    def block_SD(self, 
                 mode:str, 
                 block_index:int, 
                 signal_num:int, noise_num:int, 
                 rect_num:int=config.stim_param['rect_num'], 
                 scale:int=config.stim_param['scale'], 
                 duration:float=config.stim_param['duration_stim']):
        '''
        - mode: 'solo' / 单人任务；'dual' / 双人任务。
        - block_index: 写入文件的标记数据。
        - signal_num / noise_num: 信号 / 噪音刺激的数量（各至多为 100，因为只预制了 400 个数组）。
        '''

        stim_order = np.array([0]*noise_num + [1]*signal_num)
        np.random.shuffle(stim_order)

        if mode == 'solo':
            self.HT_0, self.MS_0, self.CR_0, self.FA_0 = 0, 0, 0, 0
            self.HT_1, self.MS_1, self.CR_1, self.FA_1 = 0, 0, 0, 0
            harder = -1
        elif mode == 'dual':
            harder = 0 if self.solo_d[0] <= self.solo_d[1] else 1
            
        trail_index = 0

        while trail_index < len(stim_order):
            self.__trail_SD(mode=mode, harder=harder, decision_role=rd.choice([0,1]), 
                            block_index=block_index, trail_index=trail_index, 
                            sn=stim_order[trail_index], 
                            rect_num=rect_num, scale=scale, duration=duration)
            trail_index += 1



    def __trail_SD(self, 
                   mode:str, harder:int, decision_role:int, 
                   block_index:int, trail_index:int, 
                   sn:int, rect_num:int, scale:int, duration:float):
        '''
        - mode: 'solo' / 单人任务；'dual' / 双人任务。
        - harder: 提高难度的一方，仅适用于 mode=='dual'。
        - desicion_role：如果双方选择不一致，有谁进行最终选择，仅适用于 mode=='dual'。
        - block_index: 写入文件的标记数据。
        - trail_index: 写入文件的标记数据。
        - sn: 0 / 噪音，1 / 信号。
        - rect_num: 每个序列中矩形的数量。
        - scale: 量表单项尺度（实际为 2 倍）。
        - duration: 矩形序列呈现的时间。
        '''

        self.clock_local.reset()

        # 0 准备响应

        self.__disp_wait_js()
        
        # 1 注视点呈现

        self.disp_text(wait=config.stim_param['duration_fixation'], auto=True, text_0='+', text_1='+', 
                       align='center', textsize=config.size['fixation'])

        # 2 刺激呈现

        self.__disp_stim(mode=mode, harder=harder, 
                         block_index=block_index, trail_index=trail_index, 
                         sn=sn, rect_num=rect_num, duration=duration)

        # 3 单独报告

        confidence_0 = 0
        confidence_1 = 0
        choice_solo_0 = None
        choice_solo_1 = None
        finished_solo_0 = False
        finished_solo_1 = False
        _js_solo_before_0 = [False]*len(self.DUAL.js0.getAllButtons())
        _js_solo_before_1 = [False]*len(self.DUAL.js1.getAllButtons())

        self.__render_solo(scale=scale, confidence_0=confidence_0, confidence_1=confidence_1, 
                           render_win0=True, render_win1=True)
        self.win0.flip(), self.win1.flip()

        while (not finished_solo_0) or (not finished_solo_1):
            
            core.wait(0.01)
            self.DUAL.win_flipper.flip()
            _pressed_0, _pressed_1 = self.DUAL.check_js(_js0_before=_js_solo_before_0, _js1_before=_js_solo_before_1)

            if (not finished_solo_0) and _pressed_0:

                if (_pressed_0 == 'LB') and (confidence_0 < 6):
                    confidence_0 += 1 if confidence_0 != -1 else 2
                    self.__render_solo(scale=scale, confidence_0=confidence_0, confidence_1=confidence_1, 
                                       render_win0=True, render_win1=False)
                    self.win0.flip()

                elif (_pressed_0 == 'RB') and (confidence_0 > -6):
                    confidence_0 -= 1 if confidence_0 != 1 else 2
                    self.__render_solo(scale=scale, confidence_0=confidence_0, confidence_1=confidence_1, 
                                       render_win0=True, render_win1=False)
                    self.win0.flip()

                elif (_pressed_0 == 'Y_A') and (confidence_0 != 0):
                    if confidence_0 != 0:
                        choice_solo_0 = 1 if confidence_0 > 0 else 0
                        finished_solo_0 = True
                        self.__disp_wait(win=self.win0, text=config.text['wait_allay_solo'])
                        self.__judger(sn=sn, role=0, choice=choice_solo_0)

            elif (not finished_solo_1) and _pressed_1:

                if (_pressed_1 == 'LB') and (confidence_1 < 6):
                    confidence_1 += 1 if confidence_1 != -1 else 2
                    self.__render_solo(scale=scale, confidence_0=confidence_0, confidence_1=confidence_1, 
                                       render_win0=False, render_win1=True)
                    self.win1.flip()

                elif (_pressed_1 == 'RB') and (confidence_1 > -6):
                    confidence_1 -= 1 if confidence_1 != 1 else 2
                    self.__render_solo(scale=scale, confidence_0=confidence_0, confidence_1=confidence_1, 
                                       render_win0=False, render_win1=True)
                    self.win1.flip()

                elif (_pressed_1 == 'Y_A') and (confidence_1 != 0):
                    if confidence_1 != 0:
                        choice_solo_1 = 1 if confidence_1 > 0 else 0
                        finished_solo_1 = True
                        self.__disp_wait(win=self.win1, text=config.text['wait_allay_solo'])
                        self.__judger(sn=sn, role=1, choice=choice_solo_1)

        # 4 联合报告（可选）

        if mode == 'dual':
            pass
        elif mode == 'solo':
            self.record(process_name='solo_SD', block_index=block_index, trail_index=trail_index, 
                        duration=self.clock_local.getTime(), actual_stim=sn, 
                        choice_0=1 if confidence_0>0 else 0, choice_1=1 if confidence_1>0 else 0,
                        confidence_0=confidence_0, confidence_1=confidence_1, 
                        choice_dual='null', choice_role='null', harder_role='null')
            return
        else:
            raise ValueError(f'\n__trail_SD 方法错误的参数：mode={mode}\n')
        
        decision_ready = None
        decision_final = None
        _js_solo_before_0 = [False]*len(self.DUAL.js0.getAllButtons())
        _js_solo_before_1 = [False]*len(self.DUAL.js1.getAllButtons())

        if choice_solo_0 == choice_solo_1: #双方选择相同

            decision_final = choice_solo_0

            self.__render_dual(choice_solo_0=choice_solo_0, choice_solo_1=choice_solo_1,
                               confidence_0=confidence_0, confidence_1=confidence_1, 
                               decision_role=decision_role, decision_ready=decision_ready)
            self.win0.flip(), self.win1.flip()
            
            core.wait(5)

        else: #双方选择不同

            while decision_final == None:

                core.wait(0.01)
                self.DUAL.win_flipper.flip()
                _pressed_0, _pressed_1 = self.DUAL.check_js(_js0_before=_js_solo_before_0, _js1_before=_js_solo_before_1)

                self.__render_dual(sn=sn, 
                                   choice_solo_0=choice_solo_0, choice_solo_1=choice_solo_1,
                                   confidence_0=confidence_0, confidence_1=confidence_1, 
                                   decision_role=decision_role, decision_ready=decision_ready)
                self.win0.flip(), self.win1.flip()

                if decision_role == 0:

                    if _pressed_0 == 'LB':
                        decision_ready = 1
                        self.__render_dual(sn=sn, 
                                           choice_solo_0=choice_solo_0, choice_solo_1=choice_solo_1, 
                                           confidence_0=confidence_0, confidence_1=confidence_1, 
                                           decision_role=decision_role, decision_ready=decision_ready)
                        self.win0.flip(), self.win1.flip()

                    elif _pressed_0 == 'RB':
                        decision_ready = 0
                        self.__render_dual(sn=sn, 
                                           choice_solo_0=choice_solo_0, choice_solo_1=choice_solo_1, 
                                           confidence_0=confidence_0, confidence_1=confidence_1, 
                                           decision_role=decision_role, decision_ready=decision_ready)
                        self.win0.flip(), self.win1.flip()

                    elif (_pressed_0 == 'Y_A') and (decision_ready != None):
                        decision_final = decision_ready

                elif decision_role == 1:

                    if _pressed_1 == 'LB':
                        decision_ready = 1
                        self.__render_dual(sn=sn, 
                                           choice_solo_0=choice_solo_0, choice_solo_1=choice_solo_1, 
                                           confidence_0=confidence_0, confidence_1=confidence_1, 
                                           decision_role=decision_role, decision_ready=decision_ready)
                        self.win0.flip(), self.win1.flip()

                    elif _pressed_1 == 'RB':
                        decision_ready = 0
                        self.__render_dual(sn=sn, 
                                           choice_solo_0=choice_solo_0, choice_solo_1=choice_solo_1, 
                                           confidence_0=confidence_0, confidence_1=confidence_1, 
                                           decision_role=decision_role, decision_ready=decision_ready)
                        self.win0.flip(), self.win1.flip()

                    elif (_pressed_1 == 'Y_A') and (decision_ready != None):
                        decision_final = decision_ready
                        
            self.disp_text(wait=3, auto=True, align='center', textsize=config.size['text_large'], 
                           text_0=config.text['final_choice_s'] if decision_final == 1 else config.text['final_choice_n'], 
                           text_1=config.text['final_choice_s'] if decision_final == 1 else config.text['final_choice_n'])
        
        self.record(process_name='dual_SD', block_index=block_index, trail_index=trail_index, 
                    duration=self.clock_local.getTime(), actual_stim=sn, 
                    choice_0=1 if confidence_0>0 else 0, choice_1=1 if confidence_1>0 else 0,
                    confidence_0=confidence_0, confidence_1=confidence_1, 
                    choice_dual=decision_final, 
                    choice_role=decision_role, 
                    harder_role=harder)
        return



    def __judger(self, sn:int, role:int, choice:int):
        '''
        判断结果，计数并记录在实例的属性（inst_attr）中。
        - sn: 0 / 噪音，1 / 信号。
        - role: 做出当前选择的个体（0 / 1）。
        - choice: 当前个体做出的选择（0 / 噪音，1 / 信号）。
        '''
        results = {
            0: {1: {1: "HT_0", 0: "MS_0"},
                0: {1: "FA_0", 0: "CR_0"}},
            1: {1: {1: "HT_1", 0: "MS_1"},
                0: {1: "FA_1", 0: "CR_1"}}
                }
        
        inst_attr = results[role][sn][choice]
        
        ori_value = getattr(self, inst_attr)
        setattr(self, inst_attr, ori_value + 1)


    
    def __disp_stim(self, 
                    mode:str, harder:int, 
                    block_index:int, trail_index:int, 
                    sn:int, rect_num:int, duration:float):
        '''
        渲染视觉刺激。
        '''

        if mode == 'solo':
            signal_0 = self.easy_S
            signal_1 = self.easy_S
            noise_0 = self.easy_N
            noise_1 = self.easy_N
        elif mode == 'dual' and harder == 0:
            signal_0 = self.hard_S
            signal_1 = self.easy_S
            noise_0 = self.hard_N
            noise_1 = self.easy_N
        elif mode == 'dual' and harder == 1:
            signal_0 = self.easy_S
            signal_1 = self.hard_S
            noise_0 = self.easy_N
            noise_1 = self.hard_N
        else:
            raise ValueError(f'\n__disp_stim 方法错误的参数：mode={mode}, harder={harder}.\n')

        bg_rects_0 = [rect.Rect(win=self.win0, 
                                width=config.size['rect'][0], height=config.size['rect'][1], 
                                lineColor=config.color_set['bg_black'], 
                                lineWidth=config.size['rect_stroke'], 
                                fillColor=config.color_set['bg_white'], 
                                pos=(np.linspace(start=-0.6, stop=0.6, num=rect_num)[i], 0), 
                                units='norm') for i in range(rect_num)]
        bg_rects_1 = [rect.Rect(win=self.win1, 
                                width=config.size['rect'][0], height=config.size['rect'][1], 
                                lineColor=config.color_set['bg_black'], 
                                lineWidth=config.size['rect_stroke'], 
                                fillColor=config.color_set['bg_white'], 
                                pos=(np.linspace(start=-0.6, stop=0.6, num=rect_num)[i], 0), 
                                units='norm') for i in range(rect_num)]
        
        sn_rects_0 = [rect.Rect(win=self.win0, 
                                width=self.dyrect(dict_obj=signal_0 if sn==1 else noise_0, 
                                                  trail_index=trail_index, array_index=i, rect_num=rect_num)['size'][0], 
                                height=self.dyrect(dict_obj=signal_0 if sn==1 else noise_0, 
                                                   trail_index=trail_index, array_index=i, rect_num=rect_num)['size'][1], 
                                fillColor=config.color_set['black'], 
                                pos=(np.linspace(start=-0.6, stop=0.6, num=rect_num)[i], 
                                     self.dyrect(dict_obj=signal_0 if sn==1 else noise_0, 
                                                 trail_index=trail_index, array_index=i, rect_num=rect_num)['loca'][1]), 
                                units='norm') for i in range(rect_num)]
        sn_rects_1 = [rect.Rect(win=self.win1, 
                                width=self.dyrect(dict_obj=signal_1 if sn==1 else noise_1, 
                                                  trail_index=trail_index, array_index=i, rect_num=rect_num)['size'][0], 
                                height=self.dyrect(dict_obj=signal_1 if sn==1 else noise_1, 
                                                   trail_index=trail_index, array_index=i, rect_num=rect_num)['size'][1], 
                                fillColor=config.color_set['black'], 
                                pos=(np.linspace(start=-0.6, stop=0.6, num=rect_num)[i], 
                                     self.dyrect(dict_obj=signal_1 if sn==1 else noise_1, 
                                                 trail_index=trail_index, array_index=i, rect_num=rect_num)['loca'][1]), 
                                units='norm') for i in range(rect_num)]
        
        for _ in bg_rects_0:
            _.draw()
        for _ in sn_rects_0:
            _.draw()
        for _ in bg_rects_1:
            _.draw()
        for _ in sn_rects_1:
            _.draw()
        self.win0.flip(), self.win1.flip()
        core.wait(duration)



    def __render_solo(self, scale:int, 
                      render_win0:bool, render_win1:bool, 
                      confidence_0:int=0, confidence_1:int=0):
        '''
        渲染单独报告的画面，同时适用于 mode='solo'/'dual' 的独立报告阶段。
        - render_win0/1: 是否渲染 0/1 的画面。
        '''

        loca_scale = [(np.linspace(-0.55,0.55,scale*2)[i], config.pos['trail_scale_y']) \
                      for i in range(scale*2)]
        
        if render_win0:
            title_0 = visual.TextBox2(win=self.win0, text=config.text['trail_title'], lineBreaking='uax14', 
                                      pos=config.pos['trail_title'], alignment='center', 
                                      color=config.color_set['black'], bold=True, 
                                      font='Source Han Serif SC', 
                                      letterHeight=config.size['text'], lineSpacing=1, 
                                      units='norm')
            scale_0 = [visual.TextBox2(win=self.win0, 
                                       text=f' 是\n{6-i}' if i < scale else f' 否\n{i-5}', 
                                       lineBreaking='uax14', 
                                       pos=loca_scale[i], 
                                       alignment='center', 
                                       color=config.color_set['black'], bold=True, 
                                       font='Source Han Serif SC', 
                                       letterHeight=config.size['text_small'], lineSpacing=1, 
                                       units='norm') \
                                        for i in range(scale*2)]
            if confidence_0:
                selected_0 = rect.Rect(win=self.win0, 
                                       width=config.size['selected'][0], 
                                       height=config.size['selected'][1], 
                                       fillColor=None, 
                                       lineColor=config.color_set['G'] if confidence_0 > 0 else config.color_set['R'], 
                                       lineWidth=config.size['selected_stroke'], 
                                       pos=loca_scale[6-confidence_0] if confidence_0 > 0 else loca_scale[5-confidence_0], 
                                       units='norm')
                choice_0 = visual.TextBox2(win=self.win0, 
                                           text=f"{config.text['pos']}（信心：{confidence_0}）" if confidence_0 > 0 \
                                            else f"{config.text['neg']}（信心：{-confidence_0}）", 
                                           lineBreaking='uax14', 
                                           pos=config.pos['trail_choice'], alignment='center', 
                                           color=config.color_set['G'] if confidence_0 > 0 else config.color_set['R'], 
                                           bold=True, font='Source Han Serif SC', 
                                           letterHeight=config.size['text'], lineSpacing=1, 
                                           units='norm')
            else:
                choice_0 = visual.TextBox2(win=self.win0, 
                                           text=config.text['wait_choice'], 
                                           lineBreaking='uax14', 
                                           pos=config.pos['trail_choice'], alignment='center', 
                                           color=config.color_set['B'], 
                                           bold=True, font='Source Han Serif SC', 
                                           letterHeight=config.size['text'], lineSpacing=1, 
                                           units='norm')
            title_0.draw(), choice_0.draw()
            if confidence_0:
                selected_0.draw()
            for _ in scale_0:
                _.draw()

        if render_win1:
            title_1 = visual.TextBox2(win=self.win1, text=config.text['trail_title'], lineBreaking='uax14', 
                                      pos=config.pos['trail_title'], alignment='center', 
                                      color=config.color_set['black'], bold=True, 
                                      font='Source Han Serif SC', 
                                      letterHeight=config.size['text'], lineSpacing=1, 
                                      units='norm')
            scale_1 = [visual.TextBox2(win=self.win1, 
                                       text=f' 是\n{6-i}' if i < scale else f' 否\n{i-5}', 
                                       lineBreaking='uax14', 
                                       pos=loca_scale[i], 
                                       alignment='center', 
                                       color=config.color_set['black'], bold=True, 
                                       font='Source Han Serif SC', 
                                       letterHeight=config.size['text_small'], lineSpacing=1, 
                                       units='norm') \
                                        for i in range(scale*2)]
                
            if confidence_1:
                selected_1 = rect.Rect(win=self.win1, 
                                       width=config.size['selected'][0], 
                                       height=config.size['selected'][1], 
                                       fillColor=None, 
                                       lineColor=config.color_set['G'] if confidence_1 > 0 else config.color_set['R'], 
                                       lineWidth=config.size['selected_stroke'], 
                                       pos=loca_scale[6-confidence_1] if confidence_1 > 0 else loca_scale[5-confidence_1], 
                                       units='norm')
                choice_1 = visual.TextBox2(win=self.win1, 
                                           text=f"{config.text['pos']}（信心：{confidence_1}）" if confidence_1 > 0 \
                                            else f"{config.text['neg']}（信心：{-confidence_1}）", 
                                           lineBreaking='uax14', 
                                           pos=config.pos['trail_choice'], alignment='center', 
                                           color=config.color_set['G'] if confidence_1 > 0 else config.color_set['R'], 
                                           bold=True, font='Source Han Serif SC', 
                                           letterHeight=config.size['text'], lineSpacing=1, 
                                           units='norm')
            else:
                choice_1 = visual.TextBox2(win=self.win1, 
                                           text=config.text['wait_choice'], 
                                           lineBreaking='uax14', 
                                           pos=config.pos['trail_choice'], alignment='center', 
                                           color=config.color_set['B'], 
                                           bold=True, font='Source Han Serif SC', 
                                           letterHeight=config.size['text'], lineSpacing=1, 
                                           units='norm')
            title_1.draw(), choice_1.draw()
            if confidence_1:
                selected_1.draw()
            for _ in scale_1:
                _.draw()
        


    def __render_dual(self, sn:int, 
                      choice_solo_0:int, choice_solo_1:int, 
                      confidence_0:int, confidence_1:int, 
                      decision_role:int, decision_ready:int):
        '''
        渲染联合报告页面的 UI（适用于双方独立选择相同 / 不同的情况）。
        - decision_role: 如果意见不同，由哪一方进行最终判断。
        - decision_ready: 0 / 1，联合判断的备选选择。
        '''

        choice_self_0_text = f'您的选择：“是”（信心：{confidence_0}）' if confidence_0 > 0 else f'您的选择：“否”（信心：{-confidence_0}）'
        choice_allay_0_text = f'对方选择：“是”（信心：{confidence_1}）' if confidence_1 > 0 else f'对方选择：“否”（信心：{-confidence_1}）'
        choice_self_1_text = f'您的选择：“是”（信心：{confidence_1}）' if confidence_1 > 0 else f'您的选择：“否”（信心：{-confidence_1}）'
        choice_allay_1_text = f'对方选择：“是”（信心：{confidence_0}）' if confidence_0 > 0 else f'对方选择：“否”（信心：{-confidence_0}）'
        _choice_final_text = {0:config.text['neg_final'], 1:config.text['pos_final']}

        choice_self_0 = visual.TextBox2(win=self.win0, text=choice_self_0_text, lineBreaking='uax14', 
                                        pos=config.pos['final_self'], alignment='center', 
                                        color=config.color_set['G'] if choice_solo_0 == 1 else config.color_set['R'], 
                                        bold=True, font='Source Han Serif SC', 
                                        letterHeight=config.size['text'], lineSpacing=1, 
                                        units='norm')
        choice_allay_0 = visual.TextBox2(win=self.win0, text=choice_allay_0_text, lineBreaking='uax14', 
                                         pos=config.pos['final_allay'], alignment='center', 
                                         color=config.color_set['G'] if choice_solo_1 == 1 else config.color_set['R'], 
                                         bold=True, font='Source Han Serif SC', 
                                         letterHeight=config.size['text'], lineSpacing=1, 
                                         units='norm')
        choice_self_1 = visual.TextBox2(win=self.win1, text=choice_self_1_text, lineBreaking='uax14', 
                                        pos=config.pos['final_self'], alignment='center', 
                                        color=config.color_set['G'] if choice_solo_1 == 1 else config.color_set['R'], 
                                        bold=True, font='Source Han Serif SC', 
                                        letterHeight=config.size['text'], lineSpacing=1, 
                                        units='norm')
        choice_allay_1 = visual.TextBox2(win=self.win1, text=choice_allay_1_text, lineBreaking='uax14', 
                                         pos=config.pos['final_allay'], alignment='center', 
                                         color=config.color_set['G'] if choice_solo_0 == 1 else config.color_set['R'], 
                                         bold=True, font='Source Han Serif SC', 
                                         letterHeight=config.size['text'], lineSpacing=1, 
                                         units='norm')

        if choice_solo_0 == choice_solo_1: #双方选择一致

            _choice_0 = visual.TextBox2(win=self.win0, 
                                        text=config.text['same_choice_s'] if choice_solo_0 == 1 else config.text['same_choice_n'], 
                                        lineBreaking='uax14', 
                                        pos=config.pos['final_choice'], alignment='center', 
                                        color=config.color_set['black'], 
                                        bold=True, font='Source Han Serif SC', 
                                        letterHeight=config.size['text_large'], lineSpacing=1, 
                                        units='norm')
            _choice_1 = visual.TextBox2(win=self.win1, 
                                        text=config.text['same_choice_s'] if choice_solo_1 == 1 else config.text['same_choice_n'], 
                                        lineBreaking='uax14', 
                                        pos=config.pos['final_choice'], alignment='center', 
                                        color=config.color_set['black'], 
                                        bold=True, font='Source Han Serif SC', 
                                        letterHeight=config.size['text_large'], lineSpacing=1, 
                                        units='norm')

        else: #双方选择不一致

            if decision_role == 0:
                _choice_0 = visual.TextBox2(win=self.win0, 
                                            text=config.text['wait_self_dual'] if decision_ready == None else _choice_final_text[decision_ready], 
                                            lineBreaking='uax14', 
                                            pos=config.pos['final_choice'], alignment='center', 
                                            color=config.color_set['B'], 
                                            bold=True, font='Source Han Serif SC', 
                                            letterHeight=config.size['text_large'], lineSpacing=1, 
                                            units='norm')
                _choice_1 = visual.TextBox2(win=self.win1, 
                                            text=config.text['wait_allay_dual'], 
                                            lineBreaking='uax14', 
                                            pos=config.pos['final_choice'], alignment='center', 
                                            color=config.color_set['black'], 
                                            bold=True, font='Source Han Serif SC', 
                                            letterHeight=config.size['text_large'], lineSpacing=1, 
                                            units='norm')

            elif decision_role == 1:
                _choice_0 = visual.TextBox2(win=self.win0, 
                                            text=config.text['wait_allay_dual'], 
                                            lineBreaking='uax14', 
                                            pos=config.pos['final_choice'], alignment='center', 
                                            color=config.color_set['black'], 
                                            bold=True, font='Source Han Serif SC', 
                                            letterHeight=config.size['text_large'], lineSpacing=1, 
                                            units='norm')
                _choice_1 = visual.TextBox2(win=self.win1, 
                                            text=config.text['wait_self_dual'] if decision_ready == None else _choice_final_text[decision_ready], 
                                            lineBreaking='uax14', 
                                            pos=config.pos['final_choice'], alignment='center', 
                                            color=config.color_set['B'], 
                                            bold=True, font='Source Han Serif SC', 
                                            letterHeight=config.size['text_large'], lineSpacing=1, 
                                            units='norm')

        choice_self_0.draw(), choice_self_1.draw()
        choice_allay_0.draw(), choice_allay_1.draw()
        _choice_0.draw(), _choice_1.draw()
        
    

    def __disp_wait(self, win:visual.Window, text:str):
        '''
        向一个窗口呈现等待提示。
        '''

        content = visual.TextBox2(win=win, text=text, 
                                  pos=(0,0), size=(1.5,0.5), alignment='left', color=config.color_set['black'], bold=True,
                                  font='Source Han Serif SC', letterHeight=config.size['text'], lineSpacing=1, 
                                  lineBreaking='uax14', units='norm', editable=False)
        content.draw()
        win.flip()



    def __disp_wait_js(self, 
                       text_ready:str=config.text['trail_ready'], 
                       text_ready_self:str=config.text['trail_ready_self'], 
                       text_ready_allay:str=config.text['trail_ready_allay'], 
                       allowed_bt:tuple=config.allowed_bt):
        '''
        给被试写的方法，默认双方均按下【Y】+【A】之后才跳转。
        - text_ready: 提示被试按键准备的文字。
        - text_ready_self/allay: 自己和对方按要求按键后的状态文字。
        '''

        ready_text_0 = visual.TextBox2(win=self.win0, text=text_ready, 
                                       pos=config.pos['trail_ready'], 
                                       size=(1.5,0.5), alignment='center', 
                                       color=config.color_set['black'], bold=True, 
                                       font='Source Han Serif SC', letterHeight=config.size['text'], lineSpacing=1, 
                                       lineBreaking='uax14', units='norm', editable=False)
        ready_text_1 = visual.TextBox2(win=self.win1, text=text_ready, 
                                       pos=config.pos['trail_ready'], 
                                       size=(1.5,0.5), alignment='center', 
                                       color=config.color_set['black'], bold=True, 
                                       font='Source Han Serif SC', letterHeight=config.size['text'], lineSpacing=1, 
                                       lineBreaking='uax14', units='norm', editable=False)
        ready_self_0 = visual.TextBox2(win=self.win0, text=text_ready_self, 
                                       pos=config.pos['trail_ready_self'], 
                                       size=(1.5,0.5), alignment='center', 
                                       color=config.color_set['B'], bold=True, 
                                       font='Source Han Serif SC', letterHeight=config.size['text'], lineSpacing=1, 
                                       lineBreaking='uax14', units='norm', editable=False)
        ready_allay_0 = visual.TextBox2(win=self.win0, text=text_ready_allay, 
                                        pos=config.pos['trail_ready_allay'], 
                                        size=(1.5,0.5), alignment='center', 
                                        color=config.color_set['B'], bold=True, 
                                        font='Source Han Serif SC', letterHeight=config.size['text'], lineSpacing=1, 
                                        lineBreaking='uax14', units='norm', editable=False)
        ready_self_1 = visual.TextBox2(win=self.win1, text=text_ready_self, 
                                       pos=config.pos['trail_ready_self'], 
                                       size=(1.5,0.5), alignment='center', 
                                       color=config.color_set['B'], bold=True, 
                                       font='Source Han Serif SC', letterHeight=config.size['text'], lineSpacing=1, 
                                       lineBreaking='uax14', units='norm', editable=False)
        ready_allay_1 = visual.TextBox2(win=self.win1, text=text_ready_allay, 
                                        pos=config.pos['trail_ready_allay'], 
                                        size=(1.5,0.5), alignment='center', 
                                        color=config.color_set['B'], bold=True, 
                                        font='Source Han Serif SC', letterHeight=config.size['text'], lineSpacing=1, 
                                        lineBreaking='uax14', units='norm', editable=False)
        ready_text_0.draw(), ready_text_1.draw()
        self.win0.flip(), self.win1.flip()

        ready_0 = False
        ready_1 = False
        _js_solo_before_0 = [False]*len(self.DUAL.js0.getAllButtons())
        _js_solo_before_1 = [False]*len(self.DUAL.js1.getAllButtons())

        while (not ready_0) or (not ready_1):
            
            core.wait(0.01)
            self.DUAL.win_flipper.flip()
            _pressed_0, _pressed_1 = self.DUAL.check_js(_js0_before=_js_solo_before_0, _js1_before=_js_solo_before_1)

            if (not ready_0) and (_pressed_0 in allowed_bt):
                ready_0 = True
                ready_text_0.draw(), ready_text_1.draw()
                ready_self_0.draw(), ready_allay_1.draw()
                if ready_1:
                    ready_allay_0.draw(), ready_self_1.draw()
                self.win0.flip(), self.win1.flip()

            elif (not ready_1) and (_pressed_1 in allowed_bt):
                ready_1 = True
                ready_text_0.draw(), ready_text_1.draw()
                ready_self_1.draw(), ready_allay_0.draw()
                if ready_0:
                    ready_allay_1.draw(), ready_self_0.draw()
                self.win0.flip(), self.win1.flip()

        core.wait(config.stim_param['duration_ready_delay'])
        return



    def __wait_kb(self, key:tuple=config.allowed_key):
        '''
        给主试写的方法，默认按空格键跳转，主要用于指导语翻页。
        返回按键，不改变外部状态。
        '''

        self.keyboard.clearEvents()
        while True:
            pressed = self.keyboard.getKeys()
            if pressed:
                if pressed[-1].name in key:
                    break
            else:
                core.wait(0.01)
                
        return pressed[-1]
    


    def record(self, 
               process_name:str, block_index:int, trail_index:int, duration:float, 
               actual_stim:int, choice_0:int, choice_1:int, confidence_0:int, confidence_1:int, 
               choice_dual:int, choice_role:int, harder_role:int, note:str='null', ):
        '''
        将每个 trail 记录进数据文件。
        '''

        with open(file=self.data_path, mode='a', encoding='utf-8') as file:

            body = (
                f"{self.exp_param['exp_num']},{self.exp_param['mode']},"
                f"{self.exp_param['condition_A']},{self.exp_param['condition_B']},{self.exp_param['condition_C']},"
                f"{dt.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')},{self.clock_global.getTime()},"
                f"{process_name},{block_index},{trail_index},{duration},"
                f"{actual_stim},{choice_0},{choice_1},{confidence_0},{confidence_1},"
                f"{choice_dual},{choice_role},{harder_role},{note}"
                f"\n"
            )

            file.write(body)



    def finale(self):
        '''
        计算收益，结束实验。
        '''

        exp_time = self.clock_global.getTime()
        basic_reward = exp_time / 60 * 1.25
        if basic_reward < 50:
            basic_reward = 50
        elif basic_reward > 75:
            basic_reward = 75

        self.disp_text(wait=5, auto=False, 
                       text_0=f"被试费：￥{str(format(basic_reward, '.2f'))}", 
                       text_1=f"被试费：￥{str(format(basic_reward, '.2f'))}")
        self.disp_text(wait=5, auto=True, 
                       text_0=config.text['finale'], 
                       text_1=config.text['finale'])
        
        core.quit()
        

    
if __name__ == '__main__':

    exp = Event()
    exp.overture()
    exp.prelude()
    exp.disp_text(wait=2, auto=False, text_0='单人阶段……\n这是sub_0', text_1='单人阶段……\n这是sub_1')
    exp.block_SD(mode='solo', block_index=1, signal_num=3, noise_num=3)
    print(f'hit:{exp.HT_0}, miss:{exp.MS_0}, cr:{exp.CR_0}, fa:{exp.FA_0}')
    exp.disp_text(wait=2, auto=False, text_0='双人阶段……\n这是sub_0', text_1='双人阶段……\n这是sub_1')
    exp.block_SD(mode='dual', block_index=2, signal_num=3, noise_num=3)