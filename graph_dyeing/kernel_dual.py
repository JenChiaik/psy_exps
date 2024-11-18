'''
双人版本实验核心实现模块。\n
调用时须连接 2 只手柄。
'''
# 内置模块
import os
import datetime as dt
import random as rd
import numpy as np
# 自编模块
import config, score
# from config_Class import config # 后续开发应改用私有类
from graph import GraphSeries
# Psychopy 模块
from psychopy import gui, core, visual, parallel
from psychopy.visual import circle, polygon
from psychopy.hardware import keyboard, joystick
# from psychopy.parallel._inpout import PParallelInpOut
# from psychopy.parallel._dlportio import PParallelDLPortIO

class Experiment:

    exp_existed = []

    with open(file='log.txt',mode='r',encoding='utf-8') as output:
        # 每行 log.txt 格式：xp_config,exp_num,gender_1,age_1,gender_2,age_2,sys_time
        # 例如：1,345,Female,0,Female,0,2024-04-16 13:48:05
        for i in output:
            exp_existed.append(i.split(',')[0].strip())

    def __init__(self):
        '''
        实例化实验事件、基础i/o。
        '''
        if joystick.getNumJoysticks() <= 1:
            raise IOError(f'\n未检测到足够数量的手柄。\n当前手柄数量：{joystick.getNumJoysticks()}。')

        self.win_flipper = visual.Window(size=(400,300), screen=0, color='#000000', title='.flip()' ,winType='pyglet')

        self.kb = keyboard.Keyboard()
        self.js1 = joystick.XboxController(0)
        self.js2 = joystick.XboxController(1)

        joystick.backend = 'pyglet'
        joystick.getNumJoysticks()

        # self.port = parallel.ParallelPort(address=...)
        # self.port.setData(00000000)

    def overture(self):
        '''
        在主试机上提示输入实验与被试信息。
        创建实验窗口，写入日志，并创建实验数据文件。
        '''
        self.exp_param = {'exp_num':len(Experiment.exp_existed)+1,'exp_config':[1,2]}
        self.sub_param = {'gender_1':['Female','Male'], 'age_1':0, 'gender_2':['Female','Male'], 'age_2':0}
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

        # 创建一个log文件，仅供记录实验启动参数。
        with open(file='log.txt',mode='a',encoding='utf-8') as log:
            log_info = f'{self.exp_param["exp_config"]}' + ',' +  f'{self.exp_param["exp_num"]}' + ',' + \
                       f'{self.sub_param["gender_1"]}' + ',' + f'{self.sub_param["age_1"]}' + ',' + \
                       f'{self.sub_param["gender_2"]}' + ',' + f'{self.sub_param["age_2"]}' + ',' + \
                       f'{dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n'
            log.write(log_info)

        # 创建一个datafile，记录完整的实验数据。
        sub_dir = os.path.join(os.getcwd(), 'datafile_dual')
        exp_num = self.exp_param['exp_num']
        self.exp_cfg = self.exp_param['exp_config']
        datafile_name = f'cfg{self.exp_cfg}_exp{exp_num}.txt'
        self.datafile_path = os.path.join(sub_dir, datafile_name)
        with open(file=self.datafile_path, mode='a', encoding='utf-8') as data:
            data.write('sys_time,exp_num,exp_cfg,gender_sub1,age_sub1,gender_sub2,age_sub2,exp_time,lable,sub_id,gs_id,score_total,score_a,score_b,notes\n')

        # 主试窗口
        self.win0 = visual.Window(size=config.res_conductor, screen=0, color='#ffffff', pos=(1440,200))
        # 被试窗口（双屏调试）
        self.win1 = visual.Window(screen=1, size=config.res_subjects, color='#ffffff', pos=(0,200))
        self.win2 = visual.Window(screen=1, size=config.res_subjects, color='#ffffff', pos=(1440,1000))
        # 被试窗口（三屏调试）
        # self.win1 = visual.Window(screen=1, size=config.res_subjects, color='#ffffff')
        # self.win2 = visual.Window(screen=2, size=config.res_subjects, color='#ffffff')
        self.clock = core.Clock()

        self.horizon_px, self.vertical_px = config.res_subjects

    def page_text(self, text='var not defined', pos=(0,0), height=0.05, color='#000000',
                  align='left', units = 'norm', allowed_keys=config.keys_nextpage, wait=0):
        '''
        呈现静态文本页面，由主试按回车键控制翻页。
            text: 文本内容，统一写在 config.py 模块中。
            stage_name: 记录在 datafile.txt 中时间属性的字段。
            allowed_keys: 接受的按键列表。
            wait: 按键生效前的等待时间。
        (该方法带有对 .flip() 方法的调用，所以只适用于只包含静态文本的页面，不要在其它函数内调用。)
        '''
        text1 = visual.TextStim(win=self.win0, text=text, pos=pos, font='Arial Unicode MS',
                                height=height, color=color, alignText=align, bold=True, units=units)
        text2 = visual.TextStim(win=self.win1, text=text, pos=pos, font='Arial Unicode MS',
                                height=height, color=color, alignText=align, bold=True, units=units)
        text3 = visual.TextStim(win=self.win2, text=text, pos=pos, font='Arial Unicode MS',
                                height=height, color=color, alignText=align, bold=True, units=units)
        text1.draw(), text2.draw(), text3.draw()
        self.win0.flip(), self.win1.flip(), self.win2.flip()
        core.wait(wait)
        self.kb.clearEvents()

        while True:
            pressed = self.kb.getKeys()
            if pressed:
                if pressed[-1].name == allowed_keys:
                    self.kb.clearEvents()
                    self.win1.clearBuffer()
                    break
            else:
                core.wait(0.01)
        self.kb.clearEvents()
        return
    
    def page_coloring(self, stage:int):
        '''
        阶段控制。
        - 将当前阶段的所有图形序列随机化。
        - 记录当前 sub 1/2 所在的页面（第几个图形序列）。
        - 呈现新页面的初始状态，不改变另一方的中断状态。
        - 监控双方进程，调用 .operation 控制新页面的呈现和当前阶段的结束。
        '''
        self.kb.clearEvents()
        self.current_page = {1:0, 2:0} # 当前 sub1/2 分别执行到的 gs 序列号
        self.next_page_1, self.next_page_2 = True, True # 是否将 sub 1/2 的图形序列更新至下一页
        self.finish_1, self.finish_2 = False, False # sub 1/2 是否完成了当前阶段的所有序列

        self.score_1 = []
        self.score_2 = []

        gs_stage = {0:config.graph_dict_exercise, 
                    1:config.graph_dict_stage1, 
                    2:config.graph_dict_stage2}
        self.gs_order = [i for i in gs_stage[stage].keys()]
        rd.shuffle(self.gs_order) # 本组被试呈现 gs 的顺序随机化

        while True: # 外层循环，负责切换新的图形序列、呈现等待页面，或结束方法
            if self.next_page_1 and self.current_page[1] <= len(gs_stage[stage])-1: # sub 1 完成序列，未完成阶段
                self.selected_color_index_1, self.selected_shape_index_1 = 0, 0
                self.render_graph(GS=GraphSeries(*gs_stage[stage][self.gs_order[self.current_page[1]]]['uncolored'],
                                                 **gs_stage[stage][self.gs_order[self.current_page[1]]]['colored']), 
                                  win=self.win1)
                # self.write_data(lable=f'stage{stage}_sub1_gs{gs_order[self.current_page[1]]}')
                self.GS1_copy = GraphSeries(*gs_stage[stage][self.gs_order[self.current_page[1]]]['uncolored'],
                                            **gs_stage[stage][self.gs_order[self.current_page[1]]]['colored'])
                self.render_hud(win=self.win1)
                self.win1.flip()
                self.next_page_1 = False
            elif self.current_page[1] >= len(gs_stage[stage]) : # sub 1 完成阶段
                self.finish_1 = True
                if self.finish_2 == True:
                    return # 双方都完成阶段，结束方法
                else:
                    wait1 = visual.TextStim(text=config.text_dict['wait'], win=self.win1, font='Arial Unicode MS',
                                            height=0.05, color='#000000', bold=True)
                    wait1.draw(win=self.win1)
                    self.win1.flip() # 对方还未完成阶段，呈现等待页面
            else: # sub 1 未完成序列
                pass

            if self.next_page_2 and self.current_page[2] <= len(gs_stage[stage])-1: # sub 2 完成序列，未完成阶段
                self.selected_color_index_2, self.selected_shape_index_2 = 0, 0
                self.render_graph(GS=GraphSeries(*gs_stage[stage][self.gs_order[self.current_page[2]]]['uncolored'],
                                                 **gs_stage[stage][self.gs_order[self.current_page[2]]]['colored']), 
                                  win=self.win2)
                self.GS2_copy = GraphSeries(*gs_stage[stage][self.gs_order[self.current_page[2]]]['uncolored'],
                                            **gs_stage[stage][self.gs_order[self.current_page[2]]]['colored'])
                self.render_hud(win=self.win2)
                self.win2.flip()
                self.next_page_2 = False
            elif self.current_page[2] >= len(gs_stage[stage]) : # sub 2 完成阶段
                self.finish_2 = True
                if self.finish_1 == True:
                    return # 双方都完成阶段，结束方法
                else:
                    wait2 = visual.TextStim(text=config.text_dict['wait'], win=self.win2, font='Arial Unicode MS',
                                            height=0.05, color='#000000', bold=True)
                    wait2.draw(win=self.win2)
                    self.win2.flip() # 对方还未完成阶段，呈现等待页面
            else: # sub 2 未完成序列
                pass

            self.operation(stage=stage)
            core.wait(0.01)

    def operation(self,stage:int):
        '''
        图形序列控制。
        - 持续监听 sub1/2 的手柄，更新图形序列的形态。
        - 如果某一方的图形序列填充完毕，则切至下一页（需要记录另一方的状态并无缝衔接）。
        '''
        colors_1 = [i[1] for i in self.GS1_copy.graph_series] #记录所有图形的颜色
        colors_2 = [i[1] for i in self.GS2_copy.graph_series] #记录所有图形的颜色

        self.shape_list_1 = [i[0] for i in self.GS1_copy.graph_series] #仅供计算图形序列长度使用
        self.shape_list_2 = [i[0] for i in self.GS2_copy.graph_series] #仅供计算图形序列长度使用

        states_before_1 = [False] * len(self.js1.getAllButtons()) #此前按键状态列表全部记录为 False
        states_before_2 = [False] * len(self.js2.getAllButtons()) #此前按键状态列表全部记录为 False
        
        while True: #内层循环，负责当前图形序列状态的实时渲染

            states_current_1 = self.js1.getAllButtons()
            states_current_2 = self.js2.getAllButtons()

            # 监听 sub 1 手柄
            if self.finish_1 == False:
                for i, (j, k) in enumerate(zip(states_current_1, states_before_1)): #i:键位，j:当前按键状态，k:此前按键状态 
                    if (j) and (not k): #此前释放，当前按下
                        states_before_1[i] = True #将此前状态 (k) 设为 True
                        if self.js1.get_right_shoulder(): #向右选择图形
                            if self.selected_shape_index_1 < len(self.shape_list_1)-1:
                                self.selected_shape_index_1 += 1
                            else:
                                self.selected_shape_index_1 = 0
                        elif self.js1.get_left_shoulder(): #向左选择图形
                            if self.selected_shape_index_1 > 0:
                                self.selected_shape_index_1 -= 1
                            else:
                                self.selected_shape_index_1 = len(self.shape_list_1)-1
                        elif self.js1.get_a(): #向前选择颜色
                            if self.selected_color_index_1 > 1:
                                self.selected_color_index_1 -= 1
                            else:
                                self.selected_color_index_1 = len(self.color_list)-1
                        elif self.js1.get_b(): #向后选择颜色
                            if self.selected_color_index_1 < len(self.color_list)-1:
                                self.selected_color_index_1 += 1
                            else:
                                self.selected_color_index_1 = 1
                        elif self.js1.get_back(): #检查合法性并染色
                            if self.GS1_copy.graph_series[self.selected_shape_index_1][2] == True:
                                self.GS1_copy.graph_series[self.selected_shape_index_1][1] = self.color_list[self.selected_color_index_1]
                                colors_1 = [i[1] for i in self.GS1_copy.graph_series] #更改GS图形selected_color，并更新颜色列表
                            else:
                                pass
                        elif self.js1.get_left_thumbstick() and (None not in colors_1): #检查是否填完所有颜色，写入，翻页
                            self.record(lable=f'stage{stage}_sub1_gs{self.gs_order[self.current_page[1]]}', 
                                        sub_id=1, gs_id=self.gs_order[self.current_page[1]],
                                        score_total=score.metric(self.GS1_copy,stage=stage)[0],
                                        score_a=score.metric(self.GS1_copy,stage=stage)[1],
                                        score_b=score.metric(self.GS1_copy,stage=stage)[2],
                                        notes='trial finished')
                            self.next_page_1 = True
                            self.score_1.append(score.metric(self.GS1_copy, stage=stage)[0])
                            self.current_page[1] += 1 #让 sub 1 正在观看的页面 index + 1
                            return
                        self.render_graph(self.GS1_copy, win=self.win1)
                        self.render_hud(win=self.win1)
                        self.win1.flip()
                    elif (k) and (not j): #此前按下，当前释放
                        states_before_1[i] = False #将此前状态 (k) 设为 False

            # 监听 sub 2 手柄
            if self.finish_2 == False:
                for i, (j, k) in enumerate(zip(states_current_2, states_before_2)): #i:键位，j:当前按键状态，k:此前按键状态 
                    if (j) and (not k): #此前释放，当前按下。
                        states_before_2[i] = True #将此前状态 (k) 设为 True
                        if self.js2.get_right_shoulder(): #向右选择图形
                            if self.selected_shape_index_2 < len(self.shape_list_2)-1:
                                self.selected_shape_index_2 += 1
                            else:
                                self.selected_shape_index_2 = 0
                        elif self.js2.get_left_shoulder(): #向左选择图形
                            if self.selected_shape_index_2 > 0:
                                self.selected_shape_index_2 -= 1
                            else:
                                self.selected_shape_index_2 = len(self.shape_list_2)-1
                        elif self.js2.get_a(): #向前选择颜色
                            if self.selected_color_index_2 > 1:
                                self.selected_color_index_2 -= 1
                            else:
                                self.selected_color_index_2 = len(self.color_list)-1
                        elif self.js2.get_b(): #向后选择颜色
                            if self.selected_color_index_2 < len(self.color_list)-1:
                                self.selected_color_index_2 += 1
                            else:
                                self.selected_color_index_2 = 1
                        elif self.js2.get_back(): #检查合法性并染色
                            if self.GS2_copy.graph_series[self.selected_shape_index_2][2] == True:
                                self.GS2_copy.graph_series[self.selected_shape_index_2][1] = self.color_list[self.selected_color_index_2]
                                colors_2 = [i[1] for i in self.GS2_copy.graph_series] #更改GS图形selected_color，并更新颜色列表。
                            else:
                                pass
                        elif self.js2.get_left_thumbstick() and (None not in colors_2): #检查是否填完所有颜色，写入，翻页
                            self.record(lable=f'stage{stage}_sub2_gs{self.gs_order[self.current_page[2]]}',
                                        sub_id=2, gs_id=self.gs_order[self.current_page[2]],
                                        score_total=score.metric(self.GS2_copy,stage=stage)[0],
                                        score_a=score.metric(self.GS2_copy,stage=stage)[1],
                                        score_b=score.metric(self.GS2_copy,stage=stage)[2],
                                        notes='trial finished')
                            self.next_page_2 = True
                            self.score_2.append(score.metric(self.GS2_copy, stage=stage)[0])
                            self.current_page[2] += 1 #让 sub 2 正在观看的页面 index + 1
                            return
                        self.render_graph(self.GS2_copy, win=self.win2)
                        self.render_hud(win=self.win2)
                        self.win2.flip()
                    elif (k) and (not j): #此前按下，当前释放
                        states_before_2[i] = False #将此前状态 (k) 设为 False
                
            self.win_flipper.flip()
            core.wait(0.01)
    
    def render_graph(self, GS:GraphSeries, win:visual.Window):
        '''
        在后端渲染交互式页面，包含：图形序列、图形是否可染色（文字）。
        GS: GraphSeries(*uncolored, **colored)类对象。
            *uncolored: 可以自由填色的图形，`shape`。
            **colored: 预先填色的图形，无法更改颜色，shape=`color`。
            GS的参数配置统一写在 config.py 模块中。
        win: 渲染的窗口。
        （该方法仅在 .page_coloring 和 .iohub 中调用，不单独使用。）
        '''
        self.horizon_px = config.res_subjects[0]
        self.vertical_px = config.res_subjects[1]
        hor_total = (len(GS.graph_series)-1)*self.horizon_px/22.5

        self.graph_pos = [(i,0) for i in np.linspace(-hor_total/2, hor_total/2, len(GS.graph_series))]
        text_pos = [(i,-self.vertical_px/18) for i in np.linspace(-hor_total/2, hor_total/2, len(GS.graph_series))]
        # 渲染图形
        for i,j in enumerate(GS.graph_series): # i = index, j = [shape,color,mutable]
            if j[0] == 'cl':
                graph = circle.Circle(win=win, radius=self.horizon_px/60, units='pix', pos=self.graph_pos[i], 
                                      color=GraphSeries.color_param[j[1]], lineColor='#000000')
            else:
                graph = polygon.Polygon(win=win, radius=self.horizon_px/50, units='pix', \
                                        edges=GraphSeries.shape_param[j[0]][0], \
                                        ori=GraphSeries.shape_param[j[0]][1], pos=self.graph_pos[i], 
                                        color=GraphSeries.color_param[j[1]], lineColor='#000000')
            graph.draw(win=win)
        # 渲染图形可否染色文字
        for i,j in enumerate(GS.graph_series):
            if j[2] == False:
                mutable_text = visual.TextStim(win=win, text='固定\n颜色', units='pix', pos=text_pos[i], 
                                               color=GraphSeries.color_param[j[1]], height=18, 
                                               font='Arial Unicode MS', bold=True)
                mutable_text.draw(win=win)
            else:
                pass

    def render_hud(self, win:visual.Window):
        '''
        在后端渲染当前选择状态，包含：测验指导语、选中的图形、选中的颜色。
        （该方法仅在 .page_coloring 和 .iohub 中调用，不单独使用。）
        win: 渲染的窗口。
        '''
        # 设置选区、提示文字颜色当前index
        try:
            selected_shape_index = self.selected_shape_index_1 if win==self.win1 else self.selected_shape_index_2
        except:
            selected_shape_index = 0 #由于render_hud先于iohub调用

        try:
            selected_color_index = self.selected_color_index_1 if win==self.win1 else self.selected_color_index_2
        except:
            selected_color_index = 0 #由于render_hud先于iohub调用

        # 设置提示文字颜色参数
        self.color_list = [None,'r','g','b','y','p']
        
        hud_textcolor_param = {}
        for i,j in GraphSeries.color_param.items():
            hud_textcolor_param[i] = j
        hud_textcolor_param[None] = '#000000' # None的色值与图形不同，其它相同。
        
        # 渲染指导语
        hud_guide = visual.TextStim(win=win, text=config.text_dict['operation_guide'], alignText='left', 
                                    pos=(0,0.5), color='#000000', height=0.05, font='Arial Unicode MS', bold=True)
        hud_guide.draw(win=win)
        # 渲染形状选区
        hud_frame = polygon.Polygon(win=win, radius=self.horizon_px/32, units='pix', 
                                    edges=4, ori=45, color=None, lineColor='#d0d0d0', lineWidth=4, 
                                    pos=self.graph_pos[selected_shape_index])
        hud_frame.draw(win=win)
        # 渲染颜色选择提示
        hud_colortext_dict = {None:'当前未选择颜色','r':'当前已选择：红色','g':'当前已选择：绿色', 
                              'b':'当前已选择：蓝色','y':'当前已选择：黄色','p':'当前已选择：紫色'}
        hud_colortext = visual.TextStim(win=win, text=hud_colortext_dict[self.color_list[selected_color_index]], 
                                        pos=(0,-0.5), color=hud_textcolor_param[self.color_list[selected_color_index]], 
                                        height=0.08, font='Arial Unicode MS', bold=True)
        hud_colortext.draw(win=win)

    def intermezzo(self, intermezzo_name:str):
        '''
        呈现黑底白字的静态页面。
        显式渲染纯黑空屏，持续时间对应静息态扫描或下机学习阶段。
        结束后将窗口重新调整为纯白。
            stage_name: 填入 config.intermezzo_param 中对应的阶段名称，以等待相应时长，并显示相应文本。
        '''
        # 改变窗口颜色
        self.win0.color, self.win1.color, self.win2.color = '#000000', '#000000', '#000000'
        self.win0.flip(), self.win1.flip(), self.win2.flip() # <------ 更新窗口颜色后必须立即刷新窗口，否则不起作用。
        # 呈现文字提示
        text0 = visual.TextStim(win=self.win0, text=config.intermezzo_dict[intermezzo_name][1], 
                                color='#d0d0d0', bold=True, height=0.05, font='Arial Unicode MS')
        text1 = visual.TextStim(win=self.win1, text=config.intermezzo_dict[intermezzo_name][1], 
                                color='#d0d0d0', bold=True, height=0.05, font='Arial Unicode MS')
        text2 = visual.TextStim(win=self.win2, text=config.intermezzo_dict[intermezzo_name][1], 
                                color='#d0d0d0', bold=True, height=0.05, font='Arial Unicode MS')
        text0.draw(), text1.draw(), text2.draw()
        self.win0.flip(), self.win1.flip(), self.win2.flip()
        # 等待特定时长，并更新窗口颜色
        core.wait(config.intermezzo_dict[intermezzo_name][0])
        self.win0.color, self.win1.color, self.win2.color = '#ffffff', '#ffffff', '#ffffff'
        self.win0.flip(), self.win1.flip(), self.win2.flip()

    def page_score(self):
        '''
        展示测验（1）阶段的分数。
        '''
        if sum(self.score_1) > sum(self.score_2):
            win_high, win_low = self.win1, self.win2
            conductor_text = 'sub1 > sub2.'
        else:
            win_high, win_low = self.win2, self.win1
            conductor_text = 'sub1 <= sub2.'

        text = visual.TextStim(win=self.win0, text=conductor_text, pos=(0,0), font='Arial Unicode MS',
                               height=0.05, color='#000000', alignText='center', bold=True, units='norm')
        text_h = visual.TextStim(win=win_high, text=config.text_dict['fake_score_high'], pos=(0,0), font='Arial Unicode MS',
                                 height=0.05, color='#000000', alignText='center', bold=True, units='norm')
        text_l = visual.TextStim(win=win_low, text=config.text_dict['fake_score_low'], pos=(0,0), font='Arial Unicode MS',
                                 height=0.05, color='#000000', alignText='center', bold=True, units='norm')
        text.draw(), text_h.draw(), text_l.draw()
        self.win0.flip(), self.win1.flip(), self.win2.flip()

        while True:
            pressed = self.kb.getKeys()
            if pressed:
                if pressed[-1].name == config.keys_nextpage:
                    self.kb.clearEvents()
                    self.win1.clearBuffer()
                    break
            else:
                core.wait(0.01)
        self.kb.clearEvents()
        return        

    def record(self, lable='NULL', sub_id=0, gs_id=-1, score_total='NULL', score_a='NULL', score_b='NULL', notes='NULL'):
        '''
        将实验数据写入文件，包含 log.txt 中的对应信息，以及实验数据。
            lable: 事件标签。
            notes: 备注内容。
            ...
            结尾自带一个换行符。
        每行内容：'sys_time,exp_num,exp_cfg,gender_sub1,age_sub1,gender_sub2,age_sub2,exp_time,
                  lable,sub_id,gs_id,score_total,score_a,score_b,notes'
        (可在方法内调用，也可以单独调用。)
        '''
        with open(file=self.datafile_path, mode='a', encoding='utf-8') as data:
            data.write(f'{dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")},' +\
                       f'{self.exp_param["exp_num"]},{self.exp_param["exp_config"]},' +\
                       f'{self.sub_param["gender_1"]},{self.sub_param["age_1"]},'+\
                       f'{self.sub_param["gender_2"]},{self.sub_param["age_2"]},'+\
                       f'{format(self.clock.getTime(),".3f")},'+\
                       f'{lable},{sub_id},{gs_id},{score_total},{score_a},{score_b},{notes}\n')

    def finale(self):
        '''
        实验结束。
        关闭窗口、写入结束语句、记录结束阶段时间、退出 PsychoPy。
        '''
        self.intermezzo('end')
        # self.record('end')
        self.win_flipper.close()
        self.win0.close()
        self.win1.close()
        self.win2.close()
        core.quit()

if __name__ == '__main__':

    from flow_dual import launch

    launch()
