'''
用于保存硬件配置信息，以及实验时间控制、文字材料、图形序列、键盘按键等配置信息的模块。\n
    keys: 以字符串、列表或字典形式存储的可接受按键。
    graph: 以嵌套字典（index: {'uncolored':('shape',...), 'colored':{'shape':['color'...]...}}）形式存储的图形属性。
    text: 以字典（'stage_name' : 'text_content'）形式存储的文本信息。
    intermezzo: 以字典（'stage':(duration, 'text')）形式存储的持续时间、提示文本信息。
    allowed_a: 以列表（(length, shape_type, color_type)）形式存储的得分条件A。
    allowed_b: 以列表（(length, color_type, r_count, g_count, b_count, y_count, p_count）形式存储的得分条件B。
'''

# res_conductor, res_subjects = (2048,1152), (2560,1440)
res_conductor, res_subjects = (1920,1080), (1920,1080) #双屏调试
# res_conductor, res_subjects = (1600,900), (3840,2160) #三屏调试

keys_nextpage = 'return' #主试操作页面
keys_operation = ['space','return','left','right','up','down'] #仅供键盘调试
keys_color_picker = {'up':'up','down':'down'} #仅供键盘调试
keys_shape_picker = {'left':'left', 'right':'right'} #仅供键盘调试
keys_coloring = 'space' #仅供键盘调试

# 静态页面最小时间
wait_text, wait_break = 0, 0
# min_time_text, min_time_break = 5, 5

