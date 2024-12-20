
'''
根据测验材料呈现规则，自动生成待填色的图形序列参数。
（开发中）

# A/B 类规则评分
allowed_a1 = [(5, 3, 3), (5, 4, 2), (5, 5, 4),
              (6, 3, 2), (6, 4, 4), (6, 5, 3),
              (7, 3, 3), (7, 4, 4), (7, 5, 2),
              (8, 3, 4), (8, 4, 2), (8, 5, 3)] #图形数量，形状种类，颜色种类

allowed_b1 = [(5,2,0,0,0,3,2), (5,3,0,1,0,2,2), (5,4,1,1,0,2,1),
              (6,2,3,0,3,0,0), (6,3,2,0,3,0,1), (6,4,2,0,2,1,1),
              (7,2,0,3,0,4,0), (7,3,1,2,0,4,0), (7,4,1,2,1,3,0),
              (8,2,0,5,0,0,3), (8,3,0,4,1,0,3), (8,4,1,4,1,0,2)] #图形数量，颜色种类，rgbyp数量

allowed_a2 = [(5, 2, 4), (5, 3, 3), (5, 4, 2),
              (6, 2, 3), (6, 3, 4), (6, 4, 2),
              (7, 2, 3), (7, 3, 2), (7, 4, 4),
              (8, 2, 2), (8, 3, 3), (8, 4, 4)] #图形数量，形状种类，颜色种类

allowed_b2 = [(5,2,1,0,0,0,4), (5,3,1,0,0,1,3), (5,4,1,1,0,1,2),
              (6,2,0,4,0,2,0), (6,3,0,3,0,2,1), (6,4,0,2,1,2,1),
              (7,2,0,0,3,4,0), (7,3,0,1,3,3,0), (7,4,1,1,2,3,0),
              (8,2,4,0,4,0,0), (8,3,3,0,4,1,0), (8,4,2,0,4,1,1)] #图形数量，颜色种类，rgbyp数量

步骤：
- 创建一个包含 allowed_a[0] 个图形、allowed_a[1] 种形状的图形序列（列表）。
- 将 allowed_a[2] 种颜色，填入其中 allowed_a[0]-2 个图形中。
    颜色选取：...
- 形成嵌套字典数据结构。
    {0:{'uncolored':(), 'colored':{'cl':[],'tg':[],'sq':[],'dm':[],'pt':[]}}, ....}
'''

import config
import random as rd

def illustrate():

    shapes = ['cl','tg','sq','dm','pt']
    colors = ['r','g','b','y','p']

    # 创建空字典
    graph_dict_stage1 = {}
    graph_dict_stage2 = {}

    # 填入字典，参数为空
    for i in range(len(config.allowed_b1)):
        graph_dict_stage1[i] = {'uncolored':(), 'colored':{'cl':[],'tg':[],'sq':[],'dm':[],'pt':[]}}
    for j in range(len(config.allowed_b2)):
        graph_dict_stage2[i] = {'uncolored':(), 'colored':{'cl':[],'tg':[],'sq':[],'dm':[],'pt':[]}}

    # 读取并随机选取选取形状种类
    for i,j in enumerate(config.allowed_a1): #i:index/key, j:tuple
        selected_shape = rd.sample(shapes, j[1])

    # 读取图形数量，随机分配并创建无色的形状序列
