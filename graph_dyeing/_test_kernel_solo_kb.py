'''
实验实现的核心方法。\n
主类为 Experiment。
'''

import sys, ctypes, subprocess

import os
import datetime as dt
import numpy as np

from psychopy import gui, core, event, visual, data
from psychopy.visual import circle, polygon 
from psychopy.hardware import keyboard, joystick #如果要用单机实现双人同步输入实验，必须使用手柄。

from graph import GraphSeries
import score
import config

def timer(method):
    '''
    修饰器，记录类方法从调用到结束的时间，并将持续时间写入数据文件。
        method: 类方法，必须具有clock和datafile_path实例属性。
    '''
    def modifier(self, *args, **kwargs):
        start = self.clock.getTime()
        method(self, *args, **kwargs)
        finish = self.clock.getTime()
        with open (self.datafile_path,'a',encoding='utf-8') as data:
            data.write(f'duration = {round(finish-start,2)}\n')
    return modifier

class Experiment:
    '''
    graph.py 模块中定义的基本形状、颜色属性。\n
    shape_order = ['cl','tg','sq','dm','pt'] #任何情况都按照此列表顺序对形状进行排序：圆形-三角-方形-菱形-五边形。
    allowed_shape = {'cl':None,'tg':(3,0),'sq':(4,0),'dm':(4,90),'pt':(5,0)} #除圆形外，其它图形的元组表示边数与旋角。
    allowed_color = {'r':'#d83737','g':'#65C386','b':'#275fe0','y':'#f2b21b','p':'#b29fe0',None:'#ffffff'}
    '''
    exp_existed = []
    sub_existed = []

    with open('log.txt','r',encoding='utf-8') as output:
        # 每行 log.txt 格式：exp_num,sub_num(dyad),datetime
        for i in output:
            exp_existed.append(i.split(',')[0].strip())
            sub_existed.append(i.split(',')[1].strip())

    def __init__(self, monitor=1, sub_scr1=2, sub_scr2=3):
        '''
        预读取显示器分辨率和系统缩放倍数。
            monitor: 0号显示器在系统中的编号，监视器。
            scr1: 1号显示器在系统中的编号，被试机/L。
            scr2: 2号显示器在系统中的编号，被试机/R。
        '''
        self.exp_param = {'exp_num':len(Experiment.exp_existed)+1,'exp_config':[1,2],\
                          'display mode':['full screen','window(1600*900)'], 'input device':['keyboard','joystick']}
        self.sub_param = {'sub_num':0, 'gender':['Female','Male'], 'age':0, 'seat':['请选择','left','right']}

        if sys.platform.startswith('win'):
            ctypes.windll.user32.SetProcessDPIAware()
            LOGPIXELSX = 88
            hdc = ctypes.windll.user32.GetDC(0)
            scaling = ctypes.windll.gdi32.GetDeviceCaps(hdc, LOGPIXELSX)
            ctypes.windll.user32.ReleaseDC(0, hdc)
        else:
            scaling = 65

        disp_bench = visual.Window(fullscr=True, color=(255,255,255))
        self.actual_res = disp_bench.size*scaling/96
        # scaling是需要乘以的系统图形的缩放倍数，但由于Windows和macOS的系统api不一致，故暂时搁置，以后添加macOS的分支。
        self.horizon_px = self.actual_res[0]
        self.vertical_px = self.actual_res[1]

        self.stage_record = {'launch':[False,0], 'rest_1':[False,0], 'intr_1':[False,0], 'try':[False,0],
                             'indv_1':[False,0], 'coop_1':[False,0], 'test_1':[False,0],
                             'rest_2':[False,0], 'intr_2':[False,0],
                             'indv_2':[False,0], 'coop_2':[False,0], 'test_2':[False,0],
                             'end':[False,0]} #格式：{阶段:[是否完成，完成时间（相对时间）]}

        core.wait(0.5)
        disp_bench.close()

    def overture(self):
        '''
        提示输入实验与被试信息。
        创建实验窗口，写入日志，实例化i/o，并创建实验数据文件。
        '''
        while True:
            self.exp_info = gui.DlgFromDict(title='[step 1/2] info_log',
                                            dictionary=self.exp_param, order=self.exp_param.keys())
            self.sub_info = gui.DlgFromDict(title='[step 2/2] info_log',
                                            dictionary=self.sub_param, order=self.sub_param.keys())
            if self.exp_info.OK == False or self.sub_info.OK == False:
                print ('实验中止，原因：基本信息录入阶段中止。')
                core.quit()
                break
            elif not (isinstance(self.exp_param['exp_num'],int) and 
                      isinstance(self.sub_param['sub_num'],int) and isinstance(self.sub_param['age'],int)):
                print ('无效信息：错误的被试信息参数（被试号或年龄）。')
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
            elif str(self.sub_param['sub_num']) in Experiment.sub_existed:
                warning = gui.Dlg(title='警告：重复的被试编号。')
                warning.addText('警告：此被试编号已存在于其它实验数据中。是否继续？')
                warning.show()
                if warning.OK:
                    Experiment.exp_existed.append(self.exp_param['exp_num'])
                    Experiment.sub_existed.append(self.sub_param['sub_num'])
                    break
                else:
                    core.quit()
            # elif self.sub_param['seat'] == '请选择':
            #     warning = gui.Dlg(title='警告：未选择座位信息。')
            #     warning.addField('警告：未选择座位信息（L/R），请按照实际就坐情况选择。')
            #     warning.show()
            else:
                Experiment.exp_existed.append(self.exp_param['exp_num'])
                Experiment.sub_existed.append(self.sub_param['sub_num'])
                break

        with open('log.txt','a',encoding='utf-8') as log:
            # 创建一个log文件，仅供记录实验启动参数。
            log_info = f'{self.exp_param["exp_config"]}' + ',' +  f'{self.exp_param["exp_num"]}' + ',' + \
                       f'{self.sub_param["sub_num"]}' + ',' + f'{self.sub_param["gender"]}' + ',' +\
                       f'{self.sub_param["age"]}' + ',' + f'{self.sub_param["seat"]}' + ',' +\
                       f'{dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n'
            log.write(log_info)

        exp_num = self.exp_param['exp_num']
        exp_cfg = self.exp_param['exp_config']
        sub_seat = self.sub_param['seat']
        sub_dir = os.path.join(os.getcwd(), 'datafile_solo')
        datafile_name = f'{exp_cfg}_{exp_num}_{sub_seat}.txt'
        self.datafile_path = os.path.join(sub_dir, datafile_name)
        with open(self.datafile_path, 'a', encoding='utf-8') as data:
            pass #创建一个data文件。

        # self.win = visual.Window(size=self.actual_res if self.exp_param['display mode']=='full screen' else (1366,768),
        #                          allowGUI=False if self.exp_param['display mode']=='full screen' else True,
        #                          color='#ffffff')
        self.win = visual.Window(size=config.res_conductor if self.exp_param['display mode']=='full screen' else (1600,900),
                                 allowGUI=False if self.exp_param['display mode']=='full screen' else True,
                                 color='#ffffff')

        self.kb = keyboard.Keyboard()
        self.clock = core.Clock()

    @timer
    def page_text(self, t_text='var not defined', t_pos=(0,0), t_height=0.05, t_color='#000000',
                  t_align='center', t_units = 'norm', stage_name='text', 
                  allowed_keys=config.keys_nextpage, min_time=3):
        '''
        呈现静态文本页面。
        (1)
        在后端渲染静态文本，并在前台显式渲染。
            t_text: 文本内容，统一写在 config.py 模块中。
            stage_name: 记录在 datafile.txt 中时间属性的字段。
            默认中心、居中、纯黑。
        (2)
        翻页键检测：等待接受键盘输入，并更新 self.pressed。
        按键列表统一写在 config.py 模块中。
            allowed_keys: 接受的按键列表。
            min_time: 按键生效前的等待时间。
            stage_name: 记录在 datafile.txt 中时间属性的字段。
        (该方法带有对 .flip() 方法的调用，所以只适用于只包含静态文本的页面，不要在其它函数内调用。)
        '''
        text = visual.TextStim(win=self.win, text=t_text, pos=t_pos, font='Arial Unicode MS',
                               height=t_height, color=t_color, alignText=t_align, bold=True, units=t_units)
        text.draw()
        self.win.flip()
        self.write_data(f'{stage_name},{self.clock.getTime()}')
        core.wait(min_time)
        self.kb.clearEvents()

        while True:
            pressed = self.kb.getKeys()
            if pressed:
                if pressed[-1].name == allowed_keys:
                    self.kb.clearEvents()
                    self.win.clearBuffer()
                    break
            else:
                core.wait(0.001)
        self.kb.clearEvents()
        return

    @timer
    def page_operation(self, GS:type=GraphSeries, stage:type=int):
        '''
        呈现填色交互页面。
        操作键检测：等待接受键盘输入，并更新 self.pressed 和后端绘制的图形。
        按键列表统一写在 config.py 模块中。
            gs: Graph_Series 类对象。
            stage: 实验测验阶段（0/1/2）。
        '''
        self.color_list = [None,'r','g','b','y','p']
        self.shape_list = [i[0] for i in GS.graph_series]
        self.selected_color_index = 0
        self.selected_shape_index = 0
        # self.graph_series 列表元素格式：[shape, color, mutable]
        # config.keys_operation = ['1','2','3','4','5','minus','equal','space','return']
        colors = [i[1] for i in GS.graph_series] #记录所有图形的颜色

        self.kb.clearEvents()
        self.render_graph(GS)
        self.render_hud()
        self.win.flip()

        while True: #根据按键重新渲染当前图形
            pressed = self.kb.getKeys(keyList=config.keys_operation)
            if pressed:
                if pressed[-1].name in config.keys_color_picker: #选择颜色
                    if pressed[-1] == config.keys_color_picker['down']: #向下选择
                        if self.selected_color_index < len(self.color_list) - 1:
                            self.selected_color_index += 1
                        else:
                            self.selected_color_index = 1
                    elif pressed[-1] == config.keys_color_picker['up']: #向上选择
                        if self.selected_color_index > 1:
                            self.selected_color_index -= 1
                        else:
                            self.selected_color_index = len(self.color_list) - 1
                elif pressed[-1].name in config.keys_shape_picker.values(): #选择形状
                    if pressed[-1] == config.keys_shape_picker['right']: ##向右选择
                        if self.selected_shape_index < len(self.shape_list) - 1:
                            self.selected_shape_index += 1
                        else:
                            self.selected_shape_index = 0
                    elif pressed[-1].name == config.keys_shape_picker['left']: ##向左选择
                        if self.selected_shape_index > 0:
                            self.selected_shape_index -= 1
                        else:
                            self.selected_shape_index = len(self.shape_list) - 1
                elif pressed[-1].name == config.keys_coloring: #检查能否填色并填入颜色
                    if GS.graph_series[self.selected_shape_index][2] == True:
                        GS.graph_series[self.selected_shape_index][1] = self.color_list[self.selected_color_index]
                        colors = [i[1] for i in GS.graph_series] #更改GS图形selected_color，并更新颜色列表。
                    else:
                        pass
                elif (pressed[-1].name == config.keys_nextpage) and (None not in colors): #检查是否全部填色并翻页
                    self.kb.clearEvents()
                    self.win.clearBuffer()
                    self.win.flip()
                    self.write_data(f'{(score.metric(GS,stage))}')
                    break
                else:
                    pass                
                self.render_graph(GS)
                self.render_hud()
                self.win.flip()
            else:
                core.wait(0.01)
        return
    
    def render_graph(self, GS:type=GraphSeries):
        '''
        在后端渲染交互式页面，包含：图形序列、图形是否可染色（文字）。
        GS: GraphSeries(*uncolored, **colored)类对象。
            *uncolored: 可以自由填色的图形，`shape`。
            **colored: 预先填色的图形，无法更改颜色，shape=`color`。
        GS的参数配置统一写在 config.py 模块中。
        （该方法仅在 .page_operation 中调用，不单独使用。）
        '''
        # GS.graph_series 元素格式：[形状shape, 颜色color, 可否染色True/False]

        hor_total = (len(GS.graph_series)-1)*self.horizon_px/22.5

        self.graph_pos = [(i,0) for i in np.linspace(-hor_total/2, hor_total/2, len(GS.graph_series))]
        text_pos = [(i,-self.vertical_px/18) for i in np.linspace(-hor_total/2, hor_total/2, len(GS.graph_series))]

        # 渲染图形
        for i,j in enumerate(GS.graph_series): # i = index, j = [shape,color,mutable]
            if j[0] == 'cl':
                graph = circle.Circle(self.win, radius=self.horizon_px/60, units='pix', pos=self.graph_pos[i], 
                                      color=GraphSeries.color_param[j[1]], lineColor='#000000')
            else:
                graph = polygon.Polygon(self.win, radius=self.horizon_px/50, units='pix', \
                                        edges=GraphSeries.shape_param[j[0]][0], \
                                        ori=GraphSeries.shape_param[j[0]][1], pos=self.graph_pos[i], 
                                        color=GraphSeries.color_param[j[1]], lineColor='#000000')
            graph.draw()

        # 渲染图形可否染色文字
        for i,j in enumerate(GS.graph_series):
            if j[2] == False:
                mutable_text = visual.TextStim(win=self.win, text='固定\n颜色', units='pix', pos=text_pos[i], 
                                               color=GraphSeries.color_param[j[1]], height=18, 
                                               font='Arial Unicode MS', bold=True)
                mutable_text.draw()
            else:
                pass

    def render_hud(self):
        '''
        在后端渲染当前选择状态，包含：测验指导语、选中的图形、选中的颜色。
        （该方法仅在 .page_operation 中调用，不单独使用。）
        '''
        hud_textcolor_param = {}
        for i,j in GraphSeries.color_param.items():
            hud_textcolor_param[i] = j
        hud_textcolor_param[None] = '#000000' # None的色值与图形不同，其它相同。

        # 渲染指导语
        hud_guide = visual.TextStim(win=self.win, text=config.text_dict['operation_guide'], alignText='left', 
                                    pos=(0,0.5), color='#000000', height=0.05, font='Arial Unicode MS', bold=True)
        hud_guide.draw()

        # 渲染形状选区
        hud_frame = polygon.Polygon(self.win, radius=self.horizon_px/32, units='pix', 
                                    edges=4, ori=45, color=None, lineColor='#d0d0d0', lineWidth=4, 
                                    pos=self.graph_pos[self.selected_shape_index])
        hud_frame.draw()

        # 渲染颜色选择提示
        hud_colortext_dict = {None:'当前未选择颜色','r':'当前已选择：红色','g':'当前已选择：绿色', 
                              'b':'当前已选择：蓝色','y':'当前已选择：黄色','p':'当前已选择：紫色'}
        hud_colortext = visual.TextStim(win=self.win, text=hud_colortext_dict[self.color_list[self.selected_color_index]], 
                                        pos=(0,-0.5), color=hud_textcolor_param[self.color_list[self.selected_color_index]], 
                                        height=0.05, font='Arial Unicode MS', bold=True)
        hud_colortext.draw()

    @timer
    def intermezzo(self, intermezzo_name:type=str):
        '''
        呈现黑底白字的静态页面。
        显式渲染纯黑空屏，持续时间对应静息态扫描或下机学习阶段。
        结束后将窗口重新调整为纯白。
            stage_name: 填入config.intermezzo_param中对应的阶段名称，以等待相应时长，并显示相应文本。
        '''
        # 改变窗口颜色
        self.win.clearBuffer()
        self.win.color = '#000000'
        self.win.flip() # <------ 更新窗口颜色后必须立即刷新窗口，否则不起作用。
        # 呈现文字提示
        text = visual.TextStim(win=self.win, text=config.intermezzo_dict[intermezzo_name][1], 
                               color='#d0d0d0', bold=True, height=0.05, font='Arial Unicode MS')
        text.draw()
        self.win.flip()
        # 等待特定时长，并更新窗口颜色
        core.wait(config.intermezzo_dict[intermezzo_name][0])
        self.win.clearBuffer()
        self.win.color = '#ffffff'
        self.win.flip()

    def record(self, stage_name:type=str):
        '''
        在 self.stage 中记录已完成的阶段及其实验内时间。
        '''
        self.stage_record[stage_name] = (True, self.clock.getTime())

    def write_data(self, content:type=str):
        '''
        将实验数据写入文件，包含 log.txt 中的对应信息，以及实验数据。
            content: 写入的数据，末位自带一个换行符。
        (可在方法内调用，也可以单独调用。)
        '''
        with open(self.datafile_path, 'a', encoding='utf-8') as data:
            data.write(f'{content}\n')

    def finale(self):
        '''
        实验结束。
        关闭窗口、写入结束语句、记录结束阶段时间、退出 PsychoPy。
        '''
        self.intermezzo('end')
        self.win.close()
        self.write_data('实验正常完成，未报错。')
        self.record('end')
        core.quit()

if __name__ == '__main__':

    from _test_flow_solo_kb import launch

    launch()