# 静态页面：文字
text_dict = {
             'intr_welcome':'''
欢迎您参加本次实验。
为了让您顺利地完成本研究，请您仔细阅读以下指导语，并聆听主试的介绍。

这是一个有关合作学习的研究。

在这次实验中，您的目标是与对方合作学习一组图形填色规则。
然后，您与对方将根据学习到的规则，分别独立完成一项图形填色测验。

（当前由主试控制翻页）
''',

             'intr_1_1':'''
（1）您获得的学习材料与对方获得的学习材料是完全不同的，但它们都反映了图形填色规则的一部分。
（2）在完成了独立学习、共同学习之后，您与对方将分别独立完成图形填色测验。
（3）想要在测验中得到高分，您需要同时运用双方所学习的规则。

（当前由主试控制翻页）
''',

             'intr_1_2_1':'''
当你们双方分别独自完成填色测验后，您与对方将分别得到一个测验分数。
（1）如果您与对方同时达到了我们预先设定的合格分，您与对方都可以获得额外的被试费作为奖励。
（2）如果您或对方中的任何一方没有达到我们预先设定的合格分，则您与对方都无法获得额外的被试费奖励。

（当前由主试控制翻页）
''',

             'intr_1_2_2':'''
当你们双方分别独自完成填色测验后，您与对方将分别得到一个测验分数。
（1）如果您达到了我们预先设定的合格分，并且您的得分比对方更高，则您可以获得额外的被试费作为奖励。
（2）如果您没有达到我们预先设定的合格分，则无论如何，您也无法获得额外的被试费奖励。

（当前由主试控制翻页）
''',

             'intr_1_3':'''
在开始学习之前，让我们先来熟悉一下填色测验的操作方法吧。
（1）拿起手柄，根据主试的提示，找到【A】、【B】、【back】、【LB】、【RB】、【LS】这几个键。
（2）用舒适的姿势握持住手柄，然后完成接下来的练习阶段，以熟悉手柄的操作方式。
（3）在练习阶段中，您可以用任意颜色填充图形序列，对您的任务表现没有任何影响。

（当前由主试控制翻页）
''',

             'intr_2_1':'''
接下来，是新的一轮任务。
与上一阶段相同，您首先需要独自学习填色规则，然后与对方交流整合规则，最后独立完成填色测验。
             
（当前由主试控制翻页）
''',

             'intr_2_2_1':'''
您在这个阶段的得分将与上一阶段的得分叠加。
两阶段叠加后的分数将成为您的最终分数，它决定了您最终是否能获得额外被试费奖励。

（1）如果您与对方的最终分数同时达到了我们预先设定的合格分，您与对方都可以获得额外的被试费作为奖励。
（2）如果您或对方中的任何一方的最终分数没有达到我们预先设定的合格分，则您与对方都无法获得额外的被试费奖励。

（当前由主试控制翻页）
''',

             'intr_2_2_2':'''
您在这个阶段的得分将与上一阶段的得分叠加。
两阶段叠加后的分数将成为您的最终分数，它决定了您最终是否能获得额外被试费奖励。

（1）如果您的最终分数达到了我们预先设定的合格分，并且您的最终分数比对方更高，则您可以获得额外的被试费作为奖励。
（2）如果您的最终分数没有达到我们预先设定的合格分，则无论如何，您也无法获得额外的被试费奖励。
             
（当前由主试控制翻页）
''',

             'intr_2_3':'''
请注意，本轮填色任务的得分规则与上一阶段完全不同。
您与对方需要重新学习它们，并将其应用在本阶段的填色测验中。
             
（当前由主试控制翻页）
''',

             'operation_guide':'''             
（1）切换形状：按【LB】和【RB】键。
（2）切换颜色：按【A】和【B】键。

（3）填入颜色：选定形状和颜色后，按【back】键填入颜色。
    （3.1）已预先填色的图形标有“固定颜色”标签，它们不能被染色。
    （3.2）在翻页之前，您可以随时修改您填入的颜色。

（4）所有形状都填充了颜色后，按【左摇杆 LS】键进入下一页。
''',

             'prelude_scan':'''
接下来是持续时间1分钟的静息态扫描...
在翻入下一页之后，请您：
    闭眼静息，保持思绪平静，尽量不要思考任何事情。
1分钟结束时，主试会提醒您睁眼。

（当前由主试控制翻页）
''',

             'prelude_indiv':'''
独立学习阶段（3分钟）即将开始...
请做好准备。

（当前由主试控制翻页）
''',

             'prelude_coop':'''
独立学习阶段已结束。
交流讨论阶段（5分钟）即将开始...
请面向对方，做好互动交流的准备。

（当前由主试控制翻页）
''',

             'prelude_test':'''
合作学习阶段现在已结束。
请您与对方停止交流，面对屏幕，等待测验开始。

（当前由主试控制翻页）
''',
             
             'wait':'''
您已完成当前阶段的测验。
请您耐心等待下一学习阶段开始...
             ''',

             'fake_score_high':'''
合格线：1.00 分

您的得分：1.21 分
对方得分：1.17 分

（这是经过转化处理后的分数。）
''',

             'fake_score_low':'''
合格线：1.00 分

您的得分：1.17 分
对方得分：1.21 分

（这是经过转化处理后的分数。）
''',
             }

# 时限页面：时间与文字
intermezzo_dict = {'rest':[60, '静息阶段（1分钟）'],
                   'indv':[180, '独立学习阶段（3分钟）\n现在，请您独自学习您手中的填色规则，为接下来与对方交流做准备。\n接下来的交流过程中，您将与对方共同总结规则。'],
                   'coop':[300, '合作学习阶段（5分钟）\n现在，请您与对方共同交流所学习到的填色规则，为接下来的测试做准备。\n接下来的测试包含你们双方学习的全部规则。'],
                   'end': [3, '实验已结束。\n感谢您的参与。'],
                   '_test_':[2, 'intermezzo 阶段测试。']}
## 测试实验程序时将 intermezzo 页面限时
for i in intermezzo_dict.keys():
    intermezzo_dict[i][0] = 3

