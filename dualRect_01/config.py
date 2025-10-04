
import numpy as np

class Configuration:
    '''
    实验静态参数。
    '''

    def __init__(self):

        pass
    
    @property
    def windows_param(self):
        static_param = {
            '1080p_debug': {'res':(1920, 1080), 'pos':((50,200), (1150,200)), 'fullscreen':False},
            '1080p_flscr': {'res':(1920, 1080), 'pos':((50,200), (1150,200)), 'fullscreen':True},
            '1440p_win': {'res':(1200, 900), 'pos':((50,200), (1300,200)), 'fullscreen':False},
            '1440p_flscr': {'res':(2560, 1440), 'pos':((50,200), (1300,200)), 'fullscreen':True},
            '2160p_win': {'res':(1600, 1200), 'pos':((200,600), (2000,600)), 'fullscreen':False},
            '2160p_flscr': {'res':(3840, 2160), 'pos':((200,600), (2000,600)), 'fullscreen':True},
        }
        return static_param
    
    @property
    def allowed_key(self):
        static_param = {
            'skip':('space',),
            }
        return static_param
    
    @property
    def allowed_bt(self):
        static_param = {
            'L':'LB',
            'R':'RB',
            'next':'Y_A', # intro 翻页
            'confirm':'A', # trial 确认选择
            }
        return static_param

    @property
    def color_set(self):
        static_param = {
            'bg_white':'#f2f2f2', 'bg_black':'#2f2f2f', 
            'bg_dark':'#4a4a4a', 'bg_gray':'#808080', 

            'white':"#ffffff", 'black':'#000000', 

            'R':'#af3f3f', 'r':'#dfc0c0',
            'G':'#1f5f2f', 'g':'#b8cfb8',
            'B':'#0939aa', 'b':'#a3a3f5',
            'O':"#cf6317", 'o':'#f2b78c',
            'Y':'#e6c419', 'y':'#f2e18c',
            'P':'#cf2f9f', 'p':'#e0b7c0',
            'stim_mark':['#e64d4d','#e6b34d','#b3e64d','#4de666','#4de6e6','#804de6',
                         '#1a1a1a',
                         '#804de6','#4de6e6','#4de666','#b3e64d','#e6b34d','#e64d4d',]
        }
        return static_param

    @property
    def font(self):
        static_param = {
            # 'CN':'Source Han Serif SC', 
            # 'CN':'Source Han Sans SC', 
            'CN':'Sarasa Gothic SC',
            'EN':'Times New Roman', 
        }
        return static_param
    
    @property
    def time(self):
        static_param = {
            'io_interval':0.01, #io采样间隔
            'auto_timeout':2, #自动跳过的默认等待时间
            'intro_timeout':3, #指导语的默认等待时间
            'ready_timeout':0, #准备阶段的默认等待时间
            'ready_delay':0.35, #双方都准备好后的延迟时间
            'fixation':0.50, #注视点呈现时间
            'stim':3, #刺激呈现时间
            'report_same':4.00, #选择相同时联合判断呈现时间
            'report_diff_delay':0.50, #选择不同的联合判断结果延迟时间
            'feedback_private':1.50, #反馈呈现时间
            'feedback_public':2.00, #联合判断反馈呈现时间
            'rest':300, #休息时间
        }
        return static_param
    
    @property
    def trail_num(self):
        static_param = {
            'exercise':[5,5], #b/w
            'solo':[56,56], #b/w
            'dual':[56,56], #b/w
            }
        return static_param
    
    @property
    def rect_num(self):
        static_param = {
            'rect_num':4,
        }
        return static_param
    
    @property
    def pos(self):
        static_param = {
            'ready':(0, 0), #提示准备的文字
            'confirm_self':(-0.50, -0.85), #自己已确认文字（指导语）
            'confirm_ally':(0.50, -0.85), #对方已确认文字（指导语）
            'ready_self':(-0.35, -0.30), #自己已准备文字
            'ready_ally':(0.35, -0.30), #对方已准备文字
            'stim_rect_x':(-0.20, 0.20), #绘制矩形的横向范围
            'stim_markL':[(-0.30, i) for i in np.linspace(-0.06, 0.06, 13)], #刺激刻度（44%~56%）
            'stim_markR':[(0.30, i) for i in np.linspace(-0.06, 0.06, 13)], #刺激刻度（44%~56%）
            'report_title':(0, 0.50), #报告页面标题
            'report_scale_x':(-0.6, 0.6), #选项刻度的横向范围
            'report_scale_y':0, #选项刻度的纵坐标
            'report_scale_text':{'w':(-0.75, 0), 'b':(0.75, 0)}, #轴线左侧：白色更多；右侧：黑色更多
            'report_pointer_y':{0: 0.06, 1:-0.06}, #被试 0 / 1 的选择指针
            'report_pointer_text_y':{0:0.12, 1:-0.12}, #被试 0 / 1 的选择文字
            'report_choice':(0, -0.40), #当前选择
            'report_tips':(0, -0.65), #按键提示
            'wait_ally':(0, 0), #等待对方完成操作
            'feedback_solo':(0, 0), #solo 阶段个人判断正误信息
            'feedback_dual_private':{0:(-0.20, 0), 1:(0.20, 0)}, #dual 阶段个人判断正误信息
            'feedback_dual_public':(0, -0.25), #dual 阶段联合判断正误信息
        }
        return static_param
    
    @property
    def size(self):
        static_param = {
            'fixation':0.2, #注视点（norm）
            'text_tiny':0.030,
            'text_small':0.045,
            'text':0.065, #默认文字大小（norm)
            'text_large':0.085,
            'text_huge':0.100,
            'rect':(0.1, 1), #stim 矩形尺寸（前景/背景，norm）
            'rect_stroke':1, #stim 矩形描边（背景，pix）
            'stim_mark':(0.05, 0.01), #刺激刻度尺寸
            'pointer': 0.035, #当前选择指针（正三角形）
            'axis_hori':(1.2, 0.03), #评价标尺横轴
            'axis_vert':(0.03, 0.40), #评价标尺纵轴
            'report_mark':(0.03, 0.06), #评价刻度
        }
        return static_param
    
    @property
    def report_value(self):
        static_param = {
            'confidence': {
            -6: '信心 6', -5: '信心 5', -4: '信心 4', -3: '信心 3', -2: '信心 2', -1: '信心 1',
            1: '信心 1',  2: '信心 2',  3: '信心 3',  4: '信心 4',  5: '信心 5',  6: '信心 6',
            },
            'ratio': {
            -6: '44.0%', -5: '45.0%', -4: '46.0%', -3: '47.0%', -2: '48.0%', -1: '49.0%',
            1: '51.0%',  2: '52.0%',  3: '53.0%',  4: '54.0%',  5: '55.0%',  6: '56.0%',
            }
            }
        return static_param

    @property
    def text(self):
        static_param = {
            #block
            'intro_exercise_solo_CF':'即将进入练习阶段……\n\n按【A】键继续。', 
            'intro_formal_solo_CF':'接下来是正式实验\n（单人，信心判断）\n\n按【A】键开始任务。',
            'intro_formal_dual_CF':'接下来是正式实验\n（双人，信心判断）\n\n按【A】键开始任务。',
            'intro_exercise_solo_RT':'即将进入练习阶段……\n\n按【A】键继续。',
            'intro_formal_solo_RT':'接下来是正式实验\n（单人，比例估计）\n\n按【A】键开始任务。',
            'intro_formal_dual_RT':'接下来是正式实验\n（双人，比例估计）\n\n按【A】键开始任务。',
            'block_end':'本阶段结束，请稍等……', 
            'rest':'实验进程已过半，请您休息 5 分钟。\n\n休息期间可以自由活动，可以出实验室（记得按时归来）。\n\n后半部分实验将在休息阶段结束后自动开始。',
            'switch_rule':'现在开始实验的后半部分。\n注意，接下来的任务规则有细微的变化。\n\n请呼唤主试。',
            'switch_confidence':'现在开始实验的后半部分。\n\n注意，接下来的任务规则有细微变化。\n\n请您呼唤主试，然后按【Y】+【A】键继续。',
            'switch_ratio':'现在开始实验的后半部分。\n\n注意，接下来的任务规则有细微变化。\n\n请您呼唤主试，然后按【Y】+【A】键继续。',
            'call_me':'请呼唤主试。', 
            'call_me_if_need':'接下来是双人任务。\n\n请您务必仔细阅读指导语，如有疑问请呼唤主试。\n\n按【Y】+【A】键继续。', 
            'no_exercise':'没有练习阶段，正式实验即将开始……', 
            'finale':'实验结束！感谢参与！',
            # trial
            'ready_trial':'准备好后，请按【A】。', 
            'confirm_self':'您已确认', 
            'confirm_ally':'对方已确认', 
            'ready_self':'您已准备', 
            'ready_ally':'对方已准备', 
            'title_private_confidence':'判断哪种颜色占比更多，\n并评估做出正确判断的信心。', 
            'title_private_ratio':'判断哪种颜色占比更多，\n并估计黑色部分面积的比例。', 
            'title_public_same':'双方个人判断相同，自动完成联合判断。', 
            'title_public_diff':'双方个人判断不同，需要进行联合判断！', 
            'scale_text_w':'白色更多', 
            'scale_text_b':'黑色更多', 
            'choice_None':'请您按键选择……',
            'choice_w':'白色更多', 
            'choice_b':'黑色更多', 
            'choice_public_w':'联合判断：白色更多', 
            'choice_public_b':'联合判断：黑色更多', 
            'tips_private':'【LB】左移          【RB】右移\n【A】确认', 
            'tips_public_host':'——————本轮由您完成联合判断——————\n【LB】白色更多          【RB】黑色更多\n【A】确认', 
            'tips_public_wait':'——————等待对方完成联合判断——————', 
            'wait_ally':'请等待对方完成操作……', 
            'feedback_private_T':'正确', 
            'feedback_private_F':'错误', 
            'feedback_public_T':'联合判断：正确', 
            'feedback_public_F':'联合判断：错误', 
        }
        return static_param
    


def init_config():

    global config
    config = Configuration()



init_config()