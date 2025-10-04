
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
            '2160p_flscr':{'res':(3840, 2160),'pos':((200,600), (2000,600))}
        }
        return static_param
    
    @property
    def keys(self):
        static_param = {
            'next_page':('space',),
            'operation':('space',),
            }
        return static_param
    
    @property
    def color_set(self):
        static_param = {
            'bg_white':'#f2f2f2', 'bg_black':'#2f2f2f', 'bg_gray':'#808080', 
            'black':'#000000', 'gray':'#6a6a6a', 
            'R':'#cf3f5f', 'G':'#2da04a', 'B':'#1f50bf', 'O':'#df7c4f', 'P':'#cf4cb0',
            'r':'#dfc0c0', 'g':'#b8cfb8', 'b':'#c8c8df', 'o':'#efd0af', 'p':'#e8c0c0',
            }
        return static_param
    
    @property
    def text(self):
        static_param = {
            'welcome':'欢迎参加实验！\n\n这个实验中，您只需要操纵键盘上的【空格】键。\n\n现在，请你按【空格】翻页。',
            'intro_GO':'规则：\n\n屏幕上会接连呈现字母【b】或【d】。\n一旦出现任何字母，以最快速度按下【空格】键。',
            'intro_GNG_p':'规则：\n\n屏幕上会接连呈现字母【p】或【q】。\n\n当【p】出现时，以最快速度按下【空格】键。\n不要对【q】进行反应！',
            'intro_GNG_q':'规则：\n\n屏幕上会接连呈现字母【p】或【q】。\n\n当【q】出现时，以最快速度按下【空格】键。\n不要对【p】进行反应！',
            'ready_exercise':'接下来是练习阶段。\n\n当您准备好后，按【空格】键开始。',
            'ready_formal':'接下来是正式实验。\n\n当您准备好后，按【空格】键开始。',
            'end_semiblock':'请稍等……',
            'intermezzo':'现在，请您闭眼休息。',
            'fixation':'+',
            'finale':'实验结束。\n\n感谢参与！',
        }
        return static_param
    
    @property
    def stim_params(self):
        static_param = {
            'block':6, 
            'stim_size':0.25,
            'text_size':0.08, 
        }
        return static_param

    @property
    def stim_obj(self):
        static_param = {
            'block_GO':{'go':'b','ng':'d'},
            'block_GNG_p':{'go':'p','ng':'q'},
            'block_GNG_q':{'go':'q','ng':'p'},
        }
        return static_param
    
    @property
    def stim_num(self):
        static_param = {
            'block_GO':{'go':12,'ng':12},
            'block_GNG_p':{'go':12,'ng':12},
            'block_GNG_q':{'go':12,'ng':12},
        }
        return static_param
    
    @property
    def duration(self):
        static_param = {
            'wait_resting_state':3,
            'wait_intro':3,
            'wait_ready':3,
            'wait_fixation':0.7,
            'wait_stim':0.5,
            'wait_intermezzo':5,
            'wait_finale':5,
        }
        return static_param



def init_config():

    global config

    config = Configuration()



init_config()