# A/B 类得分条件
allowed_a1 = [(5, 3, 3), (5, 4, 2), (5, 5, 4),
              (6, 3, 2), (6, 4, 4), (6, 5, 3),
              (7, 3, 3), (7, 4, 4), (7, 5, 2),
              (8, 3, 4), (8, 4, 2), (8, 5, 3)] #图形数量，形状种类，颜色种类

allowed_b1 = [(5,2,0,0,0,3,2), (5,3,0,1,0,2,2), (5,4,1,1,0,2,1),
              (6,2,3,0,3,0,0), (6,3,2,0,3,0,1), (6,4,2,0,2,1,1),
              (7,2,0,3,0,4,0), (7,3,1,2,0,4,0), (7,4,1,2,1,3,0),
              (8,2,0,5,0,0,3), (8,3,0,4,1,0,3), (8,4,1,4,1,0,2)] #图形数量，*颜色种类，rgbyp数量
# *颜色种类字段是冗余的，但代码不想重构了，能跑就行

allowed_a2 = [(5, 3, 4), (5, 4, 3), (5, 5, 2),
              (6, 3, 3), (6, 4, 4), (6, 5, 2),
              (7, 3, 3), (7, 4, 2), (7, 5, 4),
              (8, 3, 2), (8, 4, 3), (8, 5, 4)] #图形数量，形状种类，颜色种类

allowed_b2 = [(5,2,1,0,0,0,4), (5,3,1,0,0,1,3), (5,4,1,1,0,1,2),
              (6,2,0,4,0,2,0), (6,3,0,3,0,2,1), (6,4,0,2,1,2,1),
              (7,2,0,0,3,4,0), (7,3,0,1,3,3,0), (7,4,1,1,2,3,0),
              (8,2,4,0,4,0,0), (8,3,3,0,4,1,0), (8,4,2,0,4,1,1)] #图形数量，颜色种类，rgbyp数量

# 待填色的图形序列
graph_dict_exercise = {
    0:{'uncolored':('tg','pt'), 'colored':{'tg':['r'],'pt':['b','r'],'dm':[],'cl':['r'],'sq':['b']}},
    1:{'uncolored':('cl','cl'), 'colored':{'tg':['r'],'pt':['b','r'],'dm':[],'cl':[],'sq':[]}},
    2:{'uncolored':('pt','pt'), 'colored':{'tg':['r'],'pt':['r'],'dm':['r'],'cl':['r'],'sq':['r','r']}},
    3:{'uncolored':('pt','dm'), 'colored':{'tg':['r'],'pt':['r','r'],'dm':['g'],'cl':['r'],'sq':['r']}},
    4:{'uncolored':('dm','dm'), 'colored':{'tg':['r'],'pt':['y','r'],'dm':[],'cl':[],'sq':[]}},
    5:{'uncolored':('tg','cl'), 'colored':{'tg':['y','b'],'pt':['b'],'dm':[],'cl':['r','b'],'sq':['y']}},
    6:{'uncolored':('dm','pt'), 'colored':{'tg':['y','b'],'pt':[],'dm':[],'cl':['r','b'],'sq':[]}},
    7:{'uncolored':('sq','dm'), 'colored':{'tg':['y','b'],'pt':['b'],'dm':[],'cl':['g','b'],'sq':['y']}},
    8:{'uncolored':('cl','sq'), 'colored':{'tg':['p'],'pt':['b'],'dm':[],'cl':['r','b'],'sq':['y']}},
    9:{'uncolored':('dm','tg'), 'colored':{'tg':['p','b'],'pt':['b'],'dm':[],'cl':['r','b'],'sq':['y']}},
    }

