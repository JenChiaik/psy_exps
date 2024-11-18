'''
实验中包含的各个事件。
'''

# 内置模块
import os, copy
import datetime as dt
import random as rd
import numpy as np
from PIL import Image

# 自编模块
from trial import PGG
from jshub import dual_JS
from config import config

# Psychopy 模块
from psychopy import gui, core, visual
from psychopy.visual import circle, rect, TextBox2
from psychopy.hardware import keyboard



class Event:

    def __init__(self):
        '''
        录入信息，写入日志，创建数据文件。
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

        trial_data_dir = os.path.join(os.getcwd(), 'data_trial')
        trial_data_name = f"exp_{self.exp_param['exp_num']}.csv"
        self.path_data_trial = os.path.join(trial_data_dir, trial_data_name)
        self.path_data_summary = os.path.join(os.getcwd(), 'data_summary.csv')

        with open(file=self.path_data_trial, mode='a', encoding='utf-8') as file:

            head = (
                'exp_num,mode,condition_A,condition_B,condition_C,'
                'sys_time,exp_time,process_name,STAGE_index,trial_index,duration,'
                'total_token,multiply,contribution_0,contribution_1,'
                'note\n'
            )

            file.write(head)

        self.TOTAL_reward_0 = 0
        self.TOTAL_reward_1 = 0
        self.TOTAL_reservarion_0 = 0
        self.TOTAL_reservarion_1 = 0
        self.TOTAL_contribution_0 = 0
        self.TOTAL_contribution_1 = 0



    def overture(self):
        '''
        初始化 io。
        '''

        self.keyboard = keyboard.Keyboard()
        self.DUAL = dual_JS()

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



    def page_text(self, wait:int, auto:bool, text_0:str, text_1:str, 
                  pos:tuple=(0,0), align:str='left', boxsize:tuple=(1.5,1.5), 
                  color:str=config.color_set['black'], textsize:int=config.size_text['default']):
        '''
        向两个窗口呈现纯文字页面。
        '''
        
        text_0 = TextBox2(win=self.win0, text=text_0, lineBreaking='uax14',
                          pos=pos, size=boxsize, alignment=align, color=color, bold=True,
                          font='Source Han Serif SC', letterHeight=textsize, lineSpacing=1, 
                          units='norm', editable=False)
        text_1 = TextBox2(win=self.win1, text=text_1, lineBreaking='uax14',
                          pos=pos, size=boxsize, alignment=align, color=color, bold=True, 
                          font='Source Han Serif SC', letterHeight=textsize, lineSpacing=1, 
                          units='norm', editable=False)
        
        text_0.draw(), text_1.draw()
        self.win0.flip(), self.win1.flip()

        core.wait(wait)
        if auto:
            return
        else:
            self.__wait_kb()


    
    def page_pic(self, pic_0:str, pic_1:str, wait:float=1, auto:bool=False):
        '''
        向两个窗口呈现自适应分辨率的图片，保持原始比例。
        '''

        path_0 = 'image/' + pic_0
        path_1 = 'image/' + pic_1

        ratio_win = config.resolution[0] / config.resolution[1]

        with Image.open(path_0) as img_0:
            ratio_pic_0 = img_0.size[0] / img_0.size[1]
        if ratio_pic_0 >= ratio_win: #超宽图片
            pic_x_0 = config.windows_param[self.exp_param['mode']]['res']
            pic_y_0 = img_0.size[1]*pic_x_0/img_0.size[0]
        else: #超高图片
            pic_y_0 = config.windows_param[self.exp_param['mode']]['res']
            pic_x_0 = img_0.size[0]*pic_y_0/img_0.size[1]

        with Image.open(path_1) as img_1:
            ratio_pic_1 = img_1.size[0] / img_1.size[1]
        if ratio_pic_1 >= ratio_win: #超宽图片
            pic_x_1 = config.windows_param[self.exp_param['mode']]['res']
            pic_y_1 = img_1.size[1]*pic_x_1/img_1.size[0]
        else: #超高图片
            pic_y_1 = config.windows_param[self.exp_param['mode']]['res']
            pic_x_1 = img_1.size[0]*pic_y_1/img_1.size[1]

        content_win0 = visual.ImageStim(image=path_0, size=(pic_x_0, pic_y_0), units='pix', win=self.win0)
        content_win1 = visual.ImageStim(image=path_1, size=(pic_x_1, pic_y_1), units='pix', win=self.win1)

        content_win0.draw(win=self.win0), content_win1.draw(win=self.win1)
        self.win0.flip(), self.win1.flip()

        core.wait(wait)

        if auto:
            return
        else:
            self.__wait_kb()



    def STAGE_choice(self, topic_dict:dict, STAGE_index:int, condition_same:bool, duration:int=120):
        '''
        单个相似性操纵阶段。
        - topic_dict: 话题字典 {index : str_content}。
        - STAGE_index: 阶段编号（对应字典的键），1 ~ 3。
        - condition_same: True = 相似性操纵，False = 异质性操纵。
        - duration: 双方发表看法的时间（s）。
        '''

        order = [i for i in topic_dict[STAGE_index].keys()]
        rd.shuffle(order)

        choice_dict_0 = {}
        choice_dict_1 = {}

        def __trial_choice(STAGE_index:int, trial_index:int):
            '''
            呈现单个选择条目 trial，并由双方选择。
            - STAGE_index: 阶段编号（对应字典的键），1 ~ 3。
            - trial_index: 当前 trial 编号（整数键）。
            '''

            nonlocal choice_dict_0, choice_dict_1

            guide_0 = TextBox2(win=self.win0, text=config.static_text['choice_guide'],
                               size=config.size_shape['text_box'], lineBreaking='uax14',
                               pos=config.pos_element['choice_guide'], alignment='center', 
                               color=config.color_set['black'], bold=True, font='Source Han Serif SC', 
                               letterHeight=config.size_text['choice_guide'], lineSpacing=1, 
                               units='norm', editable=False)
            guide_1 = TextBox2(win=self.win1, text=config.static_text['choice_guide'],
                               size=config.size_shape['text_box'], lineBreaking='uax14',
                               pos=config.pos_element['choice_guide'], alignment='center', 
                               color=config.color_set['black'], bold=True, font='Source Han Serif SC', 
                               letterHeight=config.size_text['choice_guide'], lineSpacing=1, 
                               units='norm', editable=False)
            topic_0 = TextBox2(win=self.win0, text=config.topic_dict[STAGE_index][trial_index],
                               size=config.size_shape['text_box'], lineBreaking='uax14',
                               pos=config.pos_element['choice_topic'], alignment='center', 
                               color=config.color_set['black'], bold=True, font='Source Han Serif SC', 
                               letterHeight=config.size_text['choice_topic'], lineSpacing=1, 
                               units='norm', editable=False)
            topic_1 = TextBox2(win=self.win1, text=config.topic_dict[STAGE_index][trial_index],
                               size=config.size_shape['text_box'], lineBreaking='uax14',
                               pos=config.pos_element['choice_topic'], alignment='center', 
                               color=config.color_set['black'], bold=True, font='Source Han Serif SC', 
                               letterHeight=config.size_text['choice_topic'], lineSpacing=1, 
                               units='norm', editable=False)

            guide_0.draw(), guide_1.draw()
            topic_0.draw(), topic_1.draw()
            self.win0.flip(), self.win1.flip()

            choice_0, choice_1 = None, None
            finished_0, finished_1 = False, False

            _js0_before = [False]*len(self.DUAL.js0.getAllButtons())
            _js1_before = [False]*len(self.DUAL.js1.getAllButtons())

            while (not finished_0) or (not finished_1):
                core.wait(0.01)
                self.DUAL.win_flipper.flip()
                _pressed_0, _pressed_1 = self.DUAL.check_js(_js0_before=_js0_before, _js1_before=_js1_before)

                if (not finished_0) and _pressed_0:

                    if _pressed_0 == 'LB':
                        choice_0 = 'LB'
                        choice_confirm_0 = TextBox2(win=self.win0, text=config.static_text['choice_confirm']['LB'],
                                                    pos=config.pos_element['choice_confirm'], alignment='center', 
                                                    color=config.color_set['B'], bold=True, font='Source Han Serif SC',
                                                    letterHeight=config.size_text['choice_confirm'], lineSpacing=1,
                                                    lineBreaking='uax14', units='norm', editable=False)
                        guide_0.draw(), topic_0.draw(), choice_confirm_0.draw()
                        self.win0.flip()

                    elif _pressed_0 == 'RB':
                        choice_0 = 'RB'
                        choice_confirm_0 = TextBox2(win=self.win0, text=config.static_text['choice_confirm']['RB'],
                                                    pos=config.pos_element['choice_confirm'], alignment='center', 
                                                    color=config.color_set['B'], bold=True, font='Source Han Serif SC',
                                                    letterHeight=config.size_text['choice_confirm'], lineSpacing=1,
                                                    lineBreaking='uax14', units='norm', editable=False)
                        guide_0.draw(), topic_0.draw(), choice_confirm_0.draw()
                        self.win0.flip()

                    elif choice_0 and _pressed_0 == 'A':
                        finished_0 = True
                        choice_dict_0[trial_index] = choice_0
                        self.__render_wait(win=self.win0, text=config.static_text['wait_allay_choice'])
                        self.win0.flip()

                if (not finished_1) and _pressed_1:

                    if _pressed_1 == 'LB':
                        choice_1 = 'LB'
                        choice_confirm_1 = TextBox2(win=self.win1, text=config.static_text['choice_confirm']['LB'],
                                                    pos=config.pos_element['choice_confirm'], alignment='center', 
                                                    color=config.color_set['B'], bold=True, font='Source Han Serif SC',
                                                    letterHeight=config.size_text['choice_confirm'], lineSpacing=1,
                                                    lineBreaking='uax14', units='norm', editable=False)
                        guide_1.draw(), topic_1.draw(), choice_confirm_1.draw()
                        self.win1.flip()

                    elif _pressed_1 == 'RB':
                        choice_1 = 'RB'
                        choice_confirm_1 = TextBox2(win=self.win1, text=config.static_text['choice_confirm']['RB'],
                                                    pos=config.pos_element['choice_confirm'], alignment='center', 
                                                    color=config.color_set['B'], bold=True, font='Source Han Serif SC',
                                                    letterHeight=config.size_text['choice_confirm'], lineSpacing=1,
                                                    lineBreaking='uax14', units='norm', editable=False)
                        guide_1.draw(), topic_1.draw(), choice_confirm_1.draw()
                        self.win1.flip()

                    elif choice_1 and _pressed_1 == 'A':
                        finished_1 = True
                        choice_dict_1[trial_index] = choice_1
                        self.__render_wait(win=self.win1, text=config.static_text['wait_allay_choice'])
                        self.win1.flip()

        def __discuss_choice(condition_same:bool, duration:int):
            '''
            呈现当前阶段讨论阶段的条目。
            - condition_same: True == 相似性操纵，Fasle == 异质性操纵。
            - duration: 双方发表看法的时间（s）。
            '''

            nonlocal choice_dict_0, choice_dict_1

            item_key_same = []
            item_key_diff = []
            coincidence = False

            for i in choice_dict_0.keys():
                if choice_dict_0[i] == choice_dict_1[i]:
                    item_key_same.append(i)
                else:
                    item_key_diff.append(i)

            if condition_same and item_key_same:
                discuss_topic_index = rd.choice(item_key_same)
                if choice_dict_0[discuss_topic_index] == 'LB':
                    discuss_choice_0 = config.static_text['discuss_choice']['same_LB']
                    discuss_choice_1 = config.static_text['discuss_choice']['same_LB']
                elif choice_dict_0[discuss_topic_index] == 'RB':
                    discuss_choice_0 = config.static_text['discuss_choice']['same_RB']
                    discuss_choice_1 = config.static_text['discuss_choice']['same_RB']
            elif (not condition_same) and item_key_diff:
                discuss_topic_index = rd.choice(item_key_diff)
                if choice_dict_0[discuss_topic_index] == 'LB':
                    discuss_choice_0 = config.static_text['discuss_choice']['diff_LB']
                    discuss_choice_1 = config.static_text['discuss_choice']['diff_RB']
                elif choice_dict_0[discuss_topic_index] == 'RB':
                    discuss_choice_0 = config.static_text['discuss_choice']['diff_RB']
                    discuss_choice_1 = config.static_text['discuss_choice']['diff_LB']
            else:
                coincidence = True

            if (not coincidence):

                topic_0 = TextBox2(win=self.win0, text=config.topic_dict[STAGE_index][discuss_topic_index],
                                size=config.size_shape['text_box'],
                                pos=config.pos_element['discuss_topic'], alignment='center', 
                                color=config.color_set['black'], bold=True, font='Source Han Serif SC', 
                                letterHeight=config.size_text['discuss_topic'], lineSpacing=1, 
                                lineBreaking='uax14', units='norm', editable=False)
                topic_1 = TextBox2(win=self.win1, text=config.topic_dict[STAGE_index][discuss_topic_index],
                                size=config.size_shape['text_box'],
                                pos=config.pos_element['discuss_topic'], alignment='center', 
                                color=config.color_set['black'], bold=True, font='Source Han Serif SC', 
                                letterHeight=config.size_text['discuss_topic'], lineSpacing=1, 
                                lineBreaking='uax14', units='norm', editable=False)
                choice_0 = TextBox2(win=self.win0, text=discuss_choice_0,
                                    size=config.size_shape['text_box'],
                                    pos=config.pos_element['discuss_choice'], alignment='center', 
                                    color=config.color_set['B'], bold=True, font='Source Han Serif SC', 
                                    letterHeight=config.size_text['default'], lineSpacing=1, 
                                    units='norm', editable=False)
                choice_1 = TextBox2(win=self.win1, text=discuss_choice_1,
                                    size=config.size_shape['text_box'],
                                    pos=config.pos_element['discuss_choice'], alignment='center', 
                                    color=config.color_set['B'], bold=True, font='Source Han Serif SC', 
                                    letterHeight=config.size_text['default'], lineSpacing=1, 
                                    units='norm', editable=False)
                
                topic_0.draw(), topic_1.draw()
                choice_0.draw(), choice_1.draw()
                self.win0.flip(), self.win1.flip()

                core.wait(duration)

                self.page_text(wait=3, auto=False, 
                        text_0=config.static_text['discussion_end'], 
                        text_1=config.static_text['discussion_end'],
                        align='left')

        for i in order:

            __trial_choice(STAGE_index=STAGE_index, trial_index=i)

        self.page_text(wait=2, auto=True, 
                text_0=config.static_text['intermezzo'], 
                text_1=config.static_text['intermezzo'],
                align='left')
        
        self.page_text(wait=5, auto=False,
                       text_0=config.static_text['choice_result']['same'] if condition_same \
                        else config.static_text['choice_result']['diff'],
                       text_1=config.static_text['choice_result']['same'] if condition_same \
                        else config.static_text['choice_result']['diff'])
        
        __discuss_choice(condition_same=condition_same, duration=duration)



    def STAGE_PGG(self, STAGE_index:int, STAGE_trials:int, 
                  total_token:int, multiply:int,
                  show_trial_result:bool=True, 
                  show_STAGE_reward:bool=True):
        '''
        包含若干个 trials 的 PGG。
        - STAGE_index: 阶段编号，约定 0 = 练习阶段。
        - STAGE_trials: 当前阶段总试次数。
        - total_token: 代币总数。
        - multiply: 公共代币池倍率。
        - show_trial_result: 是否在当前 trial 结束时显示双方的分配情况。
        - show_STAGE_reward: 是否显示当前 STAGE 双方的实时收益。
        '''

        self.STAGE_reward_0 = 0
        self.STAGE_reward_1 = 0
        self.STAGE_reservarion_0 = 0
        self.STAGE_reservarion_1 = 0
        self.STAGE_contribution_0 = 0
        self.STAGE_contribution_1 = 0
        
        def __trial_PGG(role:int, trial_index:int, 
                        STAGE_index:int=STAGE_index, STAGE_trials:int=STAGE_trials, 
                        process_name='trial_PGG', 
                        show_trial_result:bool=True, show_STAGE_reward:bool=True):
            '''
            单个 PGG trial。
            '''

            nonlocal pgg
            nonlocal finished_0, finished_1
            finished = False

            _js0_before = [False] * len(self.DUAL.js0.getAllButtons())
            _js1_before = [False] * len(self.DUAL.js1.getAllButtons())

            if show_STAGE_reward:
                self.__render_reawrd(pgg=pgg, win=self.win0)
                self.__render_reawrd(pgg=pgg, win=self.win1)
            if role == 0:
                self.__render_wait(win=self.win1, text=config.static_text['wait_allay_PGG'])
                self.__render_pgg(pgg=pgg, render_win0=True, render_win1=False, 
                                  STAGE_trials=STAGE_trials, trial_index=trial_index)
                self.win0.flip(), self.win1.flip()
            elif role == 1:
                self.__render_wait(win=self.win0, text=config.static_text['wait_allay_PGG'])
                self.__render_pgg(pgg=pgg, render_win0=False, render_win1=True, 
                                  STAGE_trials=STAGE_trials, trial_index=trial_index)
                self.win0.flip(), self.win1.flip()

            while not finished:

                core.wait(0.01)
                self.DUAL.win_flipper.flip()
                _pressed_0, _pressed_1 = self.DUAL.check_js(_js0_before=_js0_before, _js1_before=_js1_before)

                if role == 0 and _pressed_0:

                    if _pressed_0 == 'LB' and pgg.trial_reservation_0 > 0: #增加贡献，减少保留
                        pgg.contribution_0 += 1
                        self.__render_pgg(pgg=pgg, render_win0=True, render_win1=False, 
                                          STAGE_trials=STAGE_trials, trial_index=trial_index)
                        if show_STAGE_reward:
                            self.__render_reawrd(pgg=pgg, win=self.win0)
                            self.win0.flip()

                    elif _pressed_0 == 'RB' and pgg.contribution_0 > 0: #减少贡献，增加保留
                        pgg.contribution_0 -= 1
                        self.__render_pgg(pgg=pgg, render_win0=True, render_win1=False, 
                                          STAGE_trials=STAGE_trials, trial_index=trial_index)
                        if show_STAGE_reward:
                            self.__render_reawrd(pgg=pgg, win=self.win0)
                            self.win0.flip()

                    elif _pressed_0 == 'Y_A':
                        finished = True
                        finished_0 = True
                        if not finished_1:
                            self.__render_wait(win=self.win0, text=config.static_text['wait_allay_PGG'])

                elif role == 1 and _pressed_1:

                    if _pressed_1 == 'LB' and pgg.trial_reservation_1 > 0: #增加贡献，减少保留
                        pgg.contribution_1 += 1
                        self.__render_pgg(pgg=pgg, render_win0=False, render_win1=True, 
                                          STAGE_trials=STAGE_trials, trial_index=trial_index)
                        if show_STAGE_reward:
                            self.__render_reawrd(pgg=pgg, win=self.win1)
                            self.win1.flip()

                    elif _pressed_1 == 'RB' and pgg.contribution_1 > 0: #减少贡献，增加保留
                        pgg.contribution_1 -= 1
                        self.__render_pgg(pgg=pgg, render_win0=False, render_win1=True, 
                                          STAGE_trials=STAGE_trials, trial_index=trial_index)
                        if show_STAGE_reward:
                            self.__render_reawrd(pgg=pgg, win=self.win1)
                            self.win1.flip()

                    elif _pressed_1 == 'Y_A':
                        finished = True
                        finished_1 = True
                        if not finished_0:
                            self.__render_wait(win=self.win1, text=config.static_text['wait_allay_PGG'])

            if finished_0 and finished_1: #完成一个 trial

                self.STAGE_reward_0 += pgg.trial_reward_0
                self.STAGE_reward_1 += pgg.trial_reward_1
                self.STAGE_reservarion_0 += pgg.trial_reservation_0
                self.STAGE_reservarion_1 += pgg.trial_reservation_1
                self.STAGE_contribution_0 += pgg.contribution_0
                self.STAGE_contribution_1 += pgg.contribution_1
                self.save_trial(process_name=process_name, STAGE_index=STAGE_index, trial_index=trial_index, 
                                duration=format(self.clock_local.getTime(),'.3f'), pgg=pgg)

                if show_trial_result:

                    if show_STAGE_reward:
                        self.__render_reawrd(pgg=pgg, win=self.win0)
                        self.__render_reawrd(pgg=pgg, win=self.win1)
                        # .page_text() 内置了 .flip()

                    dynamic_param = self.__dynamic_param(pgg=pgg)
                    self.page_text(wait=5, auto=True, 
                                   text_0=dynamic_param['trial_result_0'], 
                                   text_1=dynamic_param['trial_result_1'], )
                
            return
        
        for i in range(STAGE_trials):

            order = [0,1]
            rd.shuffle(order)

            pgg = PGG(total_token=total_token, multiply=multiply,
                      init_contribution_0=rd.randint(0,total_token), 
                      init_contribution_1=rd.randint(0,total_token))
            
            finished_0, finished_1 = False, False
            self.clock_local.reset()

            __trial_PGG(role=order[0], trial_index=i, STAGE_index=STAGE_index, 
                        process_name='trial_PGG', 
                        show_trial_result=show_trial_result, show_STAGE_reward=show_STAGE_reward)
            __trial_PGG(role=order[1], trial_index=i, STAGE_index=STAGE_index, 
                        process_name='trial_PGG', 
                        show_trial_result=show_trial_result, show_STAGE_reward=show_STAGE_reward)

        self.page_text(wait=3, auto=False, 
                       text_0=config.static_text['call_me'], 
                       text_1=config.static_text['call_me'],
                       align='left')
        
        self.TOTAL_reward_0 += self.STAGE_reward_0
        self.TOTAL_reward_1 += self.STAGE_reward_1
        self.TOTAL_reservarion_0 += self.STAGE_reward_0
        self.TOTAL_reservarion_1 += self.STAGE_reward_1
        self.TOTAL_contribution_0 += self.STAGE_contribution_0
        self.TOTAL_contribution_1 += self.STAGE_contribution_1



    def __dynamic_param(self, pgg:PGG):
        '''
        根据 pgg 实例计算实验动态参数，包括文字、位置、颜色、尺寸等。
        - pgg: 当前 PGG trial。
        '''

        explain_public_box = f' 每投入 1 枚，双方各获得\n￥{format(pgg.multiply,".2f")}'
        explain_private_box = f' 每投入 1 枚，双方各获得\n￥1.00'

        trial_result_0 = (
            f'您往公共帐户中投入了 {pgg.contribution_0} 枚代币\n对方往公共账户投入了 {pgg.contribution_1} 枚代币\n\n'
            f'本轮您的收益：￥{format(pgg.trial_reward_0,".2f")}\n本轮对方收益：￥{format(pgg.trial_reward_1,".2f")}'
            )
        trial_result_1 = (
            f'您往公共帐户中投入了 {pgg.contribution_1} 枚代币\n对方往公共账户投入了 {pgg.contribution_0} 枚代币\n\n'
            f'本轮您的收益：￥{format(pgg.trial_reward_1,".2f")}\n本轮对方收益：￥{format(pgg.trial_reward_0,".2f")}'
            )

        STAGE_reward_self_0 = f' 您的累计收益\n￥{format(self.STAGE_reward_0,".2f")}'
        STAGE_reward_self_1 = f' 您的累计收益\n￥{format(self.STAGE_reward_1,".2f")}'
        STAGE_reward_allay_0 = f' 对方累计收益\n￥{format(self.STAGE_reward_1,".2f")}'
        STAGE_reward_allay_1 = f' 对方累计收益\n￥{format(self.STAGE_reward_0,".2f")}'

        pos_token = [(i, -0.20) for i in np.linspace(start=-0.35, stop=0.35, num=pgg.total_token)]

        size_token = (config.size_shape['token'], 
                      config.size_shape['token'] * config.windows_param[self.exp_param['mode']]['res'][0] / config.windows_param[self.exp_param['mode']]['res'][1])

        fillcolor_token_0 = [config.color_set['r']] * pgg.contribution_0 + [config.color_set['g']] * pgg.trial_reservation_0
        fillcolor_token_1 = [config.color_set['r']] * pgg.contribution_1 + [config.color_set['g']] * pgg.trial_reservation_1
        linecolor_token_0 = [config.color_set['R']] * pgg.contribution_0 + [config.color_set['G']] * pgg.trial_reservation_0
        linecolor_token_1 = [config.color_set['R']] * pgg.contribution_1 + [config.color_set['G']] * pgg.trial_reservation_1

        return {
            'explain_public_box':explain_public_box, 'explain_private_box':explain_private_box, 
            'trial_result_0':trial_result_0, 'trial_result_1':trial_result_1, 
            'STAGE_reward_self_0':STAGE_reward_self_0, 'STAGE_reward_allay_0':STAGE_reward_allay_0, 
            'STAGE_reward_self_1':STAGE_reward_self_1, 'STAGE_reward_allay_1':STAGE_reward_allay_1, 
            'pos_token':pos_token, 'size_token':size_token, 
            'fill_0':fillcolor_token_0, 'fill_1':fillcolor_token_1, 
            'line_0':linecolor_token_0, 'line_1':linecolor_token_1,
            }



    def __render_pgg(self, pgg:PGG, render_win0:bool, render_win1:bool, 
                     STAGE_trials:int, trial_index:int):
        '''
        实时渲染 PGG 图形界面。
        - pgg: 当前 PGG trial。
        - render_win_0/1: 是否更新窗口后端渲染的内容。
        - show_STAGE_reward: 是否显示当前 STAGE 双方的实时收益。
        - STAGE_trials: 当前 STAGE trials 的数量。
        - trial_index: 当前 trial 的序数。
        '''

        dynamic_param = self.__dynamic_param(pgg=pgg)

        # 当前轮次
        trial_index_0 = TextBox2(win=self.win0, text=f'第 {trial_index+1} / {STAGE_trials} 轮',
                                 pos=config.pos_element['trial_index'], 
                                 alignment='center', color=config.color_set['B'], bold=True,
                                 font='Source Han Serif SC', letterHeight=config.size_text['trial_index'], lineSpacing=1, 
                                 units='norm', editable=False)
        trial_index_1 = TextBox2(win=self.win1, text=f'第 {trial_index+1} / {STAGE_trials} 轮',
                                 pos=config.pos_element['trial_index'], 
                                 alignment='center', color=config.color_set['B'], bold=True,
                                 font='Source Han Serif SC', letterHeight=config.size_text['trial_index'], lineSpacing=1, 
                                 units='norm', editable=False)
        
        # 公共池和私有池框架
        public_box_0 = rect.Rect(win=self.win0, units='norm', 
                                 width=config.size_shape['public_box'][0], 
                                 height=config.size_shape['public_box'][1], 
                                 pos=config.pos_element['public_box'], 
                                 lineColor=config.color_set['R'], fillColor=config.color_set['r'])
        public_box_1 = rect.Rect(win=self.win1, units='norm', 
                                 width=config.size_shape['public_box'][0], 
                                 height=config.size_shape['public_box'][1], 
                                 pos=config.pos_element['public_box'], 
                                 lineColor=config.color_set['R'], fillColor=config.color_set['r'])
        private_box_0 = rect.Rect(win=self.win0, units='norm', 
                                 width=config.size_shape['private_box'][0], 
                                 height=config.size_shape['private_box'][1], 
                                 pos=config.pos_element['private_box'], 
                                 lineColor=config.color_set['G'], fillColor=config.color_set['g'])
        private_box_1 = rect.Rect(win=self.win1, units='norm', 
                                 width=config.size_shape['private_box'][0], 
                                 height=config.size_shape['private_box'][1], 
                                 pos=config.pos_element['private_box'], 
                                 lineColor=config.color_set['G'], fillColor=config.color_set['g'])

        # 公共池和私有池投入代币
        public_box_token_0 = TextBox2(win=self.win0, text=f'{pgg.contribution_0} 枚',
                                      pos=config.pos_element['public_box_token'], 
                                      size=config.size_shape['public_box'], 
                                      alignment='center', color=config.color_set['R'], bold=True,
                                      font='Source Han Serif SC', letterHeight=config.size_text['box_token'], lineSpacing=1, 
                                      units='norm', editable=False)
        public_box_token_1 = TextBox2(win=self.win1, text=f'{pgg.contribution_1} 枚',
                                      pos=config.pos_element['public_box_token'], 
                                      size=config.size_shape['public_box'], 
                                      alignment='center', color=config.color_set['R'], bold=True,
                                      font='Source Han Serif SC', letterHeight=config.size_text['box_token'], lineSpacing=1, 
                                      units='norm', editable=False)
        private_box_token_0 = TextBox2(win=self.win0, text=f'{pgg.trial_reservation_0} 枚',
                                      pos=config.pos_element['private_box_token'], 
                                      size=config.size_shape['private_box'], 
                                      alignment='center', color=config.color_set['G'], bold=True,
                                      font='Source Han Serif SC', letterHeight=config.size_text['box_token'], lineSpacing=1, 
                                      units='norm', editable=False)
        private_box_token_1 = TextBox2(win=self.win1, text=f'{pgg.trial_reservation_1} 枚',
                                      pos=config.pos_element['private_box_token'], 
                                      size=config.size_shape['private_box'], 
                                      alignment='center', color=config.color_set['G'], bold=True,
                                      font='Source Han Serif SC', letterHeight=config.size_text['box_token'], lineSpacing=1, 
                                      units='norm', editable=False)
        
        # 公共池和私有池说明及标签
        explain_public_box_0 = TextBox2(win=self.win0, text=dynamic_param['explain_public_box'],
                                        pos=config.pos_element['explain_public_box'], 
                                        size=config.size_shape['public_box'], 
                                        alignment='center', color=config.color_set['R'], bold=True,
                                        font='Source Han Serif SC', letterHeight=config.size_text['default'], lineSpacing=1, 
                                        units='norm', editable=False)
        explain_public_box_1 = TextBox2(win=self.win1, text=dynamic_param['explain_public_box'],
                                        pos=config.pos_element['explain_public_box'], 
                                        size=config.size_shape['public_box'], 
                                        alignment='center', color=config.color_set['R'], bold=True,
                                        font='Source Han Serif SC', letterHeight=config.size_text['default'], lineSpacing=1, 
                                        units='norm', editable=False)
        explain_private_box_0 = TextBox2(win=self.win0, text=dynamic_param['explain_private_box'],
                                        pos=config.pos_element['explain_private_box'], 
                                        size=config.size_shape['private_box'], 
                                        alignment='center', color=config.color_set['G'], bold=True,
                                        font='Source Han Serif SC', letterHeight=config.size_text['default'], lineSpacing=1, 
                                        units='norm', editable=False)
        explain_private_box_1 = TextBox2(win=self.win1, text=dynamic_param['explain_private_box'],
                                        pos=config.pos_element['explain_private_box'], 
                                        size=config.size_shape['private_box'], 
                                        alignment='center', color=config.color_set['G'], bold=True,
                                        font='Source Han Serif SC', letterHeight=config.size_text['default'], lineSpacing=1, 
                                        units='norm', editable=False)
        add_public_box_0 = TextBox2(win=self.win0, text=config.static_text['add_public_box'],
                                      pos=config.pos_element['add_public_box'], 
                                      size=config.size_shape['public_box'], 
                                      alignment='center', color=config.color_set['R'], bold=True,
                                      font='Source Han Serif SC', letterHeight=config.size_text['default'], lineSpacing=1, 
                                      units='norm', editable=False)
        add_public_box_1 = TextBox2(win=self.win1, text=config.static_text['add_public_box'],
                                      pos=config.pos_element['add_public_box'], 
                                      size=config.size_shape['public_box'], 
                                      alignment='center', color=config.color_set['R'], bold=True,
                                      font='Source Han Serif SC', letterHeight=config.size_text['default'], lineSpacing=1, 
                                      units='norm', editable=False)
        add_private_box_0 = TextBox2(win=self.win0, text=config.static_text['add_private_box'],
                                       pos=config.pos_element['add_private_box'], 
                                       alignment='center', color=config.color_set['G'], bold=True,
                                       font='Source Han Serif SC', letterHeight=config.size_text['default'], lineSpacing=1, 
                                       units='norm', editable=False)
        add_private_box_1 = TextBox2(win=self.win1, text=config.static_text['add_private_box'],
                                       pos=config.pos_element['add_private_box'], 
                                       alignment='center', color=config.color_set['G'], bold=True,
                                       font='Source Han Serif SC', letterHeight=config.size_text['default'], lineSpacing=1, 
                                       units='norm', editable=False)
        
        # 确认分配提示
        confrim_token_0 = TextBox2(win=self.win0, text=config.static_text['confirm_token'],
                                   pos=config.pos_element['confirm_token'], 
                                   alignment='center', color=config.color_set['black'], bold=True,
                                   font='Source Han Serif SC', letterHeight=config.size_text['default'], lineSpacing=1,
                                   units='norm', editable=False)
        confrim_token_1 = TextBox2(win=self.win1, text=config.static_text['confirm_token'],
                                   pos=config.pos_element['confirm_token'], 
                                   alignment='center', color=config.color_set['black'], bold=True,
                                   font='Source Han Serif SC', letterHeight=config.size_text['default'], lineSpacing=1,
                                   units='norm', editable=False)
 
        # 代币图样
        token_list_0, token_list_1 = [], []
        token_symbol_list_0, token_symbol_list_1 = [], []

        for i in range(pgg.total_token):
            token_list_0.append(circle.Circle(win=self.win0, units='norm', 
                                              radius=dynamic_param['size_token'], 
                                              pos=dynamic_param['pos_token'][i], 
                                              lineColor=dynamic_param['line_0'][i], 
                                              fillColor=dynamic_param['fill_0'][i],))
            token_list_1.append(circle.Circle(win=self.win1, units='norm', 
                                              radius=dynamic_param['size_token'], 
                                              pos=dynamic_param['pos_token'][i], 
                                              lineColor=dynamic_param['line_1'][i], 
                                              fillColor=dynamic_param['fill_1'][i],))

        # 渲染
        if render_win0:
            # trial_index_0.draw()
            public_box_0.draw()
            private_box_0.draw()
            public_box_token_0.draw()
            private_box_token_0.draw()
            explain_public_box_0.draw()
            explain_private_box_0.draw()
            add_public_box_0.draw()
            add_private_box_0.draw()
            confrim_token_0.draw()
            for _ in token_list_0:
                _.draw()
            for _ in token_symbol_list_0:
                _.draw()

        if render_win1:
            # trial_index_1.draw()
            public_box_1.draw()
            private_box_1.draw()
            public_box_token_1.draw()
            private_box_token_1.draw()
            explain_public_box_1.draw()
            explain_private_box_1.draw()
            add_public_box_1.draw()
            add_private_box_1.draw()
            confrim_token_1.draw()
            for _ in token_list_1:
                _.draw()
            for _ in token_symbol_list_1:
                _.draw()



    def __render_reawrd(self, win:visual.Window, pgg:PGG):
        '''
        实时渲染双方当前 STAGE 累计收益。
        '''

        dynamic_param = self.__dynamic_param(pgg=pgg)

        # 当前 STAGE 双方累计收益
        current_reward_self_0 = TextBox2(win=self.win0, text=dynamic_param['STAGE_reward_self_0'], 
                                         pos=config.pos_element['STAGE_reward_self'], 
                                         alignment='center', color=config.color_set['B'], bold=True, 
                                         font='Source Han Serif SC', letterHeight=config.size_text['default'], lineSpacing=1,
                                         units='norm', editable=False)
        current_reward_self_1 = TextBox2(win=self.win1, text=dynamic_param['STAGE_reward_self_1'], 
                                         pos=config.pos_element['STAGE_reward_self'], 
                                         alignment='center', color=config.color_set['B'], bold=True, 
                                         font='Source Han Serif SC', letterHeight=config.size_text['default'], lineSpacing=1,
                                         units='norm', editable=False)
        current_reward_allay_0 = TextBox2(win=self.win0, text=dynamic_param['STAGE_reward_allay_0'], 
                                          pos=config.pos_element['STAGE_reward_allay'],
                                          alignment='center', color=config.color_set['B'], bold=True, 
                                          font='Source Han Serif SC', letterHeight=config.size_text['default'], lineSpacing=1,
                                          units='norm', editable=False)
        current_reward_allay_1 = TextBox2(win=self.win1, text=dynamic_param['STAGE_reward_allay_1'], 
                                          pos=config.pos_element['STAGE_reward_allay'],
                                          alignment='center', color=config.color_set['B'], bold=True, 
                                          font='Source Han Serif SC', letterHeight=config.size_text['default'], lineSpacing=1,
                                          units='norm', editable=False)
        
        if win == self.win0:
            current_reward_self_0.draw()
            current_reward_allay_0.draw()
        elif win == self.win1:
            current_reward_self_1.draw()
            current_reward_allay_1.draw()



    def __wait_kb(self, key:tuple=config.allowed_keys):

        self.keyboard.clearEvents()
        while True:
            pressed = self.keyboard.getKeys()
            if pressed:
                if pressed[-1].name in key:
                    break
            else:
                core.wait(0.01)
                
        return pressed[-1]
    


    def __render_wait(self, win:visual.Window, text:str):

        content = visual.TextBox2(win=win, text=text,
                                  pos=(0,0), size=(1.5,0.5), alignment='left', color=config.color_set['black'], bold=True,
                                  font='Source Han Serif SC', letterHeight=config.size_text['default'], lineSpacing=1, 
                                  lineBreaking='uax14', units='norm', editable=False)
        content.draw()



    @property
    def calculate_income(self):
        '''
        计算被试费。
        - 保底收益为 ￥1/min。
        - 最终代币更多的一方，按照双方收入的比例获得相等倍率的被试费，但不超过 1.2 倍。
        '''

        basic_income = self.clock_global.getTime() // 60 #每分钟￥1作为基准被试费

        income_ratio = max(self.TOTAL_reward_0, self.TOTAL_reward_1) / min(self.TOTAL_reward_0, self.TOTAL_reward_1)
        adjusted_ratio = income_ratio if income_ratio <= 1.2 else 1.2 #高分一方被试费倍率上限

        income_0 = basic_income * adjusted_ratio if self.TOTAL_reward_0 > self.TOTAL_reward_1 else basic_income
        income_1 = basic_income * adjusted_ratio if self.TOTAL_reward_1 > self.TOTAL_reward_0 else basic_income

        return [income_0, income_1]



    def finale(self):
        '''
        计算最终收益，结束实验。
        '''

        income = self.calculate_income
        self.page_text(wait=2, auto=False,
                       text_0=(
                           '收益情况\n\n'
                           f'您的收益（折算）：￥{int(income[0])}\n对方收益（折算）：￥{int(income[1])}'
                           ),
                       text_1=(
                           '收益情况\n\n'
                           f'您的收益（折算）：￥{int(income[1])}\n对方收益（折算）：￥{int(income[0])}'
                           ))
        self.page_text(wait=5, auto=True, 
                       text_0=config.static_text['exp_end'],
                       text_1=config.static_text['exp_end'])
        core.quit()



    def save_trial(self, process_name:str, STAGE_index:int, trial_index:int, duration:float, pgg:PGG=None):
        '''
        写入当前试次的数据。
        - pgg: 如果记录 PGG 则为当前 PGG class instance。
        '''
        with open(file=self.path_data_trial, mode='a', encoding='utf-8') as file:

            body = (
                f"{self.exp_param['exp_num']},{self.exp_param['mode']},"
                f"{self.exp_param['condition_A']},{self.exp_param['condition_B']},{self.exp_param['condition_C']},"
                f"{dt.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')},{self.clock_global.getTime()},"
                f"{process_name},{STAGE_index},{trial_index},{duration},"
                f"{pgg.total_token},{pgg.multiply},{pgg.contribution_0},{pgg.contribution_1},"
                f"{self.exp_param['note']}"
                '\n'
            )

            file.write(body)



if __name__ == '__main__':

    debug = Event()
    debug.overture()
    debug.STAGE_PGG(STAGE_index=1, STAGE_trials=10, total_token=10, multiply=0.75)
    debug.STAGE_choice(topic_dict=config.topic_dict, STAGE_index=1, condition_same=False, duration=5)
    debug.STAGE_choice(topic_dict=config.topic_dict, STAGE_index=2, condition_same=True, duration=5)
    debug.STAGE_choice(topic_dict=config.topic_dict, STAGE_index=3, condition_same=False, duration=5)
    debug.STAGE_PGG(STAGE_index=2, STAGE_trials=10, total_token=10, multiply=0.75)
    debug.finale()
