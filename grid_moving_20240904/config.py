
'''
实验静态参数配置文件。
'''

import elegen

class Configuration:
    '''
    将所有参数私有化，写为实例方法的返回值，并套用 @property 装饰器。
    '''

    def __init__(self):

        self.__resolution = (1280, 1280)
        self.__key_nextpage = ('space')

        self.__draw_range = (0.6, 0.75)
        self.__draw_offset = (0, 0.1)

        self.__graph_param = {'small_text_scaling':0.35, 'medium_text_scaling':0.45, 'large_text_scaling': 0.55, 'huge_text_scaling':0.65, 
                              'basic_unit_width':2, 'legal_unit_width':4, 'moveto_unit_width':8, }

        self.__colorset = {'default':'#1a1a1a', 'obvious':'#8025bc', 'bg_window':'#ffffff', 
                           'bg_step':'#0084CD', 'bg_score':'#CE0058', 'bg_empty':'#d7d7d7', 'bg_location':'#353535', 
                           'line_moveto':'#daca7e', 'line_default':'#1a1a1a', 'line_legal':'#3afe9a', 
                           'team_related':'#1a1a1a', 'self_related':'#f47f3e', 'allay_related':'#2fac5f', }
        
        self.__font_size = 60
        self.__unit_scaling = 0.9

        self.__marker = {}
        
        self.__static_text = {
            'welcome':'欢迎您参与本次实验！\n\n（1）在本次实验中，你将与一名同伴共同完成一项任务。\n（2）实验的总时长大约45分钟。\n\n请您仔细聆听实验指导语。', 
            'trial_end':'步数已耗尽。\n\n正在加载下一页...', 
            'operation_end':'本阶段任务结束，即将进入下一阶段...', 
            'option_begin':'接下来，您将阅读一系列观点，您需要根据操作提示选择您是否同意这些观点。', 
            'option_end':'本阶段结束，即将进入下一阶段...', 
            'discussion_begin':'接下来，您将与对方针对之前的某一个观点进行讨论。\n你们双方可以自由地发表看法，限时 3 分钟。\n但请注意，不要谈论关于“走方格任务”的任何话题。', 
            'discussion_end':'本阶段讨论结束，即将进入下一阶段...', 
            'finale':'实验结束！\n感谢您的参与！', 
            } #除了finale之外，都转换成图片形式了。

        self.__hud_text = {'turn_self':'您的\n回合', 'turn_allay':'对方回合', 'step_remain':'剩余步数', 
                           'score_total':'队伍总分', 'score_self':'您的分数', 'score_allay':'对方分数', 
                           'tips':'【Y】向上\n【A】向下\n【X】向左\n【B】向右\n\n【LB】移动方格\n【RB】回到起点\n\n只能移动到\n绿色区域', 
                           'end':'本轮步数已耗尽！\n本阶段累计得分情况：'}

        self.__grid_series_test = {
            0:{'m':9, 'n':9, 'init_loca':(4,4),'init_step':6, 'init_role':0, 'element':{}}, 
            }

        self.__grid_series_exercise = {
            0:{'m':9, 'n':9, 'init_loca':(4,4), 'init_step':6, 'init_role':0, 'element':{}}, 
            1:{'m':9, 'n':9, 'init_loca':(4,4), 'init_step':6, 'init_role':1, 'element':{}},
            }
        
        self.__grid_series_strategy = {
            0:{'m':9, 'n':9, 'init_loca':(4,4), 'init_step':6, 'init_role':0, 'element':{}}, 
            1:{'m':9, 'n':9, 'init_loca':(4,4), 'init_step':6, 'init_role':1, 'element':{}},
            2:{'m':9, 'n':9, 'init_loca':(4,4), 'init_step':6, 'init_role':0, 'element':{}},
            3:{'m':9, 'n':9, 'init_loca':(4,4), 'init_step':6, 'init_role':1, 'element':{}},
            4:{'m':9, 'n':9, 'init_loca':(4,4), 'init_step':6, 'init_role':0, 'element':{}},
            5:{'m':9, 'n':9, 'init_loca':(4,4), 'init_step':6, 'init_role':1, 'element':{}},
        }

        self.__grid_series_formal = {
            0:{'m':9, 'n':9, 'init_loca':(4,4), 'init_step':6, 'init_role':0, 'element':{}}, 
            1:{'m':9, 'n':9, 'init_loca':(4,4), 'init_step':6, 'init_role':1, 'element':{}},
            2:{'m':9, 'n':9, 'init_loca':(4,4), 'init_step':6, 'init_role':0, 'element':{}},
            3:{'m':9, 'n':9, 'init_loca':(4,4), 'init_step':6, 'init_role':1, 'element':{}},
            4:{'m':9, 'n':9, 'init_loca':(4,4), 'init_step':6, 'init_role':0, 'element':{}},
            5:{'m':9, 'n':9, 'init_loca':(4,4), 'init_step':6, 'init_role':1, 'element':{}},
            }
        
        # 备注：exp_1.1 阶段的下列条目仅为 exp_2.2/3.2 做预测试，所以可以尽可能多地添加。
        self.__option = {
            1: [
                "相比于小组学习，我更喜欢传统的讲授式教学。",
                "一般情况下，我会避免表露出自己的情绪状态。",
                "我有经常记录自己日常生活的习惯。",
                "我的消费行为相对理性，极少冲动消费。",
                "在学习或工作时，我对环境中的噪音非常敏感。",
                "拒绝他人的请求，会让我内疚好长一段时间。",
                "对于不感兴趣的事情，我会选择最后才做。",
                "长途旅行时，前往目的地的漫长旅途是一种煎熬。",
                "我经常关注最近网上有什么新的热“梗”。",
                "我习惯在网络上与陌生网友留言、评论、互动。",
                "我经常为自己以前的选择而后悔。",
                "我喜欢尝试用不同的方法去完成同一件事。",
                "我习惯往最坏的方面去想一件事情的后果。",
                ],
            2: [
                "我认为门当户对是一项极为重要的择偶原则。",
                "我认为人性中的“恶”是多于“善”的。",
                "我认为吃苦耐劳是一种优秀品质。",
                "我认为“机遇”对的成功的作用大于“努力”。",
                "我认为对大学生而言，超前消费是一种不良习惯。",
                "我认为我国应该将安乐死合法化。",
                "我认为自媒体的出现让人们离事情的真相更近了。",
                "我认为奢侈品是一种“智商税”。",
                "我认为酒香不怕巷子深，金子总会发光。",
                "我认为贫困家庭生育后代是一种不负责任的行为。",
                "我认为辩论赛比拼的是话术而非逻辑。",
                "我认为应当鼓励各地积极推广方言的使用。",
                "我认为做“鸡头”比做“凤尾”更好。",
                ],
            3: [
                "缺乏社会需求的学科是否应当保留？",
                "电子竞技是否适合作为体育比赛的项目？",
                "疫情结束后，大学校园是否应该重新向社会开放？",
                "报导国际新闻时，是否可以带有主观立场？",
                "“文化入侵”的不良后果是否被夸大了？",
                "春节期间城市是否应该禁止燃放烟花爆竹？",
                "人工智能生成的作品是否可以算作艺术？",
                "取缔教培行业是否有利于教育资源的公平化？",
                "是否应该严格限制娱乐明星的收入？",
                "污染是否是社会发展的必然结果？",
                "国家反诈行动是否可以适当牺牲公民个人隐私？",
                "传统文化是否应该与现代文化融合以提高吸引力？",
                "国家是否应该干预当前婚配与生育率下降的问题？"
                ]
                } #行为习惯、热点事件、价值评判。

        
        self.__option_guide = '按【X】选择“是”                                按【B】选择“否”\n\n可以修改您的选择，确认无误后再按【LB】。\n\n选项无对错之分，根据真实想法选择即可。'
        self.__option_confirm = {'aye':'您选择了“是”', 'nay':'您选择了“否”'}
        self.__option_wait = '请等待对方完成选择...'
        self.__option_pos = {'content':(0, 0.3), 'guide':(0, -0.1), 'choice':(0, -0.4)}

        self.__discuss_guide = {None:'你们双方的选择恰好完全相同或完全不同。\n请呼唤主试。', 
                                'same':'请尽可能多地说出您持有这种观点的原因或理由。\n时间限制：2 分钟', 
                                'diff':'请尽可能多地说出您持有这种观点的原因或理由。\n时间限制：2 分钟'}
        self.__discuss_self = {None:' ', 
                               'aye':'您的观点：“是”', 
                               'nay':'您的观点：“否”'}
        self.__discuss_pos = {'guide':(0, 0.3), 
                              'topic':(0. -0.3), 
                              'self':(0, -0.5)}
    
    @property
    def resolution(self):
        '''屏幕分辨率。'''
        return self.__resolution

    @property
    def key_nextpage(self):
        '''键盘翻页按键。'''
        return self.__key_nextpage
    
    @property
    def draw_range(self):
        '''矩阵占窗口横纵分辨率的比例'''
        return self.__draw_range
    
    @property
    def draw_offset(self):
        '''矩阵中心相对于窗口中心的横纵偏移量占横纵分辨率的比例。'''
        return self.__draw_offset
    
    @property
    def static_text(self):
        '''静态文本（指导语）。'''
        return self.__static_text

    @property
    def hud_text(self):
        '''辅助文本（任务中的静态、动态文本）。'''
        return self.__hud_text

    @property
    def graph_param(self):
        '''矩阵绘图参数。'''
        return self.__graph_param

    @property
    def colorset(self):
        '''各类对象的色号。'''
        return self.__colorset
    
    @property
    def font_size(self):
        '''基础文字尺寸（像素）。'''
        return self.__font_size

    @property
    def unit_scaling(self):
        '''矩阵中的单位形状的缩放比例。'''
        return self.__unit_scaling
    
    @property
    def marker(self):
        '''marker 代码字典。'''
        return self.__marker
    
    @property
    def grid_series_test(self):
        '''调试阶段的 grid 参数字典。'''
        return self.__grid_series_test

    @property
    def grid_series_exercise(self):
        '''练习阶段的 grid 参数字典。'''
        return self.__grid_series_exercise
    
    @property
    def grid_series_strategy(self):
        '''策略水平操纵阶段的 grid 参数字典。'''
        return self.__grid_series_strategy
    
    @property
    def grid_series_formal(self):
        '''
        正式实验的 grid 参数字典。
        * 各阶段调用时记得手动调整 grid.stage 参数。
        '''
        return self.__grid_series_formal
    
    @property
    def option(self):
        '''迫选文本。'''
        return self.__option
    
    @property
    def option_guide(self):
        '''迫选操作指南。'''
        return self.__option_guide
    
    @property
    def option_confirm(self):
        '''确认迫选选项。'''
        return self.__option_confirm
    
    @property
    def option_wait(self):
        '''等待对方完成迫选。'''
        return self.__option_wait
    
    @property
    def option_pos(self):
        '''选项页面各内容位置参数。'''
        return self.__option_pos
    
    @property
    def discuss_guide(self):
        '''讨论阶段呈现的文字。'''
        return self.__discuss_guide
    
    @property
    def discuss_self(self):
        '''讨论阶段呈现的自己的观点。'''
        return self.__discuss_self

    @property
    def discuss_pos(self):
        '''讨论阶段呈现的文字的位置参数。'''
        return self.__discuss_pos
    
    def element_generator(self, grid_series:dict, eleratio_rev:float=2.0, step_ratio_rev:float=6.0):
        '''
        调用 generator.py 模块生成固定的伪随机 bonus element 字典。
        - ele_ratio_rev: 奖励格子（非空格子）占总格子数量比例的倒数，2.0 表示占 1/2。
        - step_ratio_rev: 步数奖励格子占奖励格子（非空格子）数量比例的倒数，6.0 表示占 1/6，设为极大值可以移除所有步数奖励格子。
        '''
        for i in grid_series.keys():
            bonus_dict = elegen.gen_bonus(seed=i, m=grid_series[i]['m'], n=grid_series[i]['n'], 
                                          init_loca=grid_series[i]['init_loca'], ele_ratio_rev=eleratio_rev, step_ratio_rev=step_ratio_rev)
            grid_series[i]['element'] = bonus_dict

config = Configuration()

config.element_generator(config.grid_series_test)
config.element_generator(config.grid_series_exercise, step_ratio_rev=9.0)
config.element_generator(config.grid_series_formal)

if __name__ == '__main__':

    print(config.grid_series_test)