graph_dict_stage1 = {
    0:{'uncolored':('cl','dm'), 'colored':{'cl':['p'],'tg':[],'sq':[],'dm':['y'],'pt':['y']}},
    1:{'uncolored':('sq','tg'), 'colored':{'cl':[],'tg':['y'],'sq':[],'dm':['y'],'pt':['p']}},
    2:{'uncolored':('pt','dm'), 'colored':{'cl':['y'],'tg':['p'],'sq':['y'],'dm':[],'pt':[]}},
    3:{'uncolored':('cl','pt'), 'colored':{'cl':['r'],'tg':['b'],'sq':[],'dm':[],'pt':['b','r']}},
    4:{'uncolored':('sq','tg'), 'colored':{'cl':['b'],'tg':['r','r'],'sq':[],'dm':['b'],'pt':[]}},
    5:{'uncolored':('cl','dm'), 'colored':{'cl':[],'tg':['r','r'],'sq':['b'],'dm':[],'pt':['b']}},
    6:{'uncolored':('dm','pt'), 'colored':{'cl':['g','g'],'tg':[],'sq':[],'dm':['y'],'pt':['y','y']}},
    7:{'uncolored':('sq','sq'), 'colored':{'cl':['y'],'tg':['g','y'],'sq':['y'],'dm':[],'pt':['g']}},
    8:{'uncolored':('cl','tg'), 'colored':{'cl':['g'],'tg':['y'],'sq':['y'],'dm':['g'],'pt':['y']}},
    9:{'uncolored':('cl','pt'), 'colored':{'cl':['g','p','p'],'tg':[],'sq':['g','g','g'],'dm':[],'pt':[]}},
    10:{'uncolored':('pt','tg'), 'colored':{'cl':['p'],'tg':['g'],'sq':[],'dm':['p','g'],'pt':['g','g']}},
    11:{'uncolored':('sq','sq'), 'colored':{'cl':['p'],'tg':['g','p'],'sq':['g'],'dm':['g'],'pt':['g']}},
    }

graph_dict_stage2 = {
    0:{'uncolored':('tg','pt'), 'colored':{'cl':[],'tg':['r','p'],'sq':['p'],'dm':[],'pt':[]}},
    1:{'uncolored':('cl','cl'), 'colored':{'cl':[],'tg':[],'sq':['r'],'dm':['p'],'pt':['p']}},
    2:{'uncolored':('sq','cl'), 'colored':{'cl':[],'tg':['p'],'sq':[],'dm':['r'],'pt':['p']}},
    3:{'uncolored':('dm','tg'), 'colored':{'cl':['g','y'],'tg':['g','y'],'sq':[],'dm':[],'pt':[]}},
    4:{'uncolored':('dm','dm'), 'colored':{'cl':['g'],'tg':['y'],'sq':[],'dm':['g'],'pt':['y']}},
    5:{'uncolored':('sq','pt'), 'colored':{'cl':['y','g'],'tg':['g'],'sq':[],'dm':['y'],'pt':[]}},
    6:{'uncolored':('pt','dm'), 'colored':{'cl':['b','b'],'tg':[],'sq':[],'dm':[],'pt':['y','y','y']}},
    7:{'uncolored':('cl','pt'), 'colored':{'cl':['y','b'],'tg':['y','y'],'sq':['b'],'dm':[],'pt':[]}},
    8:{'uncolored':('tg','tg'), 'colored':{'cl':['b','b'],'tg':[],'sq':['y'],'dm':['y'],'pt':['y']}},
    9:{'uncolored':('tg','sq'), 'colored':{'cl':[],'tg':['r','b'],'sq':['b','r'],'dm':['b','b'],'pt':[]}},
    10:{'uncolored':('sq','pt'), 'colored':{'cl':['b'],'tg':[],'sq':[],'dm':['r','b','b','b'],'pt':['r']}},
    11:{'uncolored':('dm','cl'), 'colored':{'cl':['b'],'tg':['b'],'sq':['r','r','r'],'dm':[],'pt':['r']}},
    }

# graph_dict_exercise = {
#     0:{'uncolored':('tg','pt'), 'colored':{'tg':['r'],'pt':['b','r'],'dm':[],'cl':['y'],'sq':['b']}},
#     1:{'uncolored':('cl','cl'), 'colored':{'tg':['r'],'pt':['b','g'],'dm':[],'cl':[],'sq':[]}}
#     } # 测试用短 GS

