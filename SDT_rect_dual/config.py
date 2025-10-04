
class Configuration:

    '''
    静态参数。
    '''

    def __init__(self):

        pass
    
    @property
    def windows_param(self):
        static_param = {
            '1440p_debug':{'res':(1200, 900),'pos':((50,400), (1350,400))},
            '1440p_flscr':{'res':(2560, 1440),'pos':((50,400), (1350,400))},
            '2160p_debug':{'res':(1600, 1200),'pos':((200,600), (2000,600))},
        }
        return static_param
    
    @property
    def allowed_key(self):
        static_param = ('space',)
        return static_param
    
    @property
    def allowed_bt(self):
        static_param = ('Y_A',)
        return static_param
    
    @property
    def color_set(self):
        static_param = {
            'bg_white':'#f2f2f2', 'bg_black':'#2f2f2f', 'bg_gray':'#808080', 
            'black':'#000000', 
            'R':'#af3f3f', 'G':'#1f5f2f', 'B':'#3f3fdf', 'O':'#df7f0f', 'P':'#cf2f9f',
            'r':'#dfc0c0', 'g':'#b8cfb8', 'b':'#c8c8df', 'o':'#efd0af', 'p':'#e0b7c0',
            # 'noise':'#4f4f4f', 'signal':'#3a3a3a', 'signal_hard':'#3e3e3e', 'signal_easy':'#2d2d2d', 
            }
        return static_param
    
    @property
    def stim_param(self):
        static_param = {
            'rect_num':9, #每组刺激图形的数量
            'scale':6, #量表的单边尺度（实际*2）
            'duration_ready_delay':0.750, # 双方都准备好后的延迟时间
            'duration_fixation':1.000, #注视点呈现时间
            'duration_stim':1.000, #刺激呈现时间
        }
        return static_param
    
    @property
    def trail_num(self):
        static_param = {
            'exercise':[2,2], 
            'solo':[50,50], 
            'dual':[50,50], 
        }
        return static_param
    
    @property
    def pos(self):
        static_param = {
            'trail_ready':(0, 0), #提示准备的文字
            'trail_ready_self':(-0.5, -0.30), #自己已准备文字
            'trail_ready_allay':(0.5, -0.30), #对方已准备文字
            'trail_title':(0, 0.30), #问题（是否超过一半）
            'trail_scale_y':0, #选项的纵坐标
            'trail_choice':(0, -0.30), #自己选择的文字表示
            'final_self':(0, 0.20), #展示自己的最终选择（仅 mode=='dual' 时有效）
            'final_allay':(0, 0.12), #展示对方的最终选择（仅 mode=='dual' 时有效）
            'final_choice':(0, -0.20), #自己进行最终选择 / 等待对方最终选择的文字提示
        }
        return static_param
    
    @property
    def size(self):
        static_param = {
            'fixation':0.2, #注视点（norm）
            'text':0.065, #默认文字大小（norm)
            'text_small':0.045, #文字大小（norm）
            'text_large':0.085, #文字大小（norm）
            'rect':(0.1, 1), #stim 矩形尺寸（前景/背景，norm）
            'rect_stroke':1, #stim 矩形描边（背景，pix）
            'selected':(0.09, 0.16), #选框尺寸（norm）
            'selected_stroke':5, #选框描边（pix）
        }
        return static_param

    @property
    def text(self):
        static_param = {
            'trail_ready':'做好准备后，请按【Y】+【A】键开始。', 
            'trail_ready_self':'您已准备!', 
            'trail_ready_allay':'对方已准备!', 
            'trail_title':'黑色部分的平均面积是否超过一半？', 
            'wait_choice':'请按键选择……', 
            'pos':'您的选择：是', 
            'neg':'您的选择：否', 
            'pos_final':'您的选择：是\n（【Y】+【A】确认，确认前可修改）', 
            'neg_final':'您的选择：否\n（【Y】+【A】确认，确认前可修改）', 
            'wait_allay_solo':'请等待对方完成选择……', 
            'same_choice_s':'最终选择：“是”', 
            'same_choice_n':'最终选择：“否”', 
            'wait_self_dual':'本轮由您进行最终选择。\n请按键……\n（【LB】是  【RB】否）', 
            'wait_allay_dual':'本轮由对方进行最终选择。\n请等待……', 
            'final_choice_s':'最终选择：“是”', 
            'final_choice_n':'最终选择：“否”', 
            'intermezzo':'本轮结束\n请准备……', #已经作废了，用 ready_trail 替代。
            'stage_end':'本阶段结束，请稍等……', #每个 block 结束
            'call_me':'请呼唤主试。', 
            'start_exercise':'练习阶段即将开始。', 
            'start_formal':'正式实验即将开始。', #同时被 solo/dual 复用
            'finale':'实验结束！感谢参与！', 
        }
        return static_param
    


def init_config():

    global config

    config = Configuration()



init_config()