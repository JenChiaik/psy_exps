'''
图形填色计分模块。
'''

from graph import GraphSeries

import random as rd
import collections as cl
import config

# GraphSeires.graph_series 列表元素：
# ['shape','color','True/False']

def dec(gs:GraphSeries):
    '''
    解构图形序列特征，包含：
        [0]图形序列的长度。
        [1]形状种类数量，[2]形状计数字典。
        [3]颜色种类数量，[4]颜色计数字典。
    并返回上述值。
    '''
    shapes = [i[0] for i in gs.graph_series]
    colors = [i[1] for i in gs.graph_series]
    return (len(gs.graph_series), 
            len(cl.Counter(shapes)), cl.Counter(shapes), 
            len(cl.Counter(colors)), cl.Counter(colors))

def rule_a(gs:GraphSeries, stage:int):
    '''
    判断图形序列包含的颜色种类数量是否得分。
    （取决于图形序列包含的形状种类。）
        stage: 0/1/2，实验阶段。
    返回 0/1。
    '''
    if stage == 1:
        allowed = config.allowed_a1
    elif stage == 2:
        allowed = config.allowed_a2
    elif stage == 0:
        return -1
    else:
        raise ValueError('stage参数错误！')
    gs_dec = dec(gs)
    gs_att = (gs_dec[0], gs_dec[1], gs_dec[3])
    if gs_att in allowed:
        return 1
    else:
        return 0

def rule_b(gs:GraphSeries, stage:int):
    '''
    判断图形序列包含的颜色数量组合是否得分。
    （取决于图形序列包含的颜色种类）
        stage: 0/1/2，实验阶段。
    返回 0/1。
    '''
    if stage == 1:
        allowed = config.allowed_b1
    elif stage == 2:
        allowed = config.allowed_b2
    elif stage == 0:
        return -1
    else:
        raise ValueError('stage参数错误！')
    gs_dec = dec(gs)
    gs_att = (gs_dec[0], gs_dec[3], 
              gs_dec[4].get('r',0), gs_dec[4].get('g',0), 
              gs_dec[4].get('b',0), gs_dec[4].get('y',0), 
              gs_dec[4].get('p',0))
    if gs_att in allowed:
        return 1
    else:
        return 0
    
def metric(gs:GraphSeries, stage:int):
    '''
    返回总分、rule_a分、rule_b分元组。
    '''
    a = rule_a(gs, stage)
    b = rule_b(gs, stage)
    return (a+b, a, b)

if __name__ == '__main__':

    gs0 = GraphSeries(sq=['g','g','y'], tg=['y'], cl=['g'])
    print(metric(gs0, 1)) #不满足任何条件

    gs1 = GraphSeries(sq=['y','b','p'], tg=['y'], cl=['p'])
    print(metric(gs1, 1)) #仅满足 a / 5图形 / 3形状 / 3颜色

    gs2 = GraphSeries(sq=['y','y','p'], tg=['y','p'])
    print(metric(gs2, 1)) #仅满足 b / 5图形 / 3y2p

    gs3 = GraphSeries(sq=['y','g','p'], tg=['p'], cl=['y'])
    print(metric(gs3, 1)) #同时满足 a、b 5图形 / 2形状 / 3颜色 / 1g2y2p
