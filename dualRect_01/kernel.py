
# 标准库
import os
import datetime as dt
import random as rd

# 自建库
import parser
from jshub import dualJS
from render import dualWin
from config import config
from memos import Scale, Perf

# Psychopy 库
from psychopy import gui, core
from psychopy.hardware import keyboard

class Event:
    '''
    所有实验事件。
    '''

    def __init__(self):

        self.script_dir = os.path.dirname(os.path.abspath(__file__))

        self.scale = Scale()
        self.perf = Perf()



    def overture(self):
        '''
        创建日志、数据文件，录入被试信息。
        '''

        # 日志文件
        with open(file=os.path.join(self.script_dir, 'log.txt'), 
                  mode='r', encoding='utf-8') as log:
            exp_existed = 0
            for _ in log:
                exp_existed += 1

        # 被试信息
        self._exp_param = {'exp_num':exp_existed + 1,
                           'condition_A':[1,2,3], 'condition_B':[1,2,3], 'condition_C':[1,2,3],
                           'disp_mode':['1440p_win','1440p_flscr','2160p_win','2160p_flscr',],
                           'debug_mode':['debug','formal_exp',],
                           'note':'None'}
        exp_info = gui.DlgFromDict(dictionary=self._exp_param)

        if exp_info.OK:
            with open(file=os.path.join(self.script_dir, 'log.txt'), 
                      mode='a', encoding='utf-8') as log:
                log_str = (
                    f"exp_num:{self._exp_param['exp_num']},"
                    f"disp_mode:{self._exp_param['disp_mode']},"
                    f"debug_mode:{self._exp_param['debug_mode']},"
                    f"condition_A:{self._exp_param['condition_A']},"
                    f"condition_B:{self._exp_param['condition_B']},"
                    f"condition_C:{self._exp_param['condition_C']},"
                    f"time:{dt.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')},"
                    f"note:{self._exp_param['note']},\n"
                    )
                log.write(log_str)
        else:
            gui.warnDlg(prompt='manually quit.')
            core.quit()

        self.exp_num = int(self._exp_param['exp_num'])
        self.condition_A = int(self._exp_param['condition_A'])
        self.condition_B = int(self._exp_param['condition_B'])
        self.condition_C = int(self._exp_param['condition_C'])

        # 调试模式处理
        self._debug = self._exp_param['debug_mode'] == 'debug'
        if self._debug:
            self._mod_trial = 2
            self._mod_intro = 0.25
            self._mod_rest = 5
            self.json_filename = os.path.join(self.script_dir, 'stim_debug.json')
        else:
            self.json_filename = os.path.join(self.script_dir, 'stim_array.json')

        expData_filename = f"expData.csv"
        trialData_filename = f"exp_{self._exp_param['exp_num']}.csv"
        self.expData_path = os.path.join(self.script_dir, 'dataExp', expData_filename)
        self.trialData_path = os.path.join(self.script_dir, 'dataTrial', trialData_filename)
        with open(file=self.trialData_path, mode='a', encoding='utf-8') as file:
            head = (
                'exp_num,disp_mode,debug_mode,condition_A,condition_B,condition_C,'
                'sys_time,exp_time,'
                'block_index,trail_index,stim_index,'
                'task_mode,report_mode,stage,harder,' 
                'actual_stim,subject,choice,scale,dutaion,'
                'note,'
                '\n'
                )
            file.write(head)



    def prelude(self):
        '''
        初始化 i/o 设备，定义 json 文件路径。
        '''

        self.json_path = os.path.join(self.script_dir, self.json_filename)

        self.dualJS = dualJS()
        self.dualWin = dualWin(
            bg_color=config.color_set['bg_gray'], 
            size_win=config.windows_param[self._exp_param['disp_mode']]['res'], 
            pos_win0=config.windows_param[self._exp_param['disp_mode']]['pos'][0], 
            pos_win1=config.windows_param[self._exp_param['disp_mode']]['pos'][1], 
            fullscreen=config.windows_param[self._exp_param['disp_mode']]['fullscreen'], 
            allow_gui=False
            )
        self.keyboard = keyboard.Keyboard()
        self.clock_global = core.Clock()
        self.clock_local = core.Clock()


    
    def tempVars(self):
        '''
        创建临时变量。
        '''

        if getattr(self, 'init_tempVars', False):
            return
        
        self.host_subject = 0
        self.wait_subject = 1

        self._init_tempVars = True



    def wait_kb(self, listen_keys:tuple[str]) -> str:
        '''
        持续监听等待按键输入。
        返回最后一个按键名称。
        - listen_keys: 合法的按键名称元组。
        '''

        self.keyboard.clearEvents()

        while True:
            core.wait(config.time['io_interval'])
            pressed = self.keyboard.getKeys()
            if pressed:
                if pressed[-1].name in listen_keys:
                    break
                else:
                    self.keyboard.clearEvents()
            else:
                continue

        return pressed[-1].name



    def page_text(
            self,
            auto:bool, timeout:int|float,
            text_0:str, text_1:str,
            pos:tuple=(0,0), align:str='left', boxsize:tuple=(1.5,1.5),
            color:str=config.color_set['black'], textsize:int=config.size['text']
            ):
        '''
        向单方或双方呈现一个纯文字页面。
        - auto: 是否自动跳转。
        - timeout: 当前页面停留下限时间 / 自动跳转时间。
        - text_0/1: 若为 None 则不对该被试窗口调用 .flip()。
        '''

        self.dualWin.text(
            text_0=text_0, text_1=text_1, 
            pos=pos, align=align, boxsize=boxsize,
            color=color, textsize=textsize
            )
        if auto:
            core.wait(timeout if not self._debug else self._mod_intro)
            return
        else:
            core.wait(timeout if not self._debug else self._mod_intro)
            self.wait_kb(listen_keys=config.allowed_key['skip'])
            return
        


    def page_pic(
            self, 
            auto:bool, timeout:int|float,
            pic_0:str, pic_1:str,
            ):
        '''
        向双方呈现一个纯图像页面。
        - auto: 是否自动跳转。
        - timeout: 当前页面停留下限时间 / 自动跳转时间。
        - pic_0/1: 若为 None 则不对该被试窗口调用 .flip()。
        '''

        self.dualWin.pic(
            pic_0=pic_0, pic_1=pic_1
            )
        if auto:
            core.wait(timeout if not self._debug else self._mod_intro)
            return
        else:
            core.wait(timeout if not self._debug else self._mod_intro)
            self.wait_kb(listen_keys=config.allowed_key['skip'])
            return    



    def page_Ready_text(
            self,
            text_0:str, text_1:str,
            allowed_bt:str,
            timeout:int|float=config.time['intro_timeout'],
            ):
        '''
        向双方呈现一个手柄按键自助翻页的纯文字页面。
        - timeout: 当前页面停留下限时间。
        '''

        ready_0, ready_1 = False, False

        self.dualWin.Ready_text(
            text_0=text_0, text_1=text_1,
            ready_0=ready_0, ready_1=ready_1
            )
        
        if timeout > 0:
            core.wait(timeout if not self._debug else self._mod_intro)

        while (not ready_0) or (not ready_1):
            core.wait(config.time['io_interval'])
            _pressed_0, _pressed_1 = self.dualJS.check_js()
            if _pressed_0 or _pressed_1:
                if _pressed_0 == allowed_bt:
                    ready_0 = True
                if _pressed_1 == allowed_bt:
                    ready_1 = True
                self.dualWin.Ready_text(
                    text_0=text_0, text_1=text_1,
                    ready_0=ready_0, ready_1=ready_1
                    )
        return



    def page_Ready_pic(
            self, 
            pic_0:str, pic_1:str,
            allowed_bt:str,
            timeout:int|float=config.time['intro_timeout'],
            ):
        '''
        向双方呈现一个手柄按键自助翻页的图像页面。
        '''

        ready_0, ready_1 = False, False

        self.dualWin.Ready_pic(
            pic_0=pic_0, pic_1=pic_1, 
            ready_0=ready_0, ready_1=ready_1
            )
        
        if timeout > 0:
            core.wait(timeout if not self._debug else self._mod_intro)
        
        while True:
            core.wait(config.time['io_interval'])
            _pressed_0, _pressed_1 = self.dualJS.check_js()
            if _pressed_0 or _pressed_1:
                if _pressed_0 == allowed_bt:
                    ready_0 = True
                if _pressed_1 == allowed_bt:
                    ready_1 = True
                self.dualWin.Ready_pic(
                    pic_0=pic_0, pic_1=pic_1, 
                    ready_0=ready_0, ready_1=ready_1
                    )
            if ready_0 and ready_1:
                break
        return
        


    def block(
            self, 
            task_mode:str, report_mode:str,
            block_index:int, 
            trial_num_w:int, trial_num_b:int, 
            ):
        '''
        一个完整的 block: start -> trials -> end
        - task_mode: 'exercise' / 'solo' / 'dual'。
        - report_mode: 'confidence' 或 'ratio'。
        - stage_name: 写入数据的标记名称。
        - block_index: 当前 block 的索引。
            - 0 / 3: 练习阶段（CF / RT，counterbalance）。
            - 1 / 4: solo 阶段（CF / RT，顺序同练习阶段）。
            - 2 / 5: dual 阶段（CF / RT，顺序同练习阶段）。
        - trial_num_b/w: 当前 block 的 trial 数量；'w'=白色多，'b'=黑色多。
        '''

        _trial_num_w = trial_num_w if not self._debug else self._mod_trial
        _trial_num_b = trial_num_b if not self._debug else self._mod_trial

        # dual 模式下先计算对应 solo 的 d'
        if task_mode == 'dual':
            d_0 = self.perf.cal_d(task_mode='solo', report_mode=report_mode, subject=0)
            d_1 = self.perf.cal_d(task_mode='solo', report_mode=report_mode, subject=1)
            harder = 1 if d_0 >= d_1 else 0

            if report_mode == 'confidence':
                self.harder_sub_CF = 0 if harder == 0 else 1
            elif report_mode == 'ratio':
                self.harder_sub_RT = 0 if harder == 0 else 1

            if self._debug:
                print('current_block:\n', task_mode, report_mode)
                print('data_source:\n', 'solo', report_mode)
                print(f"[DEBUG] d_0: {d_0}, d_1: {d_1}, harder: {harder}\n")

        elif task_mode == 'solo' or task_mode == 'exercise':
            d_0 = None
            d_1 = None
            harder = None
        
        # 刺激字典
        StimDict = parser.match_dict(
            json_path=self.json_path, 
            task_mode=task_mode, report_mode=report_mode,
            Perf_0=d_0, Perf_1=d_1
            )
        ## StimDict = {'sub0_w'：{subdict}, 'sub0_b'：{subdict}, 'sub1_w':{subdict}, 'sub1_b':{subdict}}
        ### subdict = {int:list} = {1:[array], 2:[array], ...}

        # 随机化
        ## 全局序列
        _total_trials = _trial_num_w + _trial_num_b
        _series = [i for i in range(_total_trials)]
        rd.shuffle(_series)
        ## 根据全局序列构建传参序列
        _list_bw = ['w'] * _trial_num_w + ['b'] * _trial_num_b
        _list_bw = [_list_bw[i] for i in _series]
        _list_index = [i for i in range(_trial_num_w)] + [i for i in range(_trial_num_b)]
        _list_index = [_list_index[i] for i in _series]
        ## 根据全局序列构建刺激序列
        _stim_keys_0 = [('sub0_w', i) for i in range(_trial_num_w)] + [('sub0_b', i) for i in range(_trial_num_b)]
        _stim_keys_1 = [('sub1_w', i) for i in range(_trial_num_w)] + [('sub1_b', i) for i in range(_trial_num_b)]
        _stim_keys_0 = [_stim_keys_0[i] for i in _series] # [('sub0_b/w', b/w_index), ...]
        _stim_keys_1 = [_stim_keys_1[i] for i in _series] # [('sub1_b/w', b/w_index), ...]
        Stim_Arrays_0 = [StimDict[i[0]][i[1]] for i in _stim_keys_0] # i[0]:sub0_b/w; i[1]:b/w_index
        Stim_Arrays_1 = [StimDict[i[0]][i[1]] for i in _stim_keys_1] # i[0]:sub1_b/w; i[1]:b/w_index

        # 文字
        map_text = {
            ('exercise', 'confidence'): config.text['intro_exercise_solo_CF'],
            ('exercise', 'ratio'): config.text['intro_exercise_solo_RT'],
            ('solo', 'confidence'): config.text['intro_formal_solo_CF'],
            ('solo', 'ratio'): config.text['intro_formal_solo_RT'],
            ('dual', 'confidence'): config.text['intro_formal_dual_CF'],
            ('dual', 'ratio'): config.text['intro_formal_dual_RT'],
        }

        self.page_Ready_text(
            text_0=map_text[(task_mode, report_mode)],
            text_1=map_text[(task_mode, report_mode)],
            timeout=config.time['ready_timeout'],
            allowed_bt=config.allowed_bt['confirm']
            )

        for i in range(_total_trials):
            self.trial(
                harder=harder,
                task_mode=task_mode, report_mode=report_mode,
                block_index=block_index, 
                stim=_list_bw[i], stim_index=_list_index[i], trial_index=i,
                stim_array_0=Stim_Arrays_0[i], stim_array_1=Stim_Arrays_1[i]
                )
        
        self.page_text(
            auto=True, timeout=config.time['auto_timeout'],
            text_0=config.text['block_end'], text_1=config.text['block_end'],
            pos=(0, 0), align='center', boxsize=(1.5, 1.5),
            color=config.color_set['black'], textsize=config.size['text']
            )
       


    def trial(
            self, 
            harder,
            task_mode:str, report_mode:str,
            block_index:int,
            stim:str, trial_index:int, stim_index:int,
            stim_array_0:list[float], stim_array_1:list[float]
            ):
        '''
        一个完整的 trial：ready -> fixation -> stimulus -> private_report (-> public_report) -> feedback
        - harder: 仅用于记录；刺激难度更高的被试（0/1/None）。
        - task_mode: 'solo' 或 'dual'。
        - report_mode: 'confidence' 或 'ratio'。
        - block_index: 仅用于记录。
        - stim: 当前 trial 呈现的刺激的类型（'b'/'w'）。
        - trial_index: 仅用于记录；当前 trial 的索引（int, b&w 共同累计）。
        - stim_index: 仅用于记录；当前 trial 的刺激类型索引（int, b/w 独立累计）。
        - stim_array_0: 被试 0 的刺激数组。
        - stim_array_1: 被试 1 的刺激数组。
        '''

        # 1. ready
        self.page_Ready_text(
            text_0=config.text['ready_trial'], 
            text_1=config.text['ready_trial'], 
            timeout=config.time['ready_timeout'],
            allowed_bt=config.allowed_bt['confirm']
            )
        core.wait(config.time['ready_delay'])

        # 2. fixation
        self.dualWin.fixation()
        core.wait(config.time['fixation'])

        # 3. stimulus
        self.dualWin.stim(
            blackRatio_sub0=stim_array_0,
            blackRatio_sub1=stim_array_1,
            )
        core.wait(config.time['stim'])

        # 4. private_report
        scale_0, scale_1 = 0, 0
        choice_0, choice_1 = None, None
        finish_0, finish_1 = False, False

        def __renderPrivate(subject:int):
            self.dualWin.private_report(
                report_mode=report_mode, 
                subject=subject, 
                scale=scale_0 if subject == 0 else scale_1,
                finish=finish_0 if subject == 0 else finish_1,
                )
        __renderPrivate(subject=0)
        __renderPrivate(subject=1)

        self.clock_local.reset()

        while (not finish_0) or (not finish_1):
            core.wait(config.time['io_interval'])
            _pressed_0, _pressed_1 = self.dualJS.check_js()
            if _pressed_0:
                if _pressed_0 == 'LB':
                    if scale_0 == 1:
                        scale_0 = -1
                        __renderPrivate(subject=0)
                    elif scale_0 > -6:
                        scale_0 -= 1
                        __renderPrivate(subject=0)
                elif _pressed_0 == 'RB':
                    if scale_0 == -1:
                        scale_0 = 1
                        __renderPrivate(subject=0)
                    elif scale_0 < 6:
                        scale_0 += 1
                        __renderPrivate(subject=0)
                elif _pressed_0 == 'A' and scale_0 != 0:
                    duration_0 = self.clock_local.getTime()
                    choice_0 = 'w' if scale_0 < 0 else 'b'
                    finish_0 = True
                    self.scale.ADD(
                        task_mode=task_mode, report_mode=report_mode, subject=0, 
                        value=scale_0
                        )
                    self.perf.ADD(
                        task_mode=task_mode, report_mode=report_mode, subject=0, 
                        actual_stim=stim, choice=choice_0
                        )
                    self.record_trial(
                        block_index=block_index, trial_index=trial_index, stim_index=stim_index,
                        task_mode=task_mode, report_mode=report_mode, stage='private', harder=harder, 
                        actual_stim=stim, subject=0, choice=choice_0, scale=scale_0,
                        duration=duration_0,)
                    if not finish_1:
                        __renderPrivate(subject=0)
            if _pressed_1:
                if _pressed_1 == 'LB':
                    if scale_1 == 1:
                        scale_1 = -1
                        __renderPrivate(subject=1)
                    elif scale_1 > -6:
                        scale_1 -= 1
                        __renderPrivate(subject=1)
                elif _pressed_1 == 'RB':
                    if scale_1 == -1:
                        scale_1 = 1
                        __renderPrivate(subject=1)
                    elif scale_1 < 6:
                        scale_1 += 1
                        __renderPrivate(subject=1)
                elif _pressed_1 == 'A' and scale_1 != 0:
                    duration_1 = self.clock_local.getTime()
                    choice_1 = 'w' if scale_1 < 0 else 'b'
                    finish_1 = True
                    self.scale.ADD(
                        task_mode=task_mode, report_mode=report_mode, subject=1, 
                        value=scale_1
                        )
                    self.perf.ADD(
                        task_mode=task_mode, report_mode=report_mode, subject=1, 
                        actual_stim=stim, choice=choice_1
                        )
                    self.record_trial(
                        block_index=block_index, trial_index=trial_index, stim_index=stim_index,
                        task_mode=task_mode, report_mode=report_mode, stage='private', harder=harder, 
                        actual_stim=stim, subject=1, choice=choice_1, scale=scale_1,
                        duration=duration_1,)
                    if not finish_0:
                        __renderPrivate(subject=1)

        # 5. public_report
        if task_mode == 'dual':
            same_choice = choice_0 == choice_1
            host_choice = None
            host_finish = False
            def __renderPublic():
                self.dualWin.public_report(
                    report_mode=report_mode,
                    same_choice=same_choice,
                    scale_0=scale_0, scale_1=scale_1,
                    host_subject=self.host_subject, wait_subject=self.wait_subject, 
                    host_choice=host_choice
                    )
            __renderPublic()
            if same_choice:
                host_choice = choice_0
                self.perf.ADD(
                    task_mode=task_mode, report_mode=report_mode, subject='public', 
                    actual_stim=stim, choice=host_choice
                    )
                self.record_trial(
                    block_index=block_index, trial_index=trial_index, stim_index=stim_index,
                    task_mode=task_mode, report_mode=report_mode, stage='public', harder=harder,
                    actual_stim=stim, subject='——', choice=host_choice, scale='——',
                    duration=0,)
                core.wait(config.time['report_same'])
            else:
                while not host_finish:
                    core.wait(config.time['io_interval'])
                    pressed_host = self.dualJS.check_js()[self.host_subject]
                    if pressed_host:
                        if pressed_host == 'LB':
                            host_choice = 'w'
                            __renderPublic()
                        elif pressed_host == 'RB':
                            host_choice = 'b'
                            __renderPublic()
                        elif host_choice and pressed_host == 'A':
                            duration_public = self.clock_local.getTime()
                            host_finish = True
                            self.perf.ADD(
                                task_mode=task_mode, report_mode=report_mode, subject='public', 
                                actual_stim=stim, choice=host_choice
                                )
                            self.record_trial(
                                block_index=block_index, trial_index=trial_index, stim_index=stim_index,
                                task_mode=task_mode, report_mode=report_mode, stage='public', harder=harder,
                                actual_stim=stim, subject=self.host_subject, choice=host_choice, scale='——',
                                duration=duration_public,)
                            __renderPublic()
                            core.wait(config.time['report_diff_delay'])
                self.host_subject, self.wait_subject = self.wait_subject, self.host_subject
        
        # 6. feedback
        if task_mode == 'solo' or task_mode == 'exercise':
            self.dualWin.private_feedback(
                subject=0, actual_stim=stim, choice=choice_0
                )
            self.dualWin.private_feedback(
                subject=1, actual_stim=stim, choice=choice_1
                )
            core.wait(config.time['feedback_private'])
        elif task_mode == 'dual':
            self.dualWin.public_feedback(
                actual_stim=stim, 
                choice_0=choice_0, choice_1=choice_1, 
                choice_public=host_choice
                )
            core.wait(config.time['feedback_public'])



    def intermezzo(
            self, 
            text:str=config.text['rest'],
            interval:int=config.time['rest'], 
            bg_color:str=config.color_set['bg_black']
            ):
        '''
        休息阶段。
        '''

        self.dualWin.win0.setColor(bg_color)
        self.dualWin.win1.setColor(bg_color)
        self.dualWin.win0.flip(), self.dualWin.win1.flip()

        self.dualWin.text(
            text_0=text, text_1=text, 
            color=config.color_set['white'],
            )
        core.wait(interval if not self._debug else self._mod_rest)

        self.dualWin.win0.setColor(config.color_set['bg_gray'])
        self.dualWin.win1.setColor(config.color_set['bg_gray'])
        self.dualWin.win0.flip(), self.dualWin.win1.flip()



    def record_trial(
            self,
            block_index:int, trial_index:int, stim_index:int,
            task_mode:str, report_mode:str, stage:str, harder:int|bool, 
            actual_stim:str, subject:int, choice:str, scale:int|str, duration:float, 
            note:str='——'
            ):
        '''
        写入当前 exp 各个 trial 水平的数据（长数据），每个 trial 一行。
        - stage: 'private' / 'public'
        - harder: 0 / 1 / None
        ————————
        'exp_num,disp_mode,debug_mode,condition_A,condition_B,condition_C,'
        'sys_time,exp_time,'
        'block_index,trail_index,stim_index,'
        'task_mode,report_mode,stage,harder,' 
        'actual_stim,subject,choice,scale,dutaion,'
        'note'
        '\n'
        ————————
        '''
        
        with open(file=self.trialData_path, mode='a', encoding='utf-8') as file:
            sys_time = dt.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
            exp_time = self.clock_global.getTime()
            line = (
                f"{self.exp_num},{self._exp_param['disp_mode']},"
                f"{self._exp_param['debug_mode']},"
                f"{self.condition_A},{self.condition_B},{self.condition_C},"
                f"{sys_time},{exp_time},"
                f"{block_index},{trial_index},{stim_index},"
                f"{task_mode},{report_mode},{stage},{harder},"
                f"{actual_stim},{subject},{choice},{scale},{duration},"
                f"{note},"
                "\n"
                )
            file.write(line)



    def record_exp(
            self,
            exp_num:int, disp_mode:str, debug_mode:str,
            condition_A:int, condition_B:int, condition_C:int,
            duration:float,
            harder_sub_CF:float, 
            solo_CF_0:float, solo_CF_1:float,
            dual_CF_0:float, dual_CF_1:float,
            solo_CF_d_0:float, solo_CF_d_1:float,
            dual_CF_d_0:float, dual_CF_d_1:float, dual_CF_d_public:float,
            harder_sub_RT:float,
            solo_RT_0:float, solo_RT_1:float,
            dual_RT_0:float, dual_RT_1:float,
            solo_RT_d_0:float, solo_RT_d_1:float,
            dual_RT_d_0:float, dual_RT_d_1:float, dual_RT_d_public:float,
            ):
        '''
        写入 exp 水平的数据（宽数据），每个 exp 一行。
        ————————
        'exp_num,disp_mode,debug_mode,condition_A,condition_B,condition_C,'
        'duration,'
        'harder_sub_CF,'
        'solo_CF_0,solo_CF_1,dual_CF_0,dual_CF_1,'
        'solo_CF_d_0,solo_CF_d_1,dual_CF_d_0,dual_CF_d_1,dual_CF_d_public,'
        'harder_sub_RT,'
        'solo_RT_0,solo_RT_1,dual_RT_0,dual_RT_1,'
        'solo_RT_d_0,solo_RT_d_1,dual_RT_d_0,dual_RT_d_1,dual_RT_d_public,'
        '\n'
        ————————
        '''

        duration = self.clock_global.getTime()

        with open(file=self.expData_path, mode='a', encoding='utf-8') as file:
            line = (
                f"{exp_num},{disp_mode},{debug_mode},"
                f"{condition_A},{condition_B},{condition_C},"
                f"{duration},"
                f"{harder_sub_CF},"
                f"{solo_CF_0},{solo_CF_1},{dual_CF_0},{dual_CF_1},"
                f"{solo_CF_d_0},{solo_CF_d_1},{dual_CF_d_0},{dual_CF_d_1},{dual_CF_d_public},"
                f"{harder_sub_RT},"
                f"{solo_RT_0},{solo_RT_1},{dual_RT_0},{dual_RT_1},"
                f"{solo_RT_d_0},{solo_RT_d_1},{dual_RT_d_0},{dual_RT_d_1},{dual_RT_d_public},"                
                "\n"
                )
            file.write(line)



    def finale(self):
        '''
        记录 exp 水平的数据，展示实验结束页面。
        '''

        self.record_exp(
            exp_num=self.exp_num,
            disp_mode=self._exp_param['disp_mode'],
            debug_mode=self._exp_param['debug_mode'],
            condition_A=self.condition_A,
            condition_B=self.condition_B,
            condition_C=self.condition_C,
            duration=self.clock_global.getTime(),
            harder_sub_CF=self.harder_sub_CF,
            harder_sub_RT=self.harder_sub_RT,
            solo_CF_0=self.scale.cal_absMean(task_mode='solo', report_mode='confidence', subject=0),
            solo_CF_1=self.scale.cal_absMean(task_mode='solo', report_mode='confidence', subject=1),
            dual_CF_0=self.scale.cal_absMean(task_mode='dual', report_mode='confidence', subject=0),
            dual_CF_1=self.scale.cal_absMean(task_mode='dual', report_mode='confidence', subject=1),
            solo_CF_d_0=self.perf.cal_d(task_mode='solo', report_mode='confidence', subject=0),
            solo_CF_d_1=self.perf.cal_d(task_mode='solo', report_mode='confidence', subject=1),
            dual_CF_d_0=self.perf.cal_d(task_mode='dual', report_mode='confidence', subject=0),
            dual_CF_d_1=self.perf.cal_d(task_mode='dual', report_mode='confidence', subject=1),
            dual_CF_d_public=self.perf.cal_d(task_mode='dual', report_mode='confidence', subject='public'),
            solo_RT_0=self.scale.cal_absMean(task_mode='solo', report_mode='ratio', subject=0),
            solo_RT_1=self.scale.cal_absMean(task_mode='solo', report_mode='ratio', subject=1),
            dual_RT_0=self.scale.cal_absMean(task_mode='dual', report_mode='ratio', subject=0),
            dual_RT_1=self.scale.cal_absMean(task_mode='dual', report_mode='ratio', subject=1),
            solo_RT_d_0=self.perf.cal_d(task_mode='solo', report_mode='ratio', subject=0),
            solo_RT_d_1=self.perf.cal_d(task_mode='solo', report_mode='ratio', subject=1),
            dual_RT_d_0=self.perf.cal_d(task_mode='dual', report_mode='ratio', subject=0),
            dual_RT_d_1=self.perf.cal_d(task_mode='dual', report_mode='ratio', subject=1),
            dual_RT_d_public=self.perf.cal_d(task_mode='dual', report_mode='ratio', subject='public'),
        )

        duration = int(self.clock_global.getTime()//60)
        raw_reward = self.clock_global.getTime()//60
        if raw_reward <= 90:
            raw_reward = 90
        elif raw_reward >= 110:
            raw_reward = 110

        reward = raw_reward \
            + 2 * self.perf.cal_d(task_mode='dual', report_mode='confidence', subject='public') \
            + 2 * self.perf.cal_d(task_mode='dual', report_mode='ratio', subject='public')
        reward = round(reward, 2)

        finale_text = (
            f"实验结束。感谢参与！\n\n"
            f"实验总时长：{duration} 分钟\n"
            f"您的被试费：￥{reward} \n\n"
            f"请将您的【学号】发送至主试微信，并呼唤主试。\n如为校外被试或毕业生，请向主试说明情况。"
            )

        self.page_text(
            auto=False, timeout=config.time['intro_timeout'],
            text_0=finale_text, text_1=finale_text
            )
        
        print(
            f"pc_CF_solo_0:{self.perf.cal_pc(task_mode='solo', report_mode='confidence', subject=0)}, \n"
            f"pc_CF_solo_1:{self.perf.cal_pc(task_mode='solo', report_mode='confidence', subject=1)}, \n"
            f"pc_CF_dual_0:{self.perf.cal_pc(task_mode='dual', report_mode='confidence', subject=0)}, \n"
            f"pc_CF_dual_1:{self.perf.cal_pc(task_mode='dual', report_mode='confidence', subject=1)}, \n"
            "\n"
            f"pc_RT_solo_0:{self.perf.cal_pc(task_mode='solo', report_mode='ratio', subject=0)}, \n"
            f"pc_RT_solo_1:{self.perf.cal_pc(task_mode='solo', report_mode='ratio', subject=1)}, \n"
            f"pc_RT_dual_0:{self.perf.cal_pc(task_mode='dual', report_mode='ratio', subject=0)}, \n"
            f"pc_RT_dual_1:{self.perf.cal_pc(task_mode='dual', report_mode='ratio', subject=1)}, \n"
        )
        
        core.quit()
