
import os
import numpy as np

from PIL import Image
from config import config

from psychopy import visual
from psychopy.visual import rect, polygon, TextBox2

class dualWin:
    '''
    图形化的双人实验窗口。
    各方法的参数只影响两个窗口中的图形渲染，不负责任何逻辑处理。
    所有方法内部均调用了 .flip()。
    '''

    def __init__(
            self, 
            size_win:tuple[int,int],
            pos_win0:tuple[int,int], pos_win1:tuple[int,int],
            bg_color:str=config.color_set['bg_gray'],
            fullscreen:bool=False, allow_gui:bool=False
            ):

        self.win0 = visual.Window(color=bg_color, screen=0, size=size_win, 
                                  fullscr=fullscreen, allowGUI=allow_gui, pos=pos_win0)
        self.win1 = visual.Window(color=bg_color, screen=1, size=size_win, 
                                  fullscr=fullscreen, allowGUI=allow_gui, pos=pos_win1)

        self.win_size = size_win
        self.win_ratio = size_win[0] / size_win[1]

        self.highlight_color = {0:config.color_set['B'], 
                                1:config.color_set['Y']}



    def text(
            self, 
            text_0:str, text_1:str,
            pos:tuple=(0,0), align:str='left', boxsize:tuple=(1.5,1.5),
            color:str=config.color_set['black'], textsize:int=config.size['text']
            ) -> None:
        '''
        渲染【两个窗口】的纯文本，在外部控制跳转逻辑。
        - text_0/1: 文本内容；若为 None 则不对该被试窗口调用 .flip()。
        '''

        if text_0:
            stim_0 = TextBox2(
                win=self.win0, text=text_0, lineBreaking='uax14',
                pos=pos, size=boxsize, alignment=align, color=color, bold=True,
                font=config.font['CN'], letterHeight=textsize, lineSpacing=1,
                units='norm', editable=False
                )
            stim_0.draw(), self.win0.flip()
        if text_1:
            stim_1 = TextBox2(
                win=self.win1, text=text_1, lineBreaking='uax14',
                pos=pos, size=boxsize, alignment=align, color=color, bold=True,
                font=config.font['CN'], letterHeight=textsize, lineSpacing=1,
                units='norm', editable=False)
            stim_1.draw(), self.win1.flip()



    def Ready_text(
            self, 
            text_0:str, text_1:str, 
            ready_0:bool, ready_1:bool
            ) -> None:
        '''
        渲染【两个窗口】的准备页面。
        - text_0/1: 分别显示在 win0/win1 的准备文本。
        - ready_0/1: 被试是否已按键准备。
        '''

        stim_0 = TextBox2(
            win=self.win0, text=text_0, lineBreaking='uax14',
            pos=(0, 0), alignment='center', 
            font=config.font['CN'], bold=True, 
            letterHeight=config.size['text'], units='norm',
            color=config.color_set['black']
            )
        stim_1 = TextBox2(
            win=self.win1, text=text_1, lineBreaking='uax14',
            pos=(0, 0), alignment='center',
            font=config.font['CN'], bold=True,
            letterHeight=config.size['text'], units='norm',
            color=config.color_set['black']
            )
        stim_0.draw(), stim_1.draw()

        if ready_0:
            sub0_self = TextBox2(
                win=self.win0, text=config.text['ready_self'], 
                pos=config.pos['ready_self'], alignment='center',
                font=config.font['CN'], bold=True,
                letterHeight=config.size['text_large'], units='norm', 
                color=self.highlight_color[0]
            )
            sub1_ally = TextBox2(
                win=self.win1, text=config.text['ready_ally'], 
                pos=config.pos['ready_ally'], alignment='center',
                font=config.font['CN'], bold=True,
                letterHeight=config.size['text_large'], units='norm', 
                color=self.highlight_color[0]
            )
            sub0_self.draw(), sub1_ally.draw()
        if ready_1:
            sub0_ally = TextBox2(
                win=self.win0, text=config.text['ready_ally'], 
                pos=config.pos['ready_ally'], alignment='center',
                font=config.font['CN'], bold=True,
                letterHeight=config.size['text_large'], units='norm', 
                color=self.highlight_color[1]
                )
            sub1_self = TextBox2(
                win=self.win1, text=config.text['ready_self'], 
                pos=config.pos['ready_self'], alignment='center',
                font=config.font['CN'], bold=True,
                letterHeight=config.size['text_large'], units='norm',
                color=self.highlight_color[1])
            sub0_ally.draw(), sub1_self.draw()
        
        self.win0.flip(), self.win1.flip()



    def pic(self, pic_0:str, pic_1:str) -> None:
        '''
        渲染【两个窗口】的图像，在外部控制跳转逻辑。
        - pic_0/pic_1: 图像文件名，位于 image 目录；若为 None 则不对该被试窗口调用 .flip()
        '''
        def _render_pic(pic:str, win) -> None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            filepath = os.path.join(script_dir, 'image', pic)
            with Image.open(filepath) as img:
                ratio_pic = img.size[0] / img.size[1]
            if ratio_pic >= self.win_ratio:  # 横向填满
                pic_x = self.win_size[0]
                pic_y = int(img.size[1] * pic_x / img.size[0])
            else:  # 纵向填满
                pic_y = self.win_size[1]
                pic_x = int(img.size[0] * pic_y / img.size[1])
            stim = visual.ImageStim(
                image=filepath, size=(pic_x, pic_y),
                units='pix', win=win
            )
            stim.draw(), win.flip()

        if pic_0:
            _render_pic(pic=pic_0, win=self.win0)
        if pic_1:
            _render_pic(pic=pic_1, win=self.win1)



    def Ready_pic(
            self, 
            pic_0:str, pic_1:str,
            ready_0:bool, ready_1:bool
            ) -> None:
        '''
        渲染【两个窗口】的准备页面（图片版本）。
        - pic_0/pic_1: 图片文件名，位于 image 目录。
        - ready_0/1: 被试是否已按键准备。
        '''

        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path_0 = os.path.join(script_dir, 'image', pic_0)
        file_path_1 = os.path.join(script_dir, 'image', pic_1)

        with Image.open(file_path_0) as img0:
            ratio_pic0 = img0.size[0] / img0.size[1]
        with Image.open(file_path_1) as img1:
            ratio_pic1 = img1.size[0] / img1.size[1]
        if ratio_pic0 >= self.win_ratio:
            pic0_x = self.win_size[0]
            pic0_y = int(img0.size[1] * pic0_x / img0.size[0])
        else:
            pic0_y = self.win_size[1]
            pic0_x = int(img0.size[0] * pic0_y / img0.size[1])
        if ratio_pic1 >= self.win_ratio:
            pic1_x = self.win_size[0]
            pic1_y = int(img1.size[1] * pic1_x / img1.size[0])
        else:
            pic1_y = self.win_size[1]
            pic1_x = int(img1.size[0] * pic1_y / img1.size[1])
        stim_1 = visual.ImageStim(
            image=file_path_1, size=(pic1_x, pic1_y),
            units='pix', win=self.win1
        )
        stim_0 = visual.ImageStim(
            image=file_path_0, size=(pic0_x, pic0_y),
            units='pix', win=self.win0
        )
        stim_0.draw(), stim_1.draw()

        if ready_0:
            sub0_self = TextBox2(
                win=self.win0, text=config.text['confirm_self'], 
                pos=config.pos['confirm_self'], alignment='center',
                font=config.font['CN'], bold=True,
                letterHeight=config.size['text_large'], units='norm', 
                color=self.highlight_color[0]
            )
            sub1_ally = TextBox2(
                win=self.win1, text=config.text['confirm_ally'], 
                pos=config.pos['confirm_ally'], alignment='center',
                font=config.font['CN'], bold=True,
                letterHeight=config.size['text_large'], units='norm', 
                color=self.highlight_color[0]
            )
            sub0_self.draw(), sub1_ally.draw()
        if ready_1:
            sub0_ally = TextBox2(
                win=self.win0, text=config.text['confirm_ally'], 
                pos=config.pos['confirm_ally'], alignment='center',
                font=config.font['CN'], bold=True,
                letterHeight=config.size['text_large'], units='norm', 
                color=self.highlight_color[1]
            )
            sub1_self = TextBox2(
                win=self.win1, text=config.text['confirm_self'], 
                pos=config.pos['confirm_self'], alignment='center',
                font=config.font['CN'], bold=True,
                letterHeight=config.size['text_large'], units='norm',
                color=self.highlight_color[1]
            )
            sub0_ally.draw(), sub1_self.draw()

        self.win0.flip(), self.win1.flip()



    def fixation(self, size:float=config.size['fixation']) -> None:
        '''
        渲染【两个窗口】的十字形注视点。
        - size: 注视点的大小，单位为 norm。
        '''

        fixation_0 = TextBox2(
            win=self.win0, text='+', lineBreaking='uax14', 
            pos=(0, 0), alignment='center', color=config.color_set['black'], bold=True,
            font=config.font['CN'], letterHeight=size, lineSpacing=1, 
            units='norm', editable=False
        )
        fixation_1 = TextBox2(
            win=self.win1, text='+', lineBreaking='uax14', 
            pos=(0, 0), alignment='center', color=config.color_set['black'], bold=True,
            font=config.font['CN'], letterHeight=size, lineSpacing=1, 
            units='norm', editable=False
        )
        fixation_0.draw(), fixation_1.draw()
        self.win0.flip(), self.win1.flip()



    def stim(
            self,
            blackRatio_sub0:list[float],
            blackRatio_sub1:list[float],
            rect_num:int=config.rect_num['rect_num'],
            show_mark:bool=True,
            whole_rect_w:float=config.size['rect'][0],
            whole_rect_h:float=config.size['rect'][1],
            whole_rect_color=config.color_set['white'],
            black_rect_color=config.color_set['black'],
            draw_range_x:tuple[float, float]=config.pos['stim_rect_x'],
            ) -> None:
        '''
        渲染【两个窗口】的刺激（根据传入的数组自动计算矩形数量、横向位置）。
        - rect_num: 矩形的数量。
        - show_mark: 是否显示辅助标记。
        - black_rect_ratio_sub0/1: 黑色矩形的比例数组。
        - whole_rect_h: 单个矩形的高度。
        - whole_rect_w: 单个矩形的宽度。
        - whole_rect_color: 背景矩形的颜色。
        - black_rect_color: 黑色矩形的颜色。
        - draw_range_x: 刺激绘制区域的范围（横向）。
        '''

        rect_num_sub0 = rect_num
        rect_num_sub1 = rect_num
        rect_pos_x_sub0 = np.linspace(draw_range_x[0], draw_range_x[1], rect_num_sub0)
        rect_pos_x_sub1 = np.linspace(draw_range_x[0], draw_range_x[1], rect_num_sub1)
        whole_pos_y = 0
        black_pos_y_sub0 = [(i - whole_rect_h) / 2 for i in blackRatio_sub0]
        black_pos_y_sub1 = [(i - whole_rect_h) / 2 for i in blackRatio_sub1]

        rects_whole_sub0 = []
        rects_black_sub0 = []
        rects_markL_sub0 = []
        rects_markR_sub0 = []

        rects_whole_sub1 = []
        rects_black_sub1 = []
        rects_markL_sub1 = []
        rects_markR_sub1 = []

        for i in range(rect_num_sub0):
            rects_whole_sub0.append(
                rect.Rect(
                    win=self.win0,
                    width=whole_rect_w, height=whole_rect_h,
                    pos=(rect_pos_x_sub0[i], whole_pos_y),
                    fillColor=whole_rect_color, lineColor=None
                    )
            )
            rects_black_sub0.append(
                rect.Rect(
                    win=self.win0,
                    width=whole_rect_w, height=whole_rect_h*blackRatio_sub0[i],
                    pos=(rect_pos_x_sub0[i], black_pos_y_sub0[i]),
                    fillColor=black_rect_color, lineColor=None
                    )
            )
        for i in range(rect_num_sub1):
            rects_whole_sub1.append(
                rect.Rect(
                    win=self.win1,
                    width=whole_rect_w, height=whole_rect_h,
                    pos=(rect_pos_x_sub1[i], whole_pos_y),
                    fillColor=whole_rect_color, lineColor=None
                    )
            )
            rects_black_sub1.append(
                rect.Rect(
                    win=self.win1,
                    width=whole_rect_w, height=whole_rect_h*blackRatio_sub1[i],
                    pos=(rect_pos_x_sub1[i], black_pos_y_sub1[i]),
                    fillColor=black_rect_color, lineColor=None
                    )
            )

        for i in range(len(config.pos['stim_markL'])):
            rects_markL_sub0.append(
                rect.Rect(win=self.win0, 
                          width=config.size['stim_mark'][0], height=config.size['stim_mark'][1],
                          pos=config.pos['stim_markL'][i],
                          fillColor=config.color_set['stim_mark'][i], lineColor=None)
            )
        for i in range(len(config.pos['stim_markR'])):
            rects_markR_sub0.append(
                rect.Rect(win=self.win0, 
                          width=config.size['stim_mark'][0], height=config.size['stim_mark'][1],
                          pos=config.pos['stim_markR'][i],
                          fillColor=config.color_set['stim_mark'][i], lineColor=None)
            )
        for i in range(len(config.pos['stim_markL'])):
            rects_markL_sub1.append(
                rect.Rect(win=self.win1, 
                          width=config.size['stim_mark'][0], height=config.size['stim_mark'][1],
                          pos=config.pos['stim_markL'][i],
                          fillColor=config.color_set['stim_mark'][i], lineColor=None)
            )
        for i in range(len(config.pos['stim_markR'])):
            rects_markR_sub1.append(
                rect.Rect(win=self.win1, 
                          width=config.size['stim_mark'][0], height=config.size['stim_mark'][1],
                          pos=config.pos['stim_markR'][i],
                          fillColor=config.color_set['stim_mark'][i], lineColor=None)
            )
        rects_markL_sub0[6].width *= 2
        rects_markR_sub0[6].width *= 2
        rects_markL_sub0[6].pos = (-0.325, 0.0)
        rects_markR_sub0[6].pos = (0.325, 0.0)
        rects_markL_sub1[6].width *= 2
        rects_markR_sub1[6].width *= 2
        rects_markL_sub1[6].pos = (-0.325, 0.0)
        rects_markR_sub1[6].pos = (0.325, 0.0)

        for rect_whole, rect_black in zip(rects_whole_sub0, rects_black_sub0):
            rect_whole.draw(), rect_black.draw()
        for rect_whole, rect_black in zip(rects_whole_sub1, rects_black_sub1):
            rect_whole.draw(), rect_black.draw()
        if show_mark:
            for i, j in zip(rects_markL_sub0, rects_markR_sub0):
                i.draw(), j.draw()
            for i, j in zip(rects_markL_sub1, rects_markR_sub1):
                i.draw(), j.draw()

        self.win0.flip(), self.win1.flip()
        


    def private_report(self, report_mode:str, 
                       subject:int, scale:int, finish:bool) -> None:
        '''
        渲染【单个窗口】的单人报告页面，同时适用于 dual 和 solo 阶段。
        - report_mode: 报告模式，'confidence' 或 'ratio'。
        - subject: 被试编号（0 / 1）。
        - scale: 该被试当前的选择尺度（[-6,-1]∪[+1,+6]=已选择，0=未选择）。
        - finish: 是否完成选择。
        '''

        map_win = {0:self.win0, 1:self.win1}
        map_title = {'confidence':config.text['title_private_confidence'], 
                     'ratio':config.text['title_private_ratio']}
        map_pointer_rotation = {0: 180, 1: 0}

        mark_pos_x_array = np.linspace(config.pos['report_scale_x'][0], config.pos['report_scale_x'][1], 13)
        mark_pos_x_array = np.delete(mark_pos_x_array, 6) #删除中间留给纵坐标的位置
        choice_keys = list(range(-6, 0)) + list(range(1, 7))
        mark_pos_x = {k: v for k, v in zip(choice_keys, mark_pos_x_array)}

        # 静态对象：标题、标尺、刻度、坐标轴文字、按键提示
        title = TextBox2(
            win=map_win[subject], text=map_title[report_mode], 
            pos=config.pos['report_title'], alignment='center', 
            lineBreaking='uax14',
            font=config.font['CN'], bold=True, 
            letterHeight=config.size['text'], units='norm', 
            color=config.color_set['black'], 
        )
        line = rect.Rect(
            win=map_win[subject],
            width=config.size['axis_hori'][0],
            height=config.size['axis_hori'][1],
            pos=(0, config.pos['report_scale_y']),
            fillColor=config.color_set['black'], lineColor=None
            )
        dvid = rect.Rect(
            win=map_win[subject], 
            width=config.size['axis_vert'][0],
            height=config.size['axis_vert'][1],
            pos=(0, config.pos['report_scale_y']),
            fillColor=config.color_set['black'], lineColor=None
        )
        mark = [rect.Rect(
            win=map_win[subject],
            width=config.size['report_mark'][0],
            height=config.size['report_mark'][1],
            pos=(mark_pos_x[i], config.pos['report_scale_y']),
            fillColor=config.color_set['black'], lineColor=None) \
                for i in choice_keys]
        scale_text_left = TextBox2(
            win=map_win[subject], text=config.text['scale_text_w'], 
            pos=config.pos['report_scale_text']['w'], alignment='center', 
            font=config.font['CN'], bold=True, 
            letterHeight=config.size['text'], units='norm', 
            color=config.color_set['white'], 
        )
        scale_text_right = TextBox2(
            win=map_win[subject], text=config.text['scale_text_b'], 
            pos=config.pos['report_scale_text']['b'], alignment='center', 
            font=config.font['CN'], bold=True, 
            letterHeight=config.size['text'], units='norm', 
            color=config.color_set['black'], 
        )
        tips = TextBox2(
            win=map_win[subject], text=config.text['tips_private'], 
            pos=config.pos['report_tips'], alignment='center', 
            font=config.font['CN'], bold=True, 
            letterHeight=config.size['text_small'], units='norm', 
            color=config.color_set['black']
        )
        scale_text_left.draw(), scale_text_right.draw()
        title.draw(), line.draw(), dvid.draw()
        tips.draw()
        for _ in mark:
            _.draw()

        # 动态对象：指针、指针文字、当前选择
        if scale != 0:
            pointer = polygon.Polygon(
                win=map_win[subject], edges=3, 
                ori=map_pointer_rotation[subject], 
                pos=(mark_pos_x[scale], config.pos['report_pointer_y'][subject]), 
                size=config.size['pointer'], 
                fillColor=self.highlight_color[subject], lineColor=None
                )
            pointerText = TextBox2(
                win=map_win[subject], text=config.report_value[report_mode][scale], 
                pos=(mark_pos_x[scale], config.pos['report_pointer_text_y'][subject]), alignment='center', 
                font=config.font['CN'], bold=True, 
                letterHeight=config.size['text'], units='norm', 
                color=self.highlight_color[subject], 
                )
            if finish:
                choice_text = TextBox2(
                    win=map_win[subject], text=config.text['wait_ally'],
                    pos=config.pos['report_choice'], alignment='center', 
                    font=config.font['CN'], bold=True, 
                    letterHeight=config.size['text_large'], units='norm', 
                    color=self.highlight_color[subject], 
                )
            else:
                choice_text = TextBox2(
                    win=map_win[subject], text=config.text['choice_w'] if scale<0 else config.text['choice_b'],
                    pos=config.pos['report_choice'], alignment='center', 
                    font=config.font['CN'], bold=True, 
                    letterHeight=config.size['text_large'], units='norm', 
                    color=self.highlight_color[subject], 
                )
            pointer.draw(), pointerText.draw()
            choice_text.draw()
        else:
            choice_text = TextBox2(
                    win=map_win[subject], text=config.text['choice_None'],
                    pos=config.pos['report_choice'], alignment='center', 
                    font=config.font['CN'], bold=True, 
                    letterHeight=config.size['text_large'], units='norm', 
                    color=self.highlight_color[subject], 
                    )
            choice_text.draw()
            
        map_win[subject].flip()



    def public_report(self, report_mode:str, same_choice:bool, 
                      scale_0:int, scale_1:int, 
                      host_subject:int, wait_subject:int, 
                      host_choice:str|bool=None) -> None:
        '''
        渲染【两个窗口】的联合报告页面，只适用于 dual 阶段。
        （方法内部自动处理双方选择相同 / 不同的情况。）
        - report_mode: 报告模式，'confidence' 或 'ratio'。
        - same_choice: 双方是否做出相同选择（由方法外部传入）。
        - scale_0: 被试 0 的选择尺度（具体报告的 confidence 或 ratio 的选项代理值，None = 未选择）。
        - scale_1: 被试 1 的选择尺度（具体报告的 confidence 或 ratio 的选项代理值，None = 未选择）。
        - host_subject: 由哪一个被试进行最终判断（0/1）。
        - wait_subject: 等待对方进行最终判断的被试（0/1）。
        - host_choice: host 被试当前的选择（None=未选择，'b'/'w'）。
        '''

        mark_pos_x_array = np.linspace(config.pos['report_scale_x'][0], config.pos['report_scale_x'][1], 13)
        mark_pos_x_array = np.delete(mark_pos_x_array, 6) #删除中间留给纵坐标的位置
        choice_keys = list(range(-6, 0)) + list(range(1, 7))
        mark_pos_x = {k: v for k, v in zip(choice_keys, mark_pos_x_array)}

        map_win = {0:self.win0, 1:self.win1}
        map_choice_text = {'w':config.text['choice_public_w'], 
                           'b':config.text['choice_public_b'], 
                           None:config.text['choice_None']}
        map_choice_color = {'w':config.color_set['white'], 
                            'b':config.color_set['black']}
        map_pointer_rotation = {0:180, 1:0}

        # 静态对象：标题、标尺、刻度
        title_0 = TextBox2(
            win=self.win0, 
            text=config.text['title_public_same'] if same_choice else config.text['title_public_diff'], 
            pos=config.pos['report_title'], alignment='center', 
            lineBreaking='uax14',
            font=config.font['CN'], bold=True, 
            letterHeight=config.size['text'], units='norm', 
            color=config.color_set['black']
            )
        title_1 = TextBox2(
            win=self.win1, 
            text=config.text['title_public_same'] if same_choice else config.text['title_public_diff'], 
            pos=config.pos['report_title'], alignment='center', 
            lineBreaking='uax14',
            font=config.font['CN'], bold=True, 
            letterHeight=config.size['text'], units='norm', 
            color=config.color_set['black']
            )
        line_0 = rect.Rect(
            win=self.win0,
            width=config.size['axis_hori'][0],
            height=config.size['axis_hori'][1],
            pos=(0, config.pos['report_scale_y']),
            fillColor=config.color_set['black'], lineColor=None
            )
        line_1 = rect.Rect(
            win=self.win1,
            width=config.size['axis_hori'][0],
            height=config.size['axis_hori'][1],
            pos=(0, config.pos['report_scale_y']),
            fillColor=config.color_set['black'], lineColor=None
            )
        dvid_0 = rect.Rect(
            win=self.win0, 
            width=config.size['axis_vert'][0],
            height=config.size['axis_vert'][1],
            pos=(0, config.pos['report_scale_y']),
            fillColor=config.color_set['black'], lineColor=None
            )
        dvid_1 = rect.Rect(
            win=self.win1, 
            width=config.size['axis_vert'][0],
            height=config.size['axis_vert'][1],
            pos=(0, config.pos['report_scale_y']),
            fillColor=config.color_set['black'], lineColor=None
            )
        mark_0 = [rect.Rect(
            win=self.win0,
            width=config.size['report_mark'][0],
            height=config.size['report_mark'][1],
            pos=(mark_pos_x[i], config.pos['report_scale_y']),
            fillColor=config.color_set['black'], lineColor=None) \
                for i in choice_keys]
        mark_1 = [rect.Rect(
            win=self.win1,
            width=config.size['report_mark'][0],
            height=config.size['report_mark'][1],
            pos=(mark_pos_x[i], config.pos['report_scale_y']),
            fillColor=config.color_set['black'], lineColor=None) \
                for i in choice_keys]
        title_0.draw(), title_1.draw()
        line_0.draw(), line_1.draw()
        dvid_0.draw(), dvid_1.draw()
        for _ in mark_0:
            _.draw()
        for _ in mark_1:
            _.draw()
        
        # 静态对象：坐标轴文字、指针（双方）、指针文字（双方）
        scale_text_left_0 = TextBox2(
            win=self.win0, text=config.text['scale_text_w'], 
            pos=config.pos['report_scale_text']['w'], alignment='center', 
            font=config.font['CN'], bold=True, 
            letterHeight=config.size['text'], units='norm', 
            color=config.color_set['white'], 
            )
        scale_text_left_1 = TextBox2(
            win=self.win1, text=config.text['scale_text_w'], 
            pos=config.pos['report_scale_text']['w'], alignment='center', 
            font=config.font['CN'], bold=True, 
            letterHeight=config.size['text'], units='norm', 
            color=config.color_set['white'], 
            )
        scale_text_right_0 = TextBox2(
            win=self.win0, text=config.text['scale_text_b'], 
            pos=config.pos['report_scale_text']['b'], alignment='center', 
            font=config.font['CN'], bold=True, 
            letterHeight=config.size['text'], units='norm', 
            color=config.color_set['black'], 
            )
        scale_text_right_1 = TextBox2(
            win=self.win1, text=config.text['scale_text_b'], 
            pos=config.pos['report_scale_text']['b'], alignment='center', 
            font=config.font['CN'], bold=True, 
            letterHeight=config.size['text'], units='norm', 
            color=config.color_set['black'], 
            )
        pointer0_sub0 = polygon.Polygon(
            win=self.win0, edges=3, 
            ori=map_pointer_rotation[0], 
            pos=(mark_pos_x[scale_0], config.pos['report_pointer_y'][0]), 
            size=config.size['pointer'], 
            fillColor=self.highlight_color[0], lineColor=None
            )
        pointer0_sub1 = polygon.Polygon(
            win=self.win1, edges=3, 
            ori=map_pointer_rotation[0], 
            pos=(mark_pos_x[scale_0], config.pos['report_pointer_y'][0]), 
            size=config.size['pointer'], 
            fillColor=self.highlight_color[0], lineColor=None
            )
        pointer1_sub0 = polygon.Polygon(
            win=self.win0, edges=3, 
            ori=map_pointer_rotation[1], 
            pos=(mark_pos_x[scale_1], config.pos['report_pointer_y'][1]), 
            size=config.size['pointer'], 
            fillColor=self.highlight_color[1], lineColor=None
            )
        pointer1_sub1 = polygon.Polygon(
            win=self.win1, edges=3, 
            ori=map_pointer_rotation[1], 
            pos=(mark_pos_x[scale_1], config.pos['report_pointer_y'][1]), 
            size=config.size['pointer'], 
            fillColor=self.highlight_color[1], lineColor=None
            )
        pointerText0_sub0 = TextBox2(
            win=self.win0, text=config.report_value[report_mode][scale_0], 
            pos=(mark_pos_x[scale_0], config.pos['report_pointer_text_y'][0]), alignment='center', 
            font=config.font['CN'], bold=True, 
            letterHeight=config.size['text'], units='norm', 
            color=self.highlight_color[0], 
            )
        pointerText0_sub1 = TextBox2(
            win=self.win1, text=config.report_value[report_mode][scale_0], 
            pos=(mark_pos_x[scale_0], config.pos['report_pointer_text_y'][0]), alignment='center', 
            font=config.font['CN'], bold=True, 
            letterHeight=config.size['text'], units='norm', 
            color=self.highlight_color[0], 
            )
        pointerText1_sub0 = TextBox2(
            win=self.win0, text=config.report_value[report_mode][scale_1], 
            pos=(mark_pos_x[scale_1], config.pos['report_pointer_text_y'][1]), alignment='center', 
            font=config.font['CN'], bold=True, 
            letterHeight=config.size['text'], units='norm', 
            color=self.highlight_color[1], 
            )
        pointerText1_sub1 = TextBox2(
            win=self.win1, text=config.report_value[report_mode][scale_1], 
            pos=(mark_pos_x[scale_1], config.pos['report_pointer_text_y'][1]), alignment='center', 
            font=config.font['CN'], bold=True, 
            letterHeight=config.size['text'], units='norm', 
            color=self.highlight_color[1], 
            )
        scale_text_left_0.draw(), scale_text_left_1.draw()
        scale_text_right_0.draw(), scale_text_right_1.draw()
        pointer0_sub0.draw(), pointer0_sub1.draw()
        pointer1_sub0.draw(), pointer1_sub1.draw()
        pointerText0_sub0.draw(), pointerText0_sub1.draw()
        pointerText1_sub0.draw(), pointerText1_sub1.draw()

        if same_choice: #选择相同，自动做出最终判断
            # 静态对象：自动选择
            auto_choice_0 = TextBox2(
                win=self.win0, 
                text=config.text['choice_public_w'] if scale_0 < 0 else config.text['choice_public_b'], 
                pos=config.pos['report_choice'], alignment='center',
                font=config.font['CN'], bold=True, 
                letterHeight=config.size['text_large'], units='norm', 
                color=config.color_set['white'] if scale_0 < 0 else config.color_set['black']
                )
            auto_choice_1 = TextBox2(
                win=self.win1, 
                text=config.text['choice_public_w'] if scale_1 < 0 else config.text['choice_public_b'], 
                pos=config.pos['report_choice'], alignment='center',
                font=config.font['CN'], bold=True, 
                letterHeight=config.size['text_large'], units='norm', 
                color=config.color_set['white'] if scale_1 < 0 else config.color_set['black']
                )
            auto_choice_0.draw(), auto_choice_1.draw()
        else: #选择不同，其中一方做出最终判断
            # 静态对象：等待提示 / 按键提示
            tips_host = TextBox2(
                win=map_win[host_subject],
                text=config.text['tips_public_host'],
                pos=config.pos['report_tips'], alignment='center',
                font=config.font['CN'], bold=True, 
                letterHeight=config.size['text_small'], units='norm', 
                color=config.color_set['black']
                )
            tips_wait = TextBox2(
                win=map_win[wait_subject],
                text=config.text['tips_public_wait'],
                pos=config.pos['report_tips'], alignment='center',
                font=config.font['CN'], bold=True, 
                letterHeight=config.size['text_small'], units='norm', 
                color=config.color_set['black']
                )
            tips_host.draw(), tips_wait.draw()
            # 动态对象：当前选择
            if host_choice:
                final_choice_0 = TextBox2(
                    win=self.win0, text=map_choice_text[host_choice], 
                    pos=config.pos['report_choice'], alignment='center',
                    font=config.font['CN'], bold=True, 
                    letterHeight=config.size['text_large'], units='norm', 
                    color=map_choice_color[host_choice]
                    )
                final_choice_1 = TextBox2(
                    win=self.win1, text=map_choice_text[host_choice], 
                    pos=config.pos['report_choice'], alignment='center',
                    font=config.font['CN'], bold=True, 
                    letterHeight=config.size['text_large'], units='norm', 
                    color=map_choice_color[host_choice]
                    )
                final_choice_0.draw(), final_choice_1.draw()
            else:
                wait_choice = TextBox2(
                    win=map_win[host_subject], text=map_choice_text[host_choice], 
                    pos=config.pos['report_choice'], alignment='center',
                    font=config.font['CN'], bold=True, 
                    letterHeight=config.size['text_large'], units='norm', 
                    color=self.highlight_color[host_subject]
                    )
                wait_choice.draw()

        self.win0.flip(), self.win1.flip()



    def private_feedback(self, subject:int, actual_stim:str, choice:str):
        '''
        渲染【单个窗口】的结果反馈页面，仅适用于 solo 阶段。
        - subject: 被试编号（0/1）。
        - actual_stim: 实际的刺激（'w'/'b'）。
        - choice: 该被试的选择（'w'/'b'）。
        '''

        map_win = {0:self.win0, 1:self.win1}

        correct = True if choice == actual_stim else False

        feedback = TextBox2(
            win=map_win[subject], 
            text=config.text['feedback_private_T'] if correct else config.text['feedback_private_F'], 
            pos=config.pos['feedback_solo'], alignment='center',
            font=config.font['CN'], bold=True, 
            letterHeight=config.size['text_huge'], units='norm', 
            color=self.highlight_color[subject]
            )
        
        feedback.draw()
        map_win[subject].flip()



    def public_feedback(
            self, actual_stim:str,
            choice_0:str, choice_1:str, choice_public:str
            ) -> None:
        '''
        渲染【两个窗口】的反馈页面，仅适用于 dual 阶段。
        - actual_stim: 实际的刺激（'w'/'b'）。
        - choice_x: 个体或群体最终选择（'w'/'b'）。
        '''

        correct_0 = True if choice_0 == actual_stim else False
        correct_1 = True if choice_1 == actual_stim else False
        correct_public = True if choice_public == actual_stim else False
        map_color = {
            'w': config.color_set['white'], 
            'b': config.color_set['black']
            }

        feedback_private0_sub0 = TextBox2(
            win=self.win0,
            text=config.text['feedback_private_T'] if correct_0 else config.text['feedback_private_F'],
            pos=config.pos['feedback_dual_private'][0], alignment='center',
            font=config.font['CN'], bold=True, 
            letterHeight=config.size['text_huge'], units='norm', 
            color=self.highlight_color[0]
            )
        feedback_private0_sub1 = TextBox2(
            win=self.win1,
            text=config.text['feedback_private_T'] if correct_0 else config.text['feedback_private_F'],
            pos=config.pos['feedback_dual_private'][0], alignment='center',
            font=config.font['CN'], bold=True, 
            letterHeight=config.size['text_huge'], units='norm', 
            color=self.highlight_color[0]
            )
        feedback_private1_sub0 = TextBox2(
            win=self.win0,
            text=config.text['feedback_private_T'] if correct_1 else config.text['feedback_private_F'],
            pos=config.pos['feedback_dual_private'][1], alignment='center',
            font=config.font['CN'], bold=True, 
            letterHeight=config.size['text_huge'], units='norm', 
            color=self.highlight_color[1]
            )
        feedback_private1_sub1 = TextBox2(
            win=self.win1,
            text=config.text['feedback_private_T'] if correct_1 else config.text['feedback_private_F'],
            pos=config.pos['feedback_dual_private'][1], alignment='center',
            font=config.font['CN'], bold=True, 
            letterHeight=config.size['text_huge'], units='norm', 
            color=self.highlight_color[1]
            )
        feedback_public_0 = TextBox2(
            win=self.win0,
            text=config.text['feedback_public_T'] if correct_public else config.text['feedback_public_F'],
            pos=config.pos['feedback_dual_public'], alignment='center',
            font=config.font['CN'], bold=True, 
            letterHeight=config.size['text_huge'], units='norm', 
            color=map_color[choice_public]
            )
        feedback_public_1 = TextBox2(
            win=self.win1,
            text=config.text['feedback_public_T'] if correct_public else config.text['feedback_public_F'],
            pos=config.pos['feedback_dual_public'], alignment='center',
            font=config.font['CN'], bold=True, 
            letterHeight=config.size['text_huge'], units='norm', 
            color=map_color[choice_public]
            )

        feedback_private0_sub0.draw(), feedback_private0_sub1.draw()
        feedback_private1_sub0.draw(), feedback_private1_sub1.draw()
        feedback_public_0.draw(), feedback_public_1.draw()
        self.win0.flip(), self.win1.flip()


    
    def wait_ally(self, subject:int, text:str=config.text['wait_ally']) -> None:
        '''
        向单个被试呈现等待对方完成操作的界面。
        '''
        map_win = {0:self.win0, 1:self.win1}
        waiting_text = TextBox2(
            win=map_win[subject], text=text,
            pos=config.pos['wait_ally'], alignment='center',
            font=config.font['CN'], bold=True,
            letterHeight=config.size['text'], units='norm',
            color=config.color_set['black']
            )
        waiting_text.draw()
        map_win[subject].flip()



