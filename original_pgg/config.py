'''
实验静态参数。
'''

class Configuration:

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
    def allowed_keys(self):
        static_param = ('space')
        return static_param
    
    @property
    def color_set(self):
        static_param = {
            'bg_white':'#f2f2f2', 'bg_black':'#2f2f2f', 
            'black':'#000000', 
            'R':'#af3f3f', 'G':'#1f5f2f', 'B':'#3f3fdf', 'O':'#df7f0f', 'P':'#cf2f9f',
            'r':'#dfc0c0', 'g':'#b8cfb8', 'b':'#c8c8df', 'o':'#efd0af', 'p':'#e0b7c0',
        }
        return static_param
    
    @property
    def static_text(self):
        static_param = {
            'intermezzo':'本阶段任务结束。\n\n即将进入下一阶段……',
            'call_me':'本阶段任务结束。\n\n请呼唤主试。',
            'add_public_box':'【LB】投入公共账户',
            'add_private_box':'【RB】投入私人账户',
            'confirm_token':'【Y】+【A】确认分配',
            'wait_allay_choice':'请等待对方完成选择……',
            'wait_allay_PGG':'请等待对方完成分配……',
            'choice_guide':'  【LB】选择“是”      【RB】选择“否”\n\n【A】确认',
            'choice_confirm':{
                'LB':'您选择了“是”', 
                'RB':'您选择了“否”'
                },
            'choice_result':{
                'same':'本轮作答情况：\n\n      双方的【相同观点】多于【不同观点】。\n\n请呼唤主试。',
                'diff':'本轮作答情况：\n\n      双方的【不同观点】多于【相同观点】。\n\n请呼唤主试。'
                },
            'discuss_choice':{ 
                None:' ', 
                'same_LB':' 您的观点：是\n对方观点：是',
                'same_RB':' 您的观点：否\n对方观点：否',
                'diff_LB':' 您的观点：是\n对方观点：否',
                'diff_RB':' 您的观点：否\n对方观点：是',},
            'discussion_end':'本阶段任务结束。\n\n陈述完您的观点后，请呼唤主试。',
            'exp_end':'实验结束，感谢参与！\n\n不要忘记带走随身物品。',
            }
        return static_param
    
    @property
    def pos_element(self):
        static_param = {
            'choice_topic':(0, 0.25),
            'choice_guide':(0, -0.05),
            'choice_confirm':(0, -0.35),
            'discuss_topic':(0, 0),
            'discuss_choice':(0, -0.35),
            'trial_index':(0, 0.85),
            'public_box':(-0.5, 0.35),
            'private_box':(0.5, 0.35),
            'explain_public_box':(-0.5, 0.60),
            'explain_private_box':(0.5, 0.60),
            'public_box_token':(-0.5, 0.35),
            'private_box_token':(0.5, 0.35),
            'add_public_box':(-0.5, 0.10),
            'add_private_box':(0.5, 0.10),
            'confirm_token':(0, -0.35),
            'STAGE_reward_self':(-0.3, -0.60),
            'STAGE_reward_allay':(0.3, -0.60),
        }
        return static_param
    
    @property
    def size_text(self):
        static_param = {
            'default':0.065,
            'choice_guide':0.050, 
            'choice_topic':0.080, 
            'choice_confirm':0.080,
            'discuss_topic':0.080,
            'trial_index':0.050,
            'box_token':0.200,
            'box_label':0.300,
        }
        return static_param
    
    @property
    def size_shape(self):
        static_param = {
            'text_box':(1.7, 1.7),
            'public_box':(0.80, 0.80),
            'private_box':(0.80, 0.80),
            'token':0.02, 
        }
        return static_param

    @property
    def topic_dict(self):
        static_param = {
            1: {
                1:"相比于小组学习，我更喜欢传统的讲授式教学。",
                2:"一般情况下，我会避免表露出自己的情绪状态。",
                3:"我有经常记录自己日常生活的习惯。",
                4:"我的消费行为相对理性，极少冲动消费。",
                5:"在学习或工作时，我对环境中的噪音非常敏感。",
                6:"拒绝他人的请求，会让我内疚好长一段时间。",
                7:"对于不感兴趣的事情，我会选择最后才做。",
                8:"长途旅行时，前往目的地的漫长旅途是一种煎熬。",
                9:"我经常关注最近网上有什么新的热“梗”。",
                10:"我习惯在网络上与陌生网友留言、评论、互动。",
                11:"我经常为自己以前的选择而后悔。",
                12:"我喜欢尝试用不同的方法去完成同一件事。",
                13:"我习惯往最坏的方面去想一件事情的后果。",
                },
            2: {
                1:"我认为门当户对是一项极为重要的择偶原则。",
                2:"我认为人性中的“恶”是多于“善”的。",
                3:"我认为吃苦耐劳是一种优秀品质。",
                4:"我认为“机遇”对的成功的作用大于“努力”。",
                5:"我认为对大学生而言，超前消费是一种不良习惯。",
                6:"我认为我国应该将安乐死合法化。",
                7:"我认为自媒体的出现让人们离事情的真相更近了。",
                8:"我认为奢侈品是一种“智商税”。",
                9:"我认为酒香不怕巷子深，金子总会发光。",
                10:"我认为贫困家庭生育后代是一种不负责任的行为。",
                11:"我认为辩论赛比拼的是话术而非逻辑。",
                12:"我认为应当鼓励各地积极推广方言的使用。",
                13:"我认为做“鸡头”比做“凤尾”更好。",
                },
            3: {
                1:"缺乏社会需求的学科是否应当保留？",
                2:"电子竞技是否适合作为体育比赛的项目？",
                3:"疫情结束后，大学校园是否应该重新向社会开放？",
                4:"报导国际新闻时，是否可以带有主观立场？",
                5:"“文化入侵”的不良后果是否被夸大了？",
                6:"春节期间城市是否应该禁止燃放烟花爆竹？",
                7:"人工智能生成的作品是否可以算作艺术？",
                8:"取缔教培行业是否有利于教育资源的公平化？",
                9:"是否应该严格限制娱乐明星的收入？",
                10:"污染是否是社会发展的必然结果？",
                11:"国家反诈行动是否可以适当牺牲公民个人隐私？",
                12:"传统文化是否应该与现代文化融合以提高吸引力？",
                13:"国家是否应该干预当前婚配与生育率下降的问题？",
                }
                }
        return static_param



def init_config():
    
    global config
    config = Configuration()

init_config()
