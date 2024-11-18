
'''
实验各个流程的图形化实现，以及输入输出的处理模块。
'''

# 内置模块
import os, copy
import datetime as dt
import random as rd
from PIL import Image
# 自编模块
from grid import Grid
from jshub import dual_JS
from config import config
# Psychopy 模块
from psychopy import gui, core, visual
from psychopy.visual import rect
from psychopy.hardware import keyboard

class Experiment:
    '''
    实验事件。
    '''

    exp_existed = []

    with open(file='log.txt', mode='r', encoding='utf-8') as output:
        for i in output:
            exp_existed.append(i.split(',')[0].strip())

    def __init__(self):
        '''
        实例化实验事件、基础i/o。
        '''

        self.DUAL = dual_JS()

        self.kb = keyboard.Keyboard()

        self.clock_global = core.Clock()
        self.clock_local = core.Clock()

        self.total_score_0 = 0
        self.total_score_1 = 0
        self.total_trials = 0
        self.total_wasted = 0
        
    def overture(self):
        '''
        在主试机上提示输入实验与被试信息。
        创建实验窗口，写入日志，并创建实验数据文件。
        '''
        self.exp_param = {'exp_num':len(Experiment.exp_existed)+1, 
                          'exp_cfg_A':[1,2], 'exp_cfg_B':[1,2], 'exp_cfg_C':[1,2], 
                          'mode':['test','formal']}
        self.sub_param = {'gender_1':['Female','Male'], 'age_1':0, 'gender_2':['Female','Male'], 'age_2':0}
        self.reality_param = {'familiarity':['not_defined','familiar','unknown'], 'notes':'null'}

        while True:

            self.exp_info = gui.DlgFromDict(title='[step 1/2] exp_params',
                                            dictionary=self.exp_param, order=self.exp_param.keys())
            self.sub_info = gui.DlgFromDict(title='[step 2/2] sub_params',
                                            dictionary=self.sub_param, order=self.sub_param.keys())

            if self.exp_info.OK == False or self.sub_info.OK == False:
                print ('实验中止，原因：基本信息录入阶段中止。')
                core.quit()
                break
            elif not isinstance(self.exp_param['exp_num'], int):
                print ('无效信息：错误的实验编号参数。')
            elif str(self.exp_param['exp_num']) in Experiment.exp_existed:
                warning = gui.Dlg(title='警告：重复的实验编号。')
                warning.addText('警告：此实验编号已存在。是否覆写该实验的数据信息？')
                warning.show()
                if warning.OK:
                    Experiment.exp_existed += 1
                    Experiment.sub_existed.append(self.sub_param['sub_num'])
                    break
                else:
                    core.quit()
            else:
                Experiment.exp_existed.append(self.exp_param['exp_num'])
                break

        self.Condition_order = self.exp_param['exp_cfg_A']
        self.Condition_undefined_2 = self.exp_param['exp_cfg_B']
        self.Condition_undefined_3 = self.exp_param['exp_cfg_C']
        self.LaunchMode = self.exp_param['mode']

        # 创建一个log文件，仅供记录实验启动参数。
        with open(file='log.txt', mode='a', encoding='utf-8') as log:
            log_info = (
                        f"{self.exp_param['exp_cfg_A']},"
                        f"{self.exp_param['exp_cfg_B']},"
                        f"{self.exp_param['exp_cfg_C']},"
                        f"{self.exp_param['exp_num']},"
                        f"{self.sub_param['gender_1']},"
                        f"{self.sub_param['age_1']},"
                        f"{self.sub_param['gender_2']},"
                        f"{self.sub_param['age_2']},"
                        f"{dt.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}\n"
                        )
            log.write(log_info)

        sub_dir_data = os.path.join(os.getcwd(), 'data')
        sub_dir_proc = os.path.join(os.getcwd(), 'data_proc')
        exp_num = self.exp_param['exp_num']

        datafile_name = f'exp{exp_num}.csv'
        procfile_name = f'proc_exp{exp_num}.txt'
        self.datafile_path = os.path.join(sub_dir_data, datafile_name)
        self.procfile_path = os.path.join(sub_dir_proc, procfile_name)

        # 写入 datafile，记录 trial 水平的实验数据。
        with open(file=self.datafile_path, mode='a', encoding='utf-8') as data:
            head = (
                    'sys_time,exp_time,exp_num,exp_cfg_A,exp_cfg_B,exp_cfg_C,launch_mode,'
                    'gender_sub1,age_sub1,gender_sub2,age_sub2,'
                    'process,stage,trial,'
                    'init_step,init_role,gone_step,score_0,score_1,#redeem,#wasted,waste_step,'
                    '#contribution_0, #contribution_1,'
                    'duration,current_role,choice,notes\n'
                    )
            data.write(head)

        self.record(process='overture')

        # 写入 procfile，记录 step 水平的实验数据。
        with open(file=self.procfile_path, mode='a', encoding='utf-8') as proc:
            head = (
                    'exp_time|process|stage|trial|role|step|score_0|score_1|choice_set|choice_bonus|initiation|destination|unit_bonus\n'
                   )
            proc.write(head)

        # 创建实验窗口，计算界面缩放。
        self.win0 = visual.Window(size=config.resolution, screen=0, 
                                  fullscr=False if self.LaunchMode == 'test' else True, 
                                  color=config.colorset['bg_window'], pos=config.win_pos[0], 
                                  title='main_0', winType='pyglet')
        self.win1 = visual.Window(size=config.resolution, screen=0 if self.LaunchMode == 'test' else 1, 
                                  fullscr=False if self.LaunchMode == 'test' else True, 
                                  color=config.colorset['bg_window'], pos=config.win_pos[1], 
                                  title='main_1', winType='pyglet')
        self.UI_scaling = (min(config.resolution[0]/4, config.resolution[1]/3)) / 256

        # 初始化 global_clock 对象。
        self.clock_global.reset()

    def page_text(self, text:str, wait:float=2, auto:bool=False):
        '''
        向两个窗口（visual.Window）呈现一个静态页面（文字）。
        - text: 文字内容。
        - wait: 在页面上停留的最短时间。
        - auto: 是否在 wait 时间结束后自动翻页。
        '''
        content_win0 = visual.TextStim(text=text, color=config.colorset['default'], height=0.06, bold=True, 
                                       font='Arial Unicode MS', alignText='left', wrapWidth=1.5, units='norm', 
                                       win=self.win0)
        content_win1 = visual.TextStim(text=text, color=config.colorset['default'], height=0.06, bold=True, 
                                       font='Arial Unicode MS', alignText='left', wrapWidth=1.5, units='norm', 
                                       win=self.win1)
        
        content_win0.draw(win=self.win0), content_win1.draw(win=self.win1)
        self.win0.flip(), self.win1.flip()

        core.wait(wait)

        if auto:
            return
        else:
            self.__wait_kb()

    def page_pic(self, filename:str, wait:float=1, auto:bool=False):
        '''
        向两个窗口（visual.Window）呈现一个适应窗口尺寸的静态页面（图片）。
        - filename: 在 image 目录中图片的文件名，包含后缀。
        - wait: 在页面上停留的最短时间。
        - auto: 是否在 wait 时间结束后自动翻页。
        '''
        path = 'image/' + filename

        ratio_win = config.resolution[0] / config.resolution[1]
        with Image.open(path) as img:
            ratio_pic = img.size[0] / img.size[1]

        if ratio_pic >= ratio_win: #超宽图片
            pic_x = config.resolution[0]
            pic_y = img.size[1]*pic_x/img.size[0]
        else: #超高图片
            pic_y = config.resolution[1]
            pic_x = img.size[0]*pic_y/img.size[1]

        content_win0 = visual.ImageStim(image=path, size=(pic_x, pic_y), units='pix', win=self.win0)
        content_win1 = visual.ImageStim(image=path, size=(pic_x, pic_y), units='pix', win=self.win1)

        content_win0.draw(win=self.win0), content_win1.draw(win=self.win1)
        self.win0.flip(), self.win1.flip()

        core.wait(wait)

        if auto:
            return
        else:
            self.__wait_kb()

    def STAGE_grid(self, grid_series:dict, stage:int, shuffle:bool, process_name:str='grid'):
        '''
        一个完整的操作阶段，包含若干个 .__page_trial 方法的调用，grid_series 的顺序随机。
        - grid_series: 实验各阶段的 grid 序列参数，键为以 0 作为起始的自然数列，以字典形式写在 config.py 中。
        - stage: 约定 0=练习阶段，1~2=正式实验阶段，决定矩阵的旋转角度、写入数据文件的内容，并且 stage == 0|1 时不计入汇总数据。
            - stage == 1 为前测（不展示个人分数），网格不旋转；stage == 2 为后测（呈现完整界面），网格旋转 90°。
        - shuffle: 是否打乱 grid_series 的顺序（指导性练习阶段须手动设定为不打乱顺序）。
        - process_name: 流程的名称，只决定写入数据文件的内容。
        '''

        order = [i for i in grid_series.keys()]

        if shuffle:
            rd.shuffle(order)

        self.stage_score_0 = 0
        self.stage_score_1 = 0

        for i in order:

            self.__trial_index = i
            self.__trial_stage = stage

            self.grid = Grid(m=grid_series[i]['m'], n=grid_series[i]['n'], 
                             init_loca=grid_series[i]['init_loca'], 
                             init_step=grid_series[i]['init_step'], 
                             init_role=grid_series[i]['init_role'], 
                             element=grid_series[i]['element'])
            self.grid.rotate(stage=stage)

            self.__page_grid(self.grid, stage=stage, process_name=process_name)

        if stage != 0:
            self.page_text(text=config.static_text['grid_end'], wait=2, auto=False)

        return

    def __page_grid(self, grid:Grid, stage:int, process_name:str='grid'):
        '''
        被试通过手柄进行操作的单个页面。
        此方法仅修改实例属性，图形化由 .render_grid 和 .__render_hud 方法实现，写入数据由 .__record 方法实现。
        - grid: 单个 Grid 实例，以字典形式写在 config.py 中。
        - stage: stage == 0 时不计入汇总数据（呈现完整界面），stage == 1 为前测（不展示个人分数），stage == 2 为后测（呈现完整界面）。
        - process_name: 流程的名称，只决定写入数据文件的内容。
        * 私有接口，仅在 .stage_grid 中调用。
        '''

        render_total = True #始终显示总分

        if stage == 0: #练习阶段有比较限速哦
            render_dual = True
        elif self.Condition_order == '1': #先无比较线索，后有比较线索
            if stage == 1:
                render_dual = False
            elif stage == 2:
                render_dual = True
        elif self.Condition_order == '2': #先有比较线索，后无比较线索
            if stage == 1:
                render_dual = True
            elif stage == 2:
                render_dual = False

        self.destination = copy.deepcopy(grid.loca) #拟移动的位置

        self.__render_grid(win=self.win0), self.__render_hud(win=self.win0)
        self.__render_grid(win=self.win1), self.__render_hud(win=self.win1)
        self.__render_misc(win=self.win0, dual=render_dual, total=render_total)
        self.__render_misc(win=self.win1, dual=render_dual, total=render_total)
        self.win0.flip(), self.win1.flip()

        self.clock_local.reset()

        _js0_before = [False]*len(self.DUAL.js0.getAllButtons())
        _js1_before = [False]*len(self.DUAL.js1.getAllButtons())

        # 接收双手柄输入，更新底层，渲染图形界面
        while True: 

            ## 结束条件
            if grid.step < 0: #按 back_RB 结束，步数变为 -999
                break

            ## 轮询操作
            self.DUAL.win_flipper.flip()

            _pressed_0, _pressed_1 = self.DUAL.check_js(_js0_before=_js0_before, _js1_before=_js1_before)
            _pressed = {0:_pressed_0, 1:_pressed_1}

            if _pressed_0 or _pressed_1:
                if _pressed[grid.role] == 'Y':
                    self.destination[1] += 1 if (self.destination[1] + 1 <= grid.frame_size[1] - 1) else 0
                elif _pressed[grid.role] == 'A':
                    self.destination[1] -= 1 if (self.destination[1] - 1 >= 0) else 0
                elif _pressed[grid.role] == 'X':
                    self.destination[0] -= 1 if (self.destination[0] - 1 >= 0) else 0
                elif _pressed[grid.role] == 'B':
                    self.destination[0] += 1 if (self.destination[0] + 1 <= grid.frame_size[0] - 1) else 0
                elif _pressed[grid.role] == 'LB':
                    if tuple(self.destination) in grid.legal_destination:
                        if grid.role == 0:
                            self.stage_score_0 += grid.unit_bonus[tuple(self.destination)][1] \
                                if grid.unit_bonus[tuple(self.destination)] != (0,0) else -grid.redeem_score
                        elif grid.role == 1:
                            self.stage_score_1 += grid.unit_bonus[tuple(self.destination)][1] \
                                if grid.unit_bonus[tuple(self.destination)] != (0,0) else -grid.redeem_score
                        self.__record_proc(grid=grid, process=process_name, stage=self.__trial_stage, trial=self.__trial_index, role=grid.role, 
                                           step=grid.step, score_0=grid.trial_score_0, score_1=grid.trial_score_1, destination=tuple(self.destination))
                        grid.move_to(tuple(self.destination) ,end=False)
                elif _pressed[grid.role] == 'back_RB':
                    if self.destination == self.grid.loca:
                        grid.move_to(tuple(self.destination), end=True)

                self.__render_grid(win=self.win0), self.__render_hud(win=self.win0)
                self.__render_grid(win=self.win1), self.__render_hud(win=self.win1)
                self.__render_misc(win=self.win0, dual=render_dual, total=render_total)
                self.__render_misc(win=self.win1, dual=render_dual, total=render_total)
                self.win0.flip(), self.win1.flip()
                
            else:
                pass

            core.wait(0.01)

        # 本轮次 grid 结束
        ## 写入数据
        trial_duration = self.clock_local.getTime()
        self.record(process=process_name, stage=self.__trial_stage, trial=self.__trial_index, 
                    init_step=grid.init_step, init_role=grid.init_role, gone_step=grid.gone_step, score_0=grid.trial_score_0, score_1=grid.trial_score_1, 
                    redeem=grid.redeem_count, wasted=grid.wasted, waste_step=grid.wasted_step, contribution_0=grid.contribution_0, contribution_1=grid.contribution_1, 
                    duration=trial_duration)
        self.__record_proc(grid=grid, process=process_name, stage=self.__trial_stage, trial=self.__trial_index, role=grid.role, 
                           step=grid.step, score_0=grid.trial_score_0, score_1=grid.trial_score_1, destination=(-999, -999))
        ## 累计分数
        if (stage == 1) or (stage == 2): #正式实验的两个阶段都计入总分
            self.total_score_0 += grid.trial_score_0
            self.total_score_1 += grid.trial_score_1
            self.total_trials += 1
            self.total_wasted += grid.wasted_step
        else: #练习阶段、能力测试阶段、前测均不计分。
            pass
        ## 结算页面
        core.wait(1) #grid页面冻结
        self.__render_misc(win=self.win0, dual=render_dual, total=render_total, end=True) #呈现结算页面
        self.__render_misc(win=self.win1, dual=render_dual, total=render_total, end=True) #呈现结算页面
        self.win0.flip(), self.win1.flip()
        core.wait(3) #结算页面冻结
        grid.clear()
    
    @property
    def __size(self) -> tuple:
        '''
        计算矩阵绘图区域的限界（元组），以及每个网格的边长（浮点数），返回元组。
        * 私有接口。
        '''
        area_size = [config.draw_range[0]*config.resolution[0], config.draw_range[1]*config.resolution[1]] #绘制区域限界
        unit_size = min((area_size[0]/self.grid.frame_size[0], area_size[1]/self.grid.frame_size[1])) #每个小方格的边长
        return (area_size, unit_size)

    @property
    def __loca_unit(self) -> dict:
        '''
        计算矩阵中每个小方格的位置参数，返回 loca_unit 字典 {(#x, #y):(pix_x, pix_y), ...} 。
        * 私有接口。
        ''' 
        if self.__size[0][0]/self.__size[0][1] <= self.grid.frame_size[0]/self.grid.frame_size[1]: #左右顶边
            loca_list_x = [(i+1/2)*self.__size[1] - self.__size[0][0]/2 + config.draw_offset[0]*config.resolution[0] 
                           for i in range(self.grid.frame_size[0])]
            loca_list_y = [(i+1/2)*self.__size[1] - self.grid.frame_size[1]*self.__size[1]/2 + config.draw_offset[1]*config.resolution[1]
                           for i in range(self.grid.frame_size[1])]

        else: #上下顶边
            loca_list_x = [(i+1/2)*self.__size[1] - self.grid.frame_size[0]*self.__size[1]/2 + config.draw_offset[0]*config.resolution[0]
                           for i in range(self.grid.frame_size[0])]
            loca_list_y = [(i+1/2)*self.__size[1] - self.__size[0][1]/2 + config.draw_offset[1]*config.resolution[1]
                           for i in range(self.grid.frame_size[1])]

        loca_unit = dict()

        for i in range(self.grid.frame_size[0]):
            for j in range(self.grid.frame_size[1]):
                loca_unit[(i,j)] = (loca_list_x[i], loca_list_y[j])

        return loca_unit

    @property
    def __loca_misc(self) -> dict:
        '''
        根据分辨率计算图形界面中文字对象的位置，返回字典 {'item_name' : (pix_x, pix_y), ...} 。
        - 两侧：左上/当前操作者、左下/剩余步数、右/操作提示。
        - 底部：左/你的贡献（如果有），中/队伍总分，右/对方贡献（如果有）。
        * 私有接口。
        '''
        loca_misc = dict()

        loca_misc['redeem_score'] = (-0.12*config.resolution[0], 
                                    (2*config.draw_offset[1]-config.draw_range[1]-1)*config.resolution[1]/4)
        
        loca_misc['score_total'] = (0.12*config.resolution[0], 
                             (2*config.draw_offset[1]-config.draw_range[1]-1)*config.resolution[1]/4)
        
        loca_misc['score_self'] = ((2*config.draw_offset[0]-config.draw_range[0]-1)*config.resolution[0]/4, 
                                   0.15*config.resolution[1])
        
        loca_misc['score_allay'] = ((2*config.draw_offset[0]-config.draw_range[0]-1)*config.resolution[0]/4, 
                                    -0.15*config.resolution[1])
        
        loca_misc['role'] = ((2*config.draw_offset[0]-config.draw_range[0]-1)*config.resolution[0]/4, 
                             0)
        
        loca_misc['tips'] = ((2*config.draw_offset[0]+config.draw_range[0]+1)*config.resolution[0]/4, 
                             0)
        
        loca_misc['end'] = (0, 0,1*config.resolution[1])
        
        loca_misc['end_score_total'] = (0, -0.15*config.resolution[1])

        loca_misc['end_score_self'] = (-0.20*config.resolution[0], -0.15*config.resolution[1])

        loca_misc['end_score_allay'] = (0.20*config.resolution[0], -0.15*config.resolution[1])

        return loca_misc

    def __render_grid(self, win:visual.Window):
        '''
        后端渲染图形化矩阵，不含 .flip()。
        渲染内容包含：基础 Grid 矩阵、网格 bonus 标识。
        * 私有接口，仅在 .__page_trial 中调用。
        '''

        loca_unit = self.__loca_unit
        unit_size = self.__size

        for i in range(self.grid.frame_size[0]):
            for j in range(self.grid.frame_size[1]):
                
                # 基础 Grid unit
                unit = rect.Rect(height=unit_size[1]*config.unit_scaling, width=unit_size[1]*config.unit_scaling, 
                                 lineColor=config.colorset['line_default'], 
                                 lineWidth=config.graph_param['basic_unit_width']*self.UI_scaling, 
                                 pos=loca_unit[(i,j)], units='pix', 
                                 win=win)
                
                # 网格 bonus 标识
                if self.grid.unit_bonus[(i,j)][0] > 0 and self.grid.unit_bonus[(i,j)][1] <= 0: #用分数重置步数
                    text = visual.TextStim(text = f'变为{self.grid.unit_bonus[(i,j)][0]}步\n{self.grid.unit_bonus[(i,j)][1]}分', 
                                           height=unit_size[1]*config.graph_param['tiny_text_scaling'], bold=True, 
                                           font='Arial Unicode MS', alignText='center', 
                                           pos=loca_unit[(i,j)], units='pix', 
                                           win=win)
                    unit.fillColor = config.colorset['bg_step'][self.grid.unit_bonus[(i,j)][0]]
                    unit.draw(win=win), text.draw(win=win)

                elif self.grid.unit_bonus[(i,j)][0] <= 0 and self.grid.unit_bonus[(i,j)][1] > 0: #步数惩罚，分数奖励
                    text = visual.TextStim(text = f'{self.grid.unit_bonus[(i,j)][0]}步\n+{self.grid.unit_bonus[(i,j)][1]}分', 
                                           height=unit_size[1]*config.graph_param['small_text_scaling'], bold=True, 
                                           color=config.colorset['default'], font='Arial Unicode MS', alignText='center', 
                                           pos=loca_unit[(i,j)], units='pix', 
                                           win=win)
                    unit.fillColor = config.colorset['bg_score'][self.grid.unit_bonus[(i,j)][1]]
                    unit.draw(win=win), text.draw(win=win)

                elif self.grid.unit_bonus[(i,j)] == (0,0):
                    # text = visual.TextStim(text = f'', 
                    #                        height=unit_size[1]*config.graph_param['tiny_text_scaling'], bold=True, 
                    #                        font='Arial Unicode MS', color=config.colorset['default'], alignText='center', 
                    #                        pos=loca_unit[(i,j)], units='pix', 
                    #                        win=win)
                    unit.fillColor = config.colorset['bg_empty']
                    unit.draw(win=win)
                    # text.draw(win=win)

                else:
                    raise ValueError(f'grid({i},{j}) 中同时包含了步数奖励与分数奖励 {(self.grid.unit_bonus[(i,j)])}。')

    def __render_hud(self, win:visual.Window): 
        '''
        图形化操作状态，不含.flip()。
        渲染内容包含：当前位置、可移动区域、拟移动位置。
        * 私有接口，仅在 .__page_trial 中调用。
        '''

        loca_unit = self.__loca_unit
        unit_size = self.__size

        # 当前位置
        unit_loca = rect.Rect(height=unit_size[1], width=unit_size[1], units='pix', 
                              color=config.colorset['bg_location'], 
                              pos=loca_unit[tuple(self.grid.loca)], 
                              win=win)
        unit_loca_step = visual.TextStim(text=f'剩余\n{self.grid.step}步' if self.grid.step >= 0 else '本轮\n结束', 
                                         height=unit_size[1]*config.graph_param['small_text_scaling'], bold=True, 
                                         font='Arial Unicode MS', alignText='center', 
                                         pos=loca_unit[tuple(self.grid.loca)], units='pix', 
                                         win=win)
        unit_loca.draw(win=win), unit_loca_step.draw(win=win)

        # 可移动区域
        for i in self.grid.legal_destination:
            
            unit_legal = rect.Rect(height=unit_size[1], width=unit_size[1], 
                                   lineColor=config.colorset['line_legal'], 
                                   lineWidth=config.graph_param['legal_unit_width']*self.UI_scaling, 
                                   color=None, pos=loca_unit[i], units='pix', 
                                   win=win)
            unit_legal.draw(win=win)
            
        # 拟移动位置
        unit_moveto = rect.Rect(height=unit_size[1], width=unit_size[1], 
                                lineColor=config.colorset['line_moveto'], 
                                lineWidth=config.graph_param['moveto_unit_width']*self.UI_scaling, 
                                color=None, pos=loca_unit[tuple(self.destination)], units='pix', 
                                win=win)
        unit_moveto.draw(win=win)

    def __render_misc(self, win:visual.Window, dual:bool, total:bool, end:bool=False):
        '''
        图形化其它元素，不含 .flip()。
        包含：操作提示、队伍总分、双方得分、操作者。部分内容仅在 step_runout == True 或 False 时调用。
        - dual: 是否显示双方得分。
        - total: 是否显示总分。
        - strategy: 决定是否显示兑换消耗。
        - end: 当前 trial 是否已经结束，决定渲染逻辑，包括分数的位置、是否渲染非分数项目。
        * 私有接口，仅在 .__page_trial（trial 中）和 .STAGE_task（trial 结束时）调用。
        '''
        
        loca_misc = self.__loca_misc

        # 操作提示（trial中）
        tips_dual = visual.TextStim(text=config.hud_text['tips'], color=config.colorset['default'], bold=True, 
                                    height=config.font_size*config.graph_param['small_text_scaling']*self.UI_scaling,
                                    font='Arial Unicode MS', alignText='center', 
                                    pos=loca_misc['tips'], units='pix', 
                                    win=win)

        # 当前角色（trial中）
        if win == self.win0:
            role_sep = visual.TextStim(text=config.hud_text['turn_self'] if self.grid.role == 0 else config.hud_text['turn_allay'], 
                                       color=config.colorset['self_related'] if self.grid.role == 0 else config.colorset['allay_related'], 
                                       height=config.font_size*config.graph_param['huge_text_scaling']*self.UI_scaling if self.grid.role == 0 \
                                         else config.font_size*config.graph_param['medium_text_scaling']*self.UI_scaling, 
                                       font='Arial Unicode MS', alignText='center', bold=True, 
                                       pos=loca_misc['role'], units='pix', 
                                       win=win)
        elif win == self.win1:
            role_sep = visual.TextStim(text=config.hud_text['turn_self'] if self.grid.role == 1 else config.hud_text['turn_allay'], 
                                       color=config.colorset['self_related'] if self.grid.role == 1 else config.colorset['allay_related'], 
                                       height=config.font_size*config.graph_param['huge_text_scaling']*self.UI_scaling if self.grid.role == 1 \
                                         else config.font_size*config.graph_param['medium_text_scaling']*self.UI_scaling, 
                                       font='Arial Unicode MS', alignText='center', bold=True, 
                                       pos=loca_misc['role'], units='pix', 
                                       win=win)
            
        # 兑换消耗（trial中）
        redeem_score_text = config.hud_text['redeem_score'] + f'\n{self.grid.redeem_score} 分'
        redeem_score = visual.TextStim(text=redeem_score_text, color=config.colorset['obvious'], bold=True, 
                                       height=config.font_size*config.graph_param['large_text_scaling']*self.UI_scaling, 
                                       font='Arial Unicode MS', alignText='center', pos=loca_misc['redeem_score'],
                                       units='pix', win=win)
        
        # 双方得分或总分（trial中 / trial结束时），二者不会同时出现
        score_self_text = \
            config.hud_text['score_self'] + f'\n{self.stage_score_0}' if win == self.win0 \
            else config.hud_text['score_self'] + f'\n{self.stage_score_1}'
        score_allay_text = \
            f'{self.stage_score_1}\n' + config.hud_text['score_allay'] if win == self.win0 \
            else f'{self.stage_score_0}\n' + config.hud_text['score_allay']
        score_allay_text_end = \
            config.hud_text['score_allay'] + f'\n{self.stage_score_1}' if win == self.win0 \
            else config.hud_text['score_allay'] + f'\n{self.stage_score_0}'
        
        score_self = visual.TextStim(text=score_self_text, color=config.colorset['self_related'], bold=True, 
                                     height=config.font_size*config.graph_param['large_text_scaling']*self.UI_scaling, 
                                     font='Arial Unicode MS', alignText='center', 
                                     pos=loca_misc['score_self'] if not end else loca_misc['end_score_self'], 
                                     units='pix', win=win)
        score_allay = visual.TextStim(text=score_allay_text if not end else score_allay_text_end, 
                                      color=config.colorset['allay_related'], bold=True, 
                                      height=config.font_size*config.graph_param['large_text_scaling']*self.UI_scaling, 
                                      font='Arial Unicode MS', alignText='center', 
                                      pos=loca_misc['score_allay'] if not end else loca_misc['end_score_allay'], 
                                      units='pix', win=win)
        
        score_total_text = config.hud_text['score_total'] + f'\n{self.stage_score_0 + self.stage_score_1} 分'
        total = visual.TextStim(text=score_total_text, color=config.colorset['team_related'], bold=True, 
                                    height=config.font_size*config.graph_param['large_text_scaling']*self.UI_scaling, 
                                    font='Arial Unicode MS', alignText='center', 
                                    pos=loca_misc['score_total'] if not end else loca_misc['end_score_total'], 
                                    units='pix', win=win)

        # trial 结束提示文字（trial结束时）
        end_trial = visual.TextStim(text=config.hud_text['end'], color=config.colorset['default'], bold=True, 
                                    height=config.font_size*config.graph_param['large_text_scaling']*self.UI_scaling,
                                    font='Arial Unicode MS', alignText='center', 
                                    pos=loca_misc['end'], units='pix', 
                                    win=win)
        
        # 根据任务设置显示的分数
        if dual:
            score_self.draw(win=win)
            score_allay.draw(win=win)
        if total:
            total.draw(win=win)

        # 根据是否结束 trial 显示的内容
        if not end:
            tips_dual.draw(win=win)
            role_sep.draw(win=win)
            redeem_score.draw(win=win)
        else:
            end_trial.draw(win=win)

    def STAGE_choice(self, stage:int, mode:str):
        '''
        一个完整的选择阶段，包含若干个 .__page_choice 方法的调用，顺序随机。
        - stage: 调用第几个阶段的问题。
        - mode: 'opinion'=问题评判（特质相似性操纵），'thinking'=思维能力测试（能力相似性操纵）。
        '''
        
        if mode == 'opinion':
            question = config.choice_opinion
        elif mode == 'thinking':
            question = config.choice_thinking
        
        order = [i for i in range(len(question[stage]))]
        rd.shuffle(order)

        # 每一阶段双方的选项记录
        self.choice_0 = {i:None for i in range(len(question[stage]))}
        self.choice_1 = {i:None for i in range(len(question[stage]))}

        self.clock_local.reset()

        for i in order:
            self.opinion_stage = stage
            self.opinion_index = i
            self.__page_choice(text=question[stage][i], mode=mode)

        opinion_duration = self.clock_local.getTime()

        self.record(process='STAGE_opinion', stage=stage, 
                    duration=opinion_duration)

        self.page_text(text=config.static_text['stage_end'], wait=2, auto=True)

        self.__choice_result(mode = mode, 
                             similarity = 'same' if self.Condition_undefined_2 == '1' else 'diff')

    def __page_choice(self, text:str, mode:str):
        '''
        向两个窗口呈现一个选项页面，要求进行迫选操作，由双方进行独立操作，含等待逻辑。
        - text: 选项文本字典，统一写在 config.py 中。
        - mode: 'opinion'=问题评判（特质相似性操纵），'thinking'=思维能力测试（能力相似性操纵）。
        * 私有接口，仅在 .stage_choice 中调用。
        '''

        if mode == 'opinion':
            choice_guide = config.opinion_guide
            choice_confirm = config.opinion_confirm
        elif mode == 'thinking':
            choice_guide = config.thinking_guide
            choice_confirm = config.thinking_confirm

        opt_win0 = visual.TextStim(text=text, color=config.colorset['default'], height=0.07, bold=True, 
                                   font='Arial Unicode MS', alignText='center', wrapWidth=1.5, units='norm', 
                                   pos=config.choice_pos['content'], win=self.win0)
        opt_win1 = visual.TextStim(text=text, color=config.colorset['default'], height=0.07, bold=True, 
                                   font='Arial Unicode MS', alignText='center', wrapWidth=1.5, units='norm', 
                                   pos=config.choice_pos['content'], win=self.win1)
        
        opt_guide_win0 = visual.TextStim(text=choice_guide, 
                                         color=config.colorset['obvious'], height=0.05, bold=True, 
                                         font='Arial Unicode MS', alignText='center', wrapWidth=1.5, units='norm', 
                                         pos=config.choice_pos['guide'], win=self.win0)
        opt_guide_win1 = visual.TextStim(text=choice_guide, 
                                         color=config.colorset['obvious'], height=0.05, bold=True, 
                                         font='Arial Unicode MS', alignText='center', wrapWidth=1.5, units='norm', 
                                         pos=config.choice_pos['guide'], win=self.win1)

        opt_win0.draw(win=self.win0), opt_win1.draw(win=self.win1)
        opt_guide_win0.draw(win=self.win0), opt_guide_win1.draw(win=self.win1)
        self.win0.flip(), self.win1.flip()

        ready_to_choose_0, ready_to_choose_1 = None, None
        finished_0, finished_1 = False, False

        core.wait(1)

        _js0_before = [False]*len(self.DUAL.js0.getAllButtons())
        _js1_before = [False]*len(self.DUAL.js1.getAllButtons())

        while (not finished_0) or (not finished_1):

            _pressed_0, _pressed_1 = self.DUAL.check_js(_js0_before=_js0_before, _js1_before=_js1_before)

            # 监听 sub0 选项
            if not finished_0: 
                if _pressed_0 == 'X':
                    ready_to_choose_0 = 'X'
                    opt_1 = visual.TextStim(text=choice_confirm['X'], 
                                            color=config.colorset['self_related'], height=0.08, bold=True, 
                                            font='Arial Unicode MS', alignText='center', units='norm', 
                                            pos=config.choice_pos['choice'], win=self.win0)
                    opt_1.draw(win=self.win0), opt_win0.draw(win=self.win0), opt_guide_win0.draw(win=self.win0)
                    self.win0.flip()
                elif _pressed_0 == 'B':
                    ready_to_choose_0 = 'B'
                    opt_1 = visual.TextStim(text=choice_confirm['B'], 
                                            color=config.colorset['self_related'], height=0.08, bold=True, 
                                            font='Arial Unicode MS', alignText='center', units='norm', 
                                            pos=config.choice_pos['choice'], win=self.win0)
                    opt_1.draw(win=self.win0), opt_win0.draw(win=self.win0), opt_guide_win0.draw(win=self.win0)
                    self.win0.flip()
                elif ready_to_choose_0 and _pressed_0 == 'LB':
                    finished_0 = True
                    self.choice_0[self.opinion_index] = ready_to_choose_0
                    self.record(process='opinion_choice', stage=self.opinion_stage, trial=self.opinion_index, 
                                current_role=0, choice=ready_to_choose_0)
                    self.__wait_allay(self.win0)

            # 监听 sub1 选项
            if not finished_1: 
                if _pressed_1 == 'X':
                    ready_to_choose_1 = 'X'
                    opt_2 = visual.TextStim(text=choice_confirm['X'], 
                                            color=config.colorset['self_related'], height=0.08, bold=True, 
                                            font='Arial Unicode MS', alignText='center', units='norm', 
                                            pos=config.choice_pos['choice'], win=self.win1)
                    opt_2.draw(win=self.win1), opt_win0.draw(win=self.win1), opt_guide_win0.draw(win=self.win1)
                    self.win1.flip()
                elif _pressed_1 == 'B':
                    ready_to_choose_1 = 'B'
                    opt_2 = visual.TextStim(text=choice_confirm['B'], 
                                            color=config.colorset['self_related'], height=0.08, bold=True, 
                                            font='Arial Unicode MS', alignText='center', units='norm', 
                                            pos=config.choice_pos['choice'], win=self.win1)
                    opt_2.draw(win=self.win1), opt_win0.draw(win=self.win1), opt_guide_win0.draw(win=self.win1)
                    self.win1.flip()
                elif ready_to_choose_1 and _pressed_1 == 'LB':
                    finished_1 = True
                    self.choice_1[self.opinion_index] = ready_to_choose_1
                    self.record(process='opinion_choice', stage=self.opinion_stage, trial=self.opinion_index, 
                                current_role=1, choice=ready_to_choose_1)
                    self.__wait_allay(self.win1)
            
            self.DUAL.win_flipper.flip()
            core.wait(0.01)
        
        return

    def __choice_result(self, mode:str, similarity:str):
        '''
        展示双方在思维能力测试阶段的结果（异同或得分）。
        - mode: 'opinion' / 'thinking'
        - similarity: 'same' / 'diff'
        * 私有接口，仅在 .STAGE_choice 中调用。
        '''

        if mode == 'opinion':

            self.page_text(text=config.opinion_result[similarity], wait=5, auto=False)

        elif mode == 'thinking':

            score_win0 = visual.TextStim(
                text=config.thinking_result[similarity][0], 
                color=config.colorset['default'], height=0.07, bold=True, 
                font='Arial Unicode MS', alignText='center', wrapWidth=1.5, units='norm', 
                pos=config.choice_pos['content'], win=self.win0)
            score_win1 = visual.TextStim(
                text=config.thinking_result[similarity][1], 
                color=config.colorset['default'], height=0.07, bold=True, 
                font='Arial Unicode MS', alignText='center', wrapWidth=1.5, units='norm', 
                pos=config.choice_pos['content'], win=self.win1)

            score_win0.draw(win=self.win0), score_win1.draw(win=self.win1)
            self.win0.flip(), self.win1.flip()
            self.__wait_kb()
    
    def STAGE_discussion(self, stage:int, duration:int=120):
        '''
        选择一个双方观点相同 / 不同的项目呈现。
        - stage: 在第几个实验任务阶段后调用，值域 1~3。
        - duration: 该阶段呈现时长，默认 120s。
        '''

        order = [i for i in range(len(config.choice_opinion[stage]))]
        rd.shuffle(order)

        discuss_guide = config.discuss_guide[None]
        discuss_topic = ' '
        topic_index = None
        coincidence = True

        if self.Condition_undefined_2 == '1': #呈现相同观点的条目
            for i in order:
                if self.choice_0[i] == self.choice_1[i]:
                    discuss_guide = config.discuss_guide['same']
                    discuss_topic = config.choice_opinion[stage][i]
                    topic_index = i
                    coincidence = False
                    if self.choice_0[i] == 'X':
                        dual_choice_state_0 = config.discuss_choice['same_X']
                        dual_choice_state_1 = config.discuss_choice['same_X']
                    elif self.choice_0[i] == 'B':
                        dual_choice_state_0 = config.discuss_choice['same_B']
                        dual_choice_state_1 = config.discuss_choice['same_B']
                    self.record(process='STAGE_discussion', stage=stage, trial=topic_index, notes=f'TOPIC/SAME: {discuss_topic}')
                    break

        elif self.Condition_undefined_2 == '2': #呈现不同观点的条目
            for i in order:
                if self.choice_0[i] != self.choice_1[i]:
                    discuss_guide = config.discuss_guide['diff']
                    discuss_topic = config.choice_opinion[stage][i]
                    topic_index = i
                    coincidence = False
                    if self.choice_0[i] == 'X':
                        dual_choice_state_0 = config.discuss_choice['diff_X']
                        dual_choice_state_1 = config.discuss_choice['diff_B']
                    elif self.choice_0[i] == 'B':
                        dual_choice_state_0 = config.discuss_choice['diff_B']
                        dual_choice_state_1 = config.discuss_choice['diff_X']
                    self.record(process='STAGE_discussion', stage=stage, trial=topic_index, notes=f'TOPIC/DIFF: {discuss_topic}')
                    break

        if coincidence:

            self.record(notes='Coincidence situation occurred.')

        else:

            text_guide_win0 = visual.TextStim(text=discuss_guide, color=config.colorset['obvious'], height=0.05, bold=True, 
                                              font='Arial Unicode MS', alignText='center', wrapWidth=1.5, units='norm', 
                                              pos=config.discuss_pos['guide'], win=self.win0)
            text_guide_win1 = visual.TextStim(text=discuss_guide, color=config.colorset['obvious'], height=0.05, bold=True, 
                                              font='Arial Unicode MS', alignText='center', wrapWidth=1.5, units='norm', 
                                              pos=config.discuss_pos['guide'], win=self.win1)

            text_topic_win0 = visual.TextStim(text=discuss_topic, color=config.colorset['default'], height=0.07, bold=True, 
                                              font='Arial Unicode MS', alignText='center', wrapWidth=1.5, units='norm', 
                                              pos=config.discuss_pos['topic'], win=self.win0)
            text_topic_win1 = visual.TextStim(text=discuss_topic, color=config.colorset['default'], height=0.07, bold=True, 
                                              font='Arial Unicode MS', alignText='center', wrapWidth=1.5, units='norm', 
                                              pos=config.discuss_pos['topic'], win=self.win1)

            text_self_win0 = visual.TextStim(text=dual_choice_state_0, 
                                             color=config.colorset['self_related'], height=0.07, bold=True, 
                                             font='Arial Unicode MS', alignText='center', wrapWidth=1.5, units='norm', 
                                             pos=config.discuss_pos['self'], win=self.win0)
            text_self_win1 = visual.TextStim(text=dual_choice_state_1, 
                                             color=config.colorset['self_related'], height=0.07, bold=True, 
                                             font='Arial Unicode MS', alignText='center', wrapWidth=1.5, units='norm', 
                                             pos=config.discuss_pos['self'], win=self.win1)

            text_guide_win0.draw(win=self.win0), text_guide_win1.draw(win=self.win1)
            text_topic_win0.draw(win=self.win0), text_topic_win1.draw(win=self.win1)
            text_self_win0.draw(win=self.win0), text_self_win1.draw(win=self.win1)
            self.win0.flip(), self.win1.flip()

            core.wait(duration)
            self.page_text(text=config.static_text['discussion_end'], wait=2, auto=False)

    def __wait_allay(self, win:visual.Window):
        '''
        向窗口呈现等待空屏。
        - win: 目标窗口。
        * 私有接口，仅在 .__page_choice 中调用。
        '''
        wait = visual.TextStim(text=config.choice_wait, color=config.colorset['default'], height=0.06, bold=True, 
                               font='Arial Unicode MS', alignText='center', wrapWidth=1.5, units='norm', 
                               win=win)
        wait.draw(win=win), win.flip()

    def __wait_kb(self, key:tuple=config.key_nextpage) -> list:
        '''
        清空按键记录，轮询并等待键盘按键，进行特定按键后返回最后一个按键的字符串。
        - key: 按键字符串构成的元组。
        * 私有接口。
        '''
        self.kb.clearEvents()
        while True:
            pressed = self.kb.getKeys()
            if pressed:
                if pressed[-1].name in key:
                    break
            else:
                core.wait(0.01)
        return pressed[-1]

    def record(self, process:str='null', stage:int=-1, trial:int=-1, 
               init_step:int=-1, init_role:int=-1, gone_step:int=-1, score_0:int=-999, score_1:int=-999, 
               redeem:int=-999, wasted:int=-999, waste_step:int=-999, contribution_0:int=-999, contribution_1:int=-999, duration:float=-1, 
               current_role:int=-1, choice:str='null', notes:str='null'):
        '''
        在每个 trail 完成后，将数据写入文件。
        适用于：.__page_trial, .__page_choice 方法。
        需要接受的参数：
        - process: 实验当前进程的名称。
        - stage: 合作任务的阶段序数（block）。
        - trial: 当前阶段的试次序数（index）。
        - init_step: 当前 trial 的初始步数。
        - init_role: 当前 trial 的先手角色。
        - gone_step: 当前 trial 行进的真实步数。
        - score_0/1: 当前 trial 双方的得分。
        - redeem: 当前 trial 兑换步数的次数。
        - wasted: 当前 trial 出现步数浪费的次数。
        - waste_step: 当前 trial 总共浪费掉的步数。
        - contribution_0/1: 当前 trial 双方用分数换步数的次数。
        - duration: 当前 trial 耗费时间。
        - current_role: 提交选择的角色。
        - choice: 当前角色进行的选择。
        - notes: 备注。
        '''
        with open(file=self.datafile_path, mode='a', encoding='utf-8') as data:
            data.write(f'{dt.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")},{format(self.clock_global.getTime(),".3f")},')
            data.write(f'{self.exp_param["exp_num"]},{self.Condition_order},{self.Condition_undefined_2},{self.Condition_undefined_3},{self.LaunchMode},')
            data.write(f'{self.sub_param["gender_1"]},{self.sub_param["age_1"]},{self.sub_param["gender_2"]},{self.sub_param["age_2"]},')
            data.write(f'{process},{stage},{trial},{init_step},{init_role},{gone_step},{score_0},{score_1},')
            data.write(f'{redeem},{wasted},{waste_step},{contribution_0},{contribution_1},')
            data.write(f'{format(duration,".3f")},')
            data.write(f'{current_role},{choice},')
            data.write(f'{notes}\n')

    def __record_proc(self, grid:Grid, process:str='null', stage:int=-1, trial:int=-1, role:int=-1, step:int=-999, 
                      score_0:int=-999, score_1:int=-999, destination:tuple=(-999,-999)):
        '''
        在每个 trial 的每次操作完成后，记录过程性数据，解析为 .csv 时应设置 `|` 作为分隔符。
        该方法应于每次被试执行合法选择后，以及调用 .moveto 方法之前调用，并在当前回合循环结束时再次调用（与 .record 方法同时机）.
        回合结束调用时 destination 参数应设置为负整数元组，以示区分。
        * 私有接口。
        '''
        with open(file=self.procfile_path, mode='a') as proc:
            proc.write(f'{format(self.clock_global.getTime(),".3f")}|')
            proc.write(f'{process}|{stage}|{trial}|{role}|{step}|{score_0}|{score_1}|')
            if (destination[0] >= 0) and (destination[1]) >= 0:
                proc.write(f'{grid.legal_bonus}|{grid.unit_bonus[destination]}|')
            else:
                proc.write(f'END_OF_TRIAL|END_OF_TRIAL|')
            proc.write(f'{str(tuple(grid.loca))}|{str(destination)}|{str(grid.unit_bonus)}\n')

    def clear_total(self):
        '''
        将双方在整个任务中的累计总分、累计总 trial 数量、累计浪费步数归零。
        在每个走方格的 stage 之前调用一次。
        '''
        self.total_score_0 = 0
        self.total_score_1 = 0
        self.total_trials = 0
        self.total_wasted = 0
            
    # def set_marker(self, code:int=0):
    #     '''
    #     向采集设备发送 8bit trigger。
    #     - code 含义：见 notes.md。
    #     '''
    #     if self.mark_mode == 0:
    #         self.port.write(code)
    #     elif self.mark_mode == 1:
    #         parallel.setData(code)

    def finale(self):
        '''
        结束实验。
        '''
        self.record(process='finale')
        self.page_text(
                        text=(
                             f'任务表现汇总：\n'
                             f'sub_0: {self.total_score_0}\n'
                             f'sub_1: {self.total_score_1}\n'
                             f'total: {self.total_score_0 + self.total_score_1}\n'
                             f'wasted:{self.total_wasted}'
                             ),
                        wait=5,
                        auto=False)
        self.page_text(text=config.static_text['finale'], wait=5, auto=True)
        core.quit()