if __name__ == '__main__':

    from psychopy import core
    from psychopy.hardware import keyboard

    TEST = dualWin(size_win=(800, 600), pos_win0=(50,100), pos_win1=(900,100))
    kb = keyboard.Keyboard()

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

    def _wait():
        while True:
            core.wait(0.05)
            pressed = kb.getKeys()
            if pressed:
                if pressed[-1].name == 'space':
                    return
                else:
                    kb.clearEvents()
    
    rect_array = {
        1:[0.474, 0.522, 0.489, 0.517],
        }

    TEST.text(text_0='测试test', text_1='测试...')
    _wait()
    TEST.Ready_text(text_0=config.text['ready_trial'],
                    text_1=config.text['ready_trial'],
                    ready_0=True, ready_1=False)
    _wait()
    TEST.Ready_text(text_0=config.text['ready_trial'],
                    text_1=config.text['ready_trial'],
                    ready_0=True, ready_1=True)
    _wait()
    TEST.stim(blackRatio_sub0=rect_array[1], blackRatio_sub1=rect_array[1])
    _wait()
    TEST.private_report(report_mode='confidence', subject=0, scale=4, finish=False)
    TEST.private_report(report_mode='confidence', subject=1, scale=4, finish=False)
    _wait()
    TEST.private_report(report_mode='ratio', subject=0, scale=-4, finish=False)
    TEST.private_report(report_mode='ratio', subject=1, scale=-4, finish=False)
    _wait()
    TEST.private_feedback(subject=0, actual_stim='b', choice='b')
    TEST.private_feedback(subject=1, actual_stim='b', choice='w')
    _wait()
    TEST.public_report(report_mode='confidence', same_choice=True, 
                       scale_0=2, scale_1=5, 
                       host_subject=1, wait_subject=0, 
                       host_choice=None)
    _wait()
    TEST.public_report(report_mode='confidence', same_choice=False, 
                       scale_0=4, scale_1=-3, 
                       host_subject=1, wait_subject=0, 
                       host_choice=None)
    _wait()
    TEST.public_report(report_mode='ratio', same_choice=True, 
                       scale_0=3, scale_1=4, 
                       host_subject=1, wait_subject=0, 
                       host_choice=None)
    _wait()
    TEST.public_report(report_mode='ratio', same_choice=False, 
                       scale_0=5, scale_1=-2, 
                       host_subject=0, wait_subject=1, 
                       host_choice=None)
    _wait()
    TEST.public_feedback(actual_stim='w', 
                         choice_0='b', choice_1='w', 
                         choice_public='b')
    _wait()
    

