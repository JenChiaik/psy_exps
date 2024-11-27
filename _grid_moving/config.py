
'''
实验静态参数配置文件。
'''

import elegen

class Configuration:
    '''
    将所有参数私有化，写为实例方法的返回值，并套用 @property 装饰器。
    '''

    def __init__(self):

        self.__resolution = (1600, 1200) #4k单屏调试
        self.__win_pos = ((200,600), (2000,600)) #4k单屏调试

        # self.__resolution = (2560, 1440) #2.5k单屏调试
        # self.__win_pos = ((50,400), (1350,400)) #2.5k 单屏调试

        # self.__resolution = (2560,1440) #2.5k正式实验（全屏）

        self.__key_nextpage = ('space')

        self.__draw_range = (0.6, 0.75)
        self.__draw_offset = (0, 0.1)

        self.__graph_param = {'tiny_text_scaling':0.22, 'small_text_scaling':0.32, 'medium_text_scaling':0.42, 
                              'large_text_scaling': 0.52, 'huge_text_scaling':0.62, 
                              'basic_unit_width':2, 'legal_unit_width':4, 'moveto_unit_width':18, }

        # self.__colorset = {'default':'#1a1a1a', 'obvious':'#9025cc', 'bg_window':'#ffffff', 
        #                    'bg_step':'#0084cd', 'bg_score':'#ce0058', 
        #                    'bg_empty':'#d7d7d7', 'bg_location':'#353535', 
        #                    'line_moveto':'#daca7e', 'line_default':'#1a1a1a', 'line_legal':'#2ade5a', 
        #                    'team_related':'#1a1a1a', 'self_related':'#f47f3e', 'allay_related':'#2fac5f', }
        
        self.__colorset = {'default':'#1a1a1a', 'obvious':'#ce0058', 'obvious_2':'#3f6f4f', 'bg_window':'#ffffff', 
                           'bg_step':{-4:'#9ae06c', -5:'#c9e06c', -6:'#e0c96c', -7:'#e09a6c'},
                           'bg_score':{4:'#9ae06c', 5:'#c9e06c', 6:'#e0c96c', 7:'#e09a6c'},
                           'bg_empty':'#eeeeee', 'bg_location':'#353535', 
                           'line_moveto':'#ef8fdf', 'line_default':'#1a1a1a', 'line_legal':'#2f8fdf', 
                           'team_related':'#1a1a1a', 'self_related':'#f47f3e', 'allay_related':'#2fac5f', }

        self.__font_size = 60
        self.__unit_scaling = 0.9

        self.__static_text = {
            'grid_end':'本阶段“走方格”任务结束。\n\n请呼唤主试...', 
            'stage_end':'本阶段结束。\n即将进入下一阶段...', 
            'discussion_end':'本阶段讨论时间到。\n\n请陈述完您的观点之后呼唤主试...', 
            'finale':'实验结束！\n感谢您的参与！',
            }

        self.__hud_text = {'turn_self':'您的\n回合', 'turn_allay':'对方回合', 'step_remain':'剩余步数', 
                           'score_total':'队伍总分', 'score_self':'您的分数', 'score_allay':'对方分数', 
                           'redeem_score':'重置消耗', 
                           'waste_punishment':'浪费步数惩罚', 
                           'tips':'【A/B/X/Y】\n选择位置\n\n【LB】\n移动方格\n\n【back - RB】\n结束本轮', 
                           'end':'本轮已结束！\n当前累计得分：'}

        self.__grid_series_test = {
            0:{'m':7, 'n':7, 'init_loca':(3,3),'init_step':11, 'init_role':0, 'element':{}},
            }

        self.__grid_series_exercise_1 = { #得分操作练习：合法位置得分 - 结束
            110:{'m':7, 'n':7, 'init_loca':(2,3), 'init_step':11, 'init_role':0, 
                 'element':{(2,6):(-5,5), (4,6):(-7,7), (5,6):(-5,5),}}, #合法位置-得分-结束
            111:{'m':7, 'n':7, 'init_loca':(1,5), 'init_step':11, 'init_role':1, 
                 'element':{(4,5):(-6,6), (4,3):(-7,7), (4,2):(-4,4),}}, #合法位置-得分-结束
            }
        
        self.__grid_series_exercise_2 = { #重置步数练习：重置步数 - 得分 - 重置步数 - 得分 - 结束。
            120:{'m':7, 'n':7, 'init_loca':(3,3), 'init_step':2, 'init_role':0, 
                 'element':{(1,5):(-7,7), (5,5):(-4,4), (5,1):(-7,7), (1,1):(-4,4)}}, 
            121:{'m':7, 'n':7, 'init_loca':(3,3), 'init_step':2, 'init_role':0, 
                 'element':{(1,5):(-6,6), (5,5):(-5,5), (5,1):(-7,7), (1,1):(-4,4)}}, 
            }
        
        self.__grid_series_exercise_3 = { #自由练习
            130:{'m':7, 'n':7, 'init_loca':(3,3), 'init_step':11, 'init_role':0, 'element':{}}, 
            }
        
        # self.__grid_series_strategy = {
        #     4:{'m':7, 'n':7, 'init_loca':(3,3), 'init_step':27, 'init_role':0, 'element':{}},
        #     5:{'m':7, 'n':7, 'init_loca':(3,3), 'init_step':27, 'init_role':1, 'element':{}},
        #     6:{'m':7, 'n':7, 'init_loca':(3,3), 'init_step':27, 'init_role':0, 'element':{}},
        #     7:{'m':7, 'n':7, 'init_loca':(3,3), 'init_step':27, 'init_role':1, 'element':{}},
        #     }

        self.__grid_series_formal = {
            8:{'m':7, 'n':7, 'init_loca':(3,3), 'init_step':11, 'init_role':0, 'element':{}},
            9:{'m':7, 'n':7, 'init_loca':(3,3), 'init_step':11, 'init_role':1, 'element':{}},
            10:{'m':7, 'n':7, 'init_loca':(3,3), 'init_step':11, 'init_role':0, 'element':{}},
            11:{'m':7, 'n':7, 'init_loca':(3,3), 'init_step':11, 'init_role':1, 'element':{}},
            }
        
        self.__choice_opinion = {
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
        
        self.__choice_thinking = {
            1: [
                "哪一项优惠活动在多数情况下更划算？\n\n【X】每购满150元返现50元\n\n【B】全场无门槛8折优惠",
                "住在哪个宿舍，上厕所排队的概率更高？\n\n【X】100个人的宿舍，设置5个厕所坑位\n\n【B】1000个人的宿舍，设置50个厕所坑位",
                "数字1000000（一百万）与下列哪个数字更接近？\n\n【X】10000000（一千万）\n\n【B】0.0000001（一千万分之一）",
                "仅凭人类手工计算，解决以下哪个问题更困难？\n\n【X】判断7081是否是质数\n\n【B】将54289开根号",
                "将一根木棒随机分割为三段，这三段木棒的长度：\n\n【X】能拼成三角形的概率更高\n\n【B】不能拼成三角形的概率更高",
                "二孩家庭中其中一个孩子为男孩，那么：\n\n【X】另一个孩子为女孩的概率为1/2\n\n【B】另一个孩子为女孩的概率不为1/2",
                "下列两台机器，哪台平均寿命更长？\n\n【X】每逢周三都有7%的概率损坏的机器\n\n【B】每天都有1%的概率损坏的机器",
                "下列哪一组数列更有可能是有规律的？\n\n【X】0, 1, 8, 17, 32, 49, 72\n\n【B】0, 1, 8, 17, 18, 26, 27",
                "现有两只烧杯，其容积分别为8L和11L，那么：\n\n【X】用它们量出6L水的步骤更少\n\n【B】用它们量出7L水的步骤更少",
                "花8元买一个瓜以9元卖掉，再以10元买入11元卖出，那么：\n\n【X】赚了1元\n\n【B】赚了2元",
                ]
                }
        
        self.__opinion_guide = '按【X】选择“是”                                按【B】选择“否”\n\n可以修改您的选择，确认无误后再按【LB】。\n\n选项无对错之分，根据真实想法选择即可。'
        self.__opinion_confirm = {'X':'您选择了“是”', 'B':'您选择了“否”'}
        self.__opinion_result = {
            'same':'本轮作答情况：\n\n双方的【相同观点】多于【不同观点】。\n\n请呼唤主试。',
            'diff':'本轮作答情况：\n\n双方的【不同观点】多于【相同观点】。\n\n请呼唤主试。',
        }
        # self.__opinion_result = {
        #     'same':{1:'在上述 13 个问题中，您与对方持有……\n\n相同观点：9个\n不同观点：4个', 
        #             2:'在上述 13 个问题中，您与对方持有……\n\n相同观点：8个\n不同观点：5个', 
        #             3:'在上述 13 个问题中，您与对方持有……\n\n相同观点：10个\n不同观点：3个'},
        #     'diff':{1:'在上述 13 个问题中，您与对方持有……\n\n相同观点：4个\n不同观点：9个', 
        #             2:'在上述 13 个问题中，您与对方持有……\n\n相同观点：5个\n不同观点：8个', 
        #             3:'在上述 13 个问题中，您与对方持有……\n\n相同观点：3个\n不同观点：10个'},
        # }
        self.__opinion_summary = {
            'same':'综合三个阶段的选择结果……\n\n',
            'diff':'综合三个阶段的选择结果……\n\n',
        } #待补充

        self.__thinking_guide = '按【X】或【B】进行选择。\n\n可以修改您的选择，确认无误后再按【LB】。\n\n作答时间会影响测验成绩。'
        self.__thinking_confirm = {'X':'您选择了【X】选项', 'B':'您选择了【B】选项'}
        self.__thinking_result = {
            'same':{0:(
                    '在刚才的测试中，\n\n'
                    '您的得分：75.3958\n '
                    '对方得分：74.6042\n'
                    '\n分数根据正确率和作答时间综合计算得到。\n'
                    '\n测试分数与任务表现有较强关联。'
                    ),
                    1:(
                    '在刚才的测试中，\n\n'
                    '您的得分：74.6042\n '
                    '对方得分：75.3958\n'
                    '\n分数根据正确率和作答时间综合计算得到。\n'
                    '\n测试分数与任务表现有较强关联。'
                    ),},
            'diff':{0:(
                    '在刚才的测试中，\n\n'
                    '您的得分：84.9414\n '
                    '对方得分：65.0586\n'
                    '\n分数根据正确率和作答时间综合计算得到。\n'
                    '\n测试分数与任务表现有较强关联。'
                    ),
                    1:(
                    '在刚才的测试中，\n\n'
                    '您的得分：65.0586\n '
                    '对方得分：84.9414\n'
                    '\n分数根据正确率和作答时间综合计算得到。\n'
                    '\n测试分数与任务表现有较强关联。'
                    ),},
        }

        self.__choice_wait = '请等待对方完成选择...'
        self.__choice_pos = {'content':(0, 0.3), 'guide':(0, -0.1), 'choice':(0, -0.4)}

        self.__discuss_guide = {None:'你们双方的选择恰好完全相同或完全不同。\n请呼唤主试。', 
                                'same':'你们在多数问题上持有相同观点，以下是其中一个：', 
                                'diff':'你们在多数问题上持有不同观点，以下是其中一个：'}
        self.__discuss_choice = {None:' ', 
                                 'X':'您的观点：“是”', 
                                 'B':'您的观点：“否”',
                                 'same_X':'您的观点：是\n对方观点：是',
                                 'same_B':'您的观点：否\n对方观点：否',
                                 'diff_X':'您的观点：是\n对方观点：否',
                                 'diff_B':'您的观点：否\n对方观点：是'}
        self.__discuss_pos = {'guide':(0, 0.3), 
                              'topic':(0, -0.3), 
                              'self':(0, -0.5)}
        
        self.__report_guide = '操作方法...'
        self.__report_wait = '请等待对方完成此阶段...'
        self.__report_pos = {'guide':(0, 0.6),
                             'question':(0, 0.3), 
                             'answers':{1:(0, 0), 2:(0, -0.12), 3:(0, -0.24), 
                                        4:(0, -0.36), 5: (0, -0.48), 6:(0, -0.60),}}
            
    @property
    def resolution(self):
        '''屏幕分辨率。'''
        return self.__resolution
    
    @property
    def win_pos(self):
        '''返回两个窗口的位置。'''
        return self.__win_pos

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
    def grid_series_test(self):
        '''调试阶段的 grid 参数字典。'''
        return self.__grid_series_test
    
    # @property
    # def grid_series_strategy(self):
    #     '''策略水平操纵阶段的 grid 参数字典。'''
    #     return self.__grid_series_strategy
    
    @property
    def grid_series_exercise_1(self):
        '''练习阶段 1 的 grid 参数字典。'''
        return self.__grid_series_exercise_1
    
    @property
    def grid_series_exercise_2(self):
        '''练习阶段 2 的 grid 参数字典。'''
        return self.__grid_series_exercise_2
    
    @property
    def grid_series_exercise_3(self):
        '''练习阶段 3 的 grid 参数字典。'''
        return self.__grid_series_exercise_3
    
    @property
    def grid_series_formal(self):
        '''
        正式实验的 grid 参数字典。
        * 各阶段调用时记得手动调整 grid.stage 参数。
        '''
        return self.__grid_series_formal
    
    @property
    def choice_opinion(self):
        '''特质相似性迫选文本。'''
        return self.__choice_opinion
    
    @property
    def choice_thinking(self):
        '''能力相似性迫选文本。'''
        return self.__choice_thinking
    
    @property
    def opinion_guide(self):
        '''迫选操作指南。'''
        return self.__opinion_guide
    
    @property
    def opinion_confirm(self):
        '''确认迫选选项。'''
        return self.__opinion_confirm
    
    @property
    def opinion_result(self):
        '''特质相似性选择结果。'''
        return self.__opinion_result
    
    @property
    def opinion_summary(self):
        '''特质相似性全阶段总结。'''
        return self.__opinion_summary
    
    @property
    def thinking_guide(self):
        '''迫选操作指南（思维能力）。'''
        return self.__thinking_guide
    
    @property
    def thinking_confirm(self):
        '''确认迫选选项。'''
        return self.__thinking_confirm
    
    @property
    def thinking_result(self):
        '''思维测试结果。'''
        return self.__thinking_result
    
    @property
    def choice_wait(self):
        '''等待对方完成迫选。'''
        return self.__choice_wait
    
    @property
    def choice_pos(self):
        '''选项页面各内容位置参数。'''
        return self.__choice_pos
    
    @property
    def discuss_guide(self):
        '''讨论阶段呈现的文字。'''
        return self.__discuss_guide
    
    @property
    def discuss_choice(self):
        '''讨论阶段呈现的自己的观点。'''
        return self.__discuss_choice

    @property
    def discuss_pos(self):
        '''讨论阶段呈现的文字的位置参数。'''
        return self.__discuss_pos
    
    @property
    def report(self):
        '''主观报告阶段的文本。'''
        return self.__report
    
    @property
    def report_guide(self):
        '''主观报告操作方法文本。'''
        return self.__report_guide
    
    @property
    def report_wait(self):
        '''主观报告等待对方完成文本。'''
        return self.__report_wait
    
    @property
    def report_pos(self):
        '''主观报告页面的文字位置参数。'''
        return self.__report_pos
    
    def random_element(self, grid_series:dict, 
                       step_grid_count:int=6, score_grid_count:int=30):
        '''
        调用 generator.py 模块生成固定的伪随机 bonus element 字典。
        \n！！随机数种子为字典的键 (int)，一旦确定就不要随意修改！！\n
        - grid_series: grid_series_... 字典。
        - step_grid_count: 步数奖励的格子数量。
        - score_grid_count: 分数奖励的格子数量。
        '''
        for i in grid_series.keys():
            bonus_dict = elegen.random_elegen(seed=i, m=grid_series[i]['m'], n=grid_series[i]['n'], 
                                              init_loca=grid_series[i]['init_loca'], 
                                              step_grid_count=step_grid_count, score_grid_count=score_grid_count)
            grid_series[i]['element'] = bonus_dict

    def condit_element(self, grid_series:dict, 
                       element:dict={(-3,6):8, (-4,8):8, (-5,10):8}):
        '''
        调用 generator.py 模块生成固定的伪随机 bonus element 字典。
        \n！！随机数种子为字典的键 (int)，一旦确定就不要随意修改！！\n
        - grid_series: grid_series_... 字典。
        - element: 由各种奖惩格子的 (step,score):count 组成的字典。
        '''
        for i in grid_series.keys():
            bonus_dict = elegen.condit_elegen(seed=i, m=grid_series[i]['m'], n=grid_series[i]['n'],
                                              init_loca=grid_series[i]['init_loca'], element=element)
            grid_series[i]['element'] = bonus_dict

    def strict_element(self, grid_series:dict, 
                       element:dict={(-3,6):7, (-4,8):7, (-5,10):7}):
        '''
        调用 generator.py 模块生成固定的伪随机 bonus element 字典。
        \n！！随机数种子为字典的键 (int)，一旦确定就不要随意修改！！\n
        - grid_series: grid_series_... 字典。
        - element: 由各种奖惩格子的 (step,score):count 组成的字典。
        '''
        for i in grid_series.keys():
            bonus_dict = elegen.strict_elegen(seed=i, m=grid_series[i]['m'], n=grid_series[i]['n'],
                                              init_loca=grid_series[i]['init_loca'], element=element)
            grid_series[i]['element'] = bonus_dict

####

def initialize_config():

    global config
    
    config = Configuration()

    config.condit_element(grid_series=config.grid_series_exercise_3,
                          element={(-4,4):6, (-5,5):6, (-6,6):6, (-7,7):6})
    # config.condit_element(grid_series=config.grid_series_strategy,
    #                       element={(-4,4):6, (-5,5):6, (-6,6):9, (-7,7):9})
    config.condit_element(grid_series=config.grid_series_formal,
                          element={(-4,4):6, (-5,5):6, (-6,6):9, (-7,7):9})

initialize_config()

####

if __name__ == '__main__':

    print(f'\n{type(config)}\n')

    print(config.grid_series_exercise_1[0]['element'])
    print()
    print(config.grid_series_exercise_1[1]['element'])
    print()
    print(config.grid_series_strategy[4]['element'])