# graph_dict_stage1 = {
#     0:{'uncolored':('cl','dm'), 'colored':{'cl':['p'],'tg':[],'sq':[],'dm':['y'],'pt':['y']}},
#     1:{'uncolored':('sq','tg'), 'colored':{'cl':[],'tg':['y'],'sq':[],'dm':['y'],'pt':['p']}},
#     2:{'uncolored':('pt','dm'), 'colored':{'cl':['y'],'tg':['p'],'sq':['y'],'dm':[],'pt':[]}},
#     3:{'uncolored':('cl','pt'), 'colored':{'cl':['r'],'tg':['b'],'sq':[],'dm':[],'pt':['b','r']}},
#     } # 测试用短 GS

# graph_dict_stage2 = {
#     0:{'uncolored':('tg','pt'), 'colored':{'cl':[],'tg':['r','p'],'sq':['p'],'dm':[],'pt':[]}},
#     1:{'uncolored':('cl','cl'), 'colored':{'cl':[],'tg':[],'sq':['r'],'dm':['p'],'pt':['p']}},
#     2:{'uncolored':('sq','cl'), 'colored':{'cl':[],'tg':['p'],'sq':[],'dm':['r'],'pt':['p']}},
#     3:{'uncolored':('dm','tg'), 'colored':{'cl':['g','y'],'tg':['g','y'],'sq':[],'dm':[],'pt':[]}},
#     } # 测试用短 GS

# allowed 合法性校验

if __name__ == '__main__':

    from graph import GraphSeries

    for j,i in enumerate(allowed_b1):
        if i[0] != sum(i[2:7]):
            raise ValueError(f'wrong_1!@b1_{j+1}')
        
    for j,i in enumerate(allowed_b1):
        colors = 0
        for k in i[2:7]:
            if k != 0:
                colors += 1
        if colors != i[1]:
            raise ValueError(f'wrong_2!@b1_{j}')
        
    for j,i in enumerate(graph_dict_stage1):
        graph_series = GraphSeries(*graph_dict_stage1[i]['uncolored'], **graph_dict_stage1[i]['colored']).graph_series
        graphs_count = 0
        shapes_list = []
        colors_list = []
        for k in graph_series:
            graphs_count += 1
            shapes_list.append(k[0])
            colors_list.append(k[1])
        if (graphs_count != allowed_a1[j][0]) \
            or (len(set(shapes_list)) != allowed_a1[j][1]) \
            or (len(set(colors_list))) != 3: # None也是一种颜色
            raise ValueError(f'wrong_3@b1_{j}')

    print ('\nb1 all right.\n')

    for j,i in enumerate(allowed_b2):
        if i[0] != sum(i[2:7]):
            raise ValueError(f'wrong_1!@b2_{j+1}')
        
    for j,i in enumerate(allowed_b2):
        for i in allowed_b1:
            colors = 0
            for k in i[2:7]:
                if k != 0:
                    colors += 1
        if colors != i[1]:
            raise ValueError(f'wrong_2!@b2_{j}')
        
    for j,i in enumerate(graph_dict_stage2):
        graph_series = GraphSeries(*graph_dict_stage2[i]['uncolored'], **graph_dict_stage2[i]['colored']).graph_series
        graphs_count = 0
        shapes_list = []
        colors_list = []
        for k in graph_series:
            graphs_count += 1
            shapes_list.append(k[0])
            colors_list.append(k[1])
        if (graphs_count != allowed_a2[j][0]) \
            or (len(set(shapes_list)) != allowed_a2[j][1]) \
            or (len(set(colors_list))) != 3: # None也是一种颜色
            raise ValueError(f'wrong_3@b2_{j}')
        
    print ('\nb2 all right.\n') 


