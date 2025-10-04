
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
    def key_nextpage(self):
        static_param = ('space',)
        return static_param

    @property
    def key_operation(self):
        static_param = {
            's_orient':'f', 
            'n_orient':'j', 
            'confirm':'space', 
        }
        return static_param
    
    @property
    def jsbt_nextpage(self):
        static_param = ('X',)
        return static_param
    
    @property
    def color_set(self):
        static_param = {
            'bg_white':'#f2f2f2', 'bg_black':'#2f2f2f', 'bg_gray':'#808080', 
            'black':'#000000', 'gray':'#6a6a6a', 
            'R':'#cf3f5f', 'G':'#2da04a', 'B':'#1f50bf', 'O':'#df8c4f', 'P':'#df7caf',
            'r':'#dfc0c0', 'g':'#b8cfb8', 'b':'#c8c8df', 'o':'#efd0af', 'p':'#e8c0c0',
            }
        return static_param
    
    @property
    def stim_params(self):
        static_param = {
            'rect_num':9, #每组刺激图形的数量
            'scale':6, #量表的单边尺度（实际*2）
            'duration_ready_delay':0.25, # 双方都准备好后的延迟时间
            'duration_fixation':0.50, #注视点呈现时间
            'duration_stim':0.75, #刺激呈现时间
            'duration_result':3.00, #展示结果的时间
            'duration_rest':60, # block 之间休息的时间
        }
        return static_param
    
    @property
    def trial_num(self):
        static_param = { # block : (signal, noise)
            0:(2,2), 
            1:(25,25), 
            2:(25,25),
            3:(25,25),
        }
        return static_param
    
    @property
    def pos(self):
        static_param = {
            'trial_wait':(0, 0), #提示准备的文字
            'trial_ready_state':(0, -0.30), #已准备提示
            'trial_title':(0, 0.55), #问题（是否超过一半）
            'trial_rule':(0, 0.25), #收益计算规则
            'trial_scale_y':0, #选项的纵坐标
            'trial_choice':(0, -0.25), 
            'result_actual':(0, 0.05), #实际情况的文字表示
            'result_choice':(0, -0.05), #自己选择的文字表示
            'result_reward':(0, -0.25), #当前结果对应的收益
            'total_reward':(0, -0.40), #累计收益情况
            'finale_1':(0, 0.30), #实验结束
            'finale_2':(0, 0.10), #收益展示
            'finale_3':(0, -0.20), #被试费发放
            'finale_4':(0, -0.50), #呼唤主试
        }
        return static_param
    
    @property
    def size(self):
        static_param = {
            'fixation':0.2, #注视点（norm）
            'text':0.065, #默认文字大小（norm)
            'text_small':0.055, #文字大小（norm）
            'text_large':0.085, #文字大小（norm）
            'rect':(0.1, 1), #stim 矩形尺寸（前景/背景，norm）
            'rect_stroke':2, #stim 矩形描边（背景，pix）
            'selected':(0.09, 0.16), #选框尺寸（norm）
            'selected_stroke':5, #选框描边（pix）
        }
        return static_param
    
    @property
    def money(self):
        static_param = {
            'reward':0.25, 
            'punish':0.50, #注意在计算 self.reward 时处理为负值
            'none':0, 
        }
        return static_param
    
    @property
    def reward_matrix(self):
        static_param = { # (sn, choice):reward, ...
            'neutral':{(1,1):self.money['reward'], (0,0):self.money['reward'], 
                       (1,0):self.money['none'], (0,1):self.money['none']}, # block 0/1（中性）

            'punish_MS':{(1,1):self.money['reward'], (0,0):self.money['reward'], 
                         (1,0):self.money['punish'], (0,1):self.money['none']}, # block 2/3，激进（惩罚 miss）

            'punish_FA':{(1,1):self.money['reward'], (0,0):self.money['reward'], 
                         (1,0):self.money['none'], (0,1):self.money['punish']}, # block 2/3，保守（惩罚 false alarm）
        }
        return static_param
    
    # @property
    # def confidence_level(self):
    #     static_param = {-6:'高信心', -5:'高信心', -4:'高信心', -3:'低信心', -2:'低信心', -1:'低信心',
    #                      1:'低信心',  2:'低信心',  3:'低信心',  4:'高信心',  5:'高信心',  6:'高信心',}
    #     return static_param

    @property
    def text(self): 
        static_param = {
            'trial_wait':f'做好准备后，请按【空格】键，并集中注意。', 
            'trial_ready_state':'已准备！',
            'trial_title':'黑色部分的平均面积是否超过一半？', 
            'rule_neutral':f'正确获得￥{self.money["reward"]}，错误无收益。', #中性
            'rule_punish_MS':f'正确获得￥{self.money["reward"]}，错误地选【否】扣除￥{self.money["punish"]}。', #激进（惩罚 miss）
            'rule_punish_FA':f'正确获得￥{self.money["reward"]}，错误地选【是】扣除￥{self.money["punish"]}。', #保守（惩罚 false alarm）
            'wait_choice':f'请按【{self.key_operation["s_orient"].capitalize()}】或【{self.key_operation["n_orient"].capitalize()}】键进行选择……', 
            'choice_s':'您的选择：是', 
            'choice_n':'您的选择：否', 
            'actual_s':'正确答案：是', 
            'actual_n':'正确答案：否', 
            'reward_plus':f'获得￥{self.money["reward"]}！', 
            'reward_none':'收益不变', 
            'reward_lose':f'扣除￥{self.money["punish"]}！',  
            'reward':'累计收益：￥', #动态文本的一半
            'stage_end':'本阶段结束，请稍等……', #每个 block 结束
            'intermezzo':f'请您稍作休息。\n{int(self.stim_params["duration_rest"]//60)} 分钟后将进入下一阶段。\n\n请勿进行让大脑疲劳的活动。',
            'start_exercise':'接下来是练习阶段……\n\n按【空格】键继续', 
            'start_formal':'正式实验即将开始……\n\n按【空格】键继续', 
            'finale_1':'实验结束！感谢参与！', 
            'finale_2':'   最终收益：￥', 
            'finale_3':'校内被试费将通过与学号绑定的中行卡发放，请仔细核对。\n- 每月 8 日及之前的实验，于当月底发放；\n- 每月 9 日及之后的实验，于次月底发放。', 
            'finale_4':'请将【学号】发送至主试微信，并呼唤主试。\n若为校外被试请说明情况。',
        }
        return static_param



def init_config():

    global config

    config = Configuration()



init_config()
