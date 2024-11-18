
'''
自动生成（固定）矩阵 bonus 字典。
'''

import copy
import random as rd

def random_elegen(seed:int, m:int=7, n:int=7, init_loca:tuple=(3,3), step_grid_count:int=6, score_grid_count:int=30):

    '''
    通过指定两类格子的数量，随机生成分数 / 步数奖励字典 {(pos_x, pos_y):(bonus_step, bonus_score)} 。
    使用固定的随机数种子，保证每次生成的随机字典相同。
    - m、n: 矩阵的尺寸。
    - init_loca: 起始位置，排除在可选范围之外。
    - step_grid_count: 步数奖励的格子数量。
    - score_grid_count: 分数奖励的格子数量。
    '''

    if step_grid_count+score_grid_count > m*n:
        raise ValueError('\n奖惩格子数量多余格子总数！\n')
    
    rd.seed(seed)

    # 记录所有坐标，移除起始点，然后随机选取奖励格子（非空格子）。

    whole_pos = []

    for i in range(m):
        for j in range(n):
            whole_pos.append((i,j))

    whole_pos.remove(init_loca)

    chosen = rd.sample(whole_pos, step_grid_count+score_grid_count)

    # 生成步数奖励格子，其余为分数奖励

    step_bonus_list = []
    score_bonus_list = []

    for i in range(step_grid_count): #步数奖励，分数惩罚
        x = rd.randint(1, 4) #步数奖励
        y = -1-x #分数惩罚
        step_bonus_list.append((x,y))
    
    for i in range(score_grid_count): #步数惩罚，分数奖励
        x = rd.randint(-4, -1) #步数惩罚
        y = 1-2*x #分数奖励
        score_bonus_list.append((x,y))

    bonus_list = step_bonus_list + score_bonus_list

    # 将坐标作为键，将键值对随机匹配

    bonus_dict = {}

    for i,j in zip(chosen, bonus_list):

        bonus_dict[i] = j

    # 重设随机数种子

    rd.seed()

    return bonus_dict

def condit_elegen(seed:int, m:int=7, n:int=7, init_loca:tuple=(3,3), 
                   element:dict={(6,-5):2, (5,-5):2, (4,-5):2,
                                 (-1,3):4, (-2,5):4, (-3,7):4, (-4,9):4,}):
    '''
    通过指定特定格子的数量，随机生成分数 / 步数奖励字典 {(pos_x, pos_y):(bonus_step, bonus_score)} 。
    使用固定的随机数种子，保证每次生成的随机字典相同。
    - m、n: 矩阵的尺寸。
    - init_loca: 起始位置，排除在可选范围之外。
    - element: 步数、分数奖惩的数量字典，每类奖惩的个数不能超过 min(m,n)。
    '''
    rd.seed(seed)
    
    bonus_dict = {}
    legal_pos = [(i, j) for i in range(m) for j in range(n) if (i, j) != init_loca]

    for i in element:
        element_pos = rd.sample(legal_pos, element[i])
        for j in element_pos:
            bonus_dict[j] = i
            legal_pos.remove(j)

    rd.seed()
    return bonus_dict

def strict_elegen(seed:int, m:int=7, n:int=7, init_loca:tuple=(3,3), 
                  element:dict={(6,-5):2, (5,-5):2, (4,-5):2,
                                (-1,3):4, (-2,5):4, (-3,7):4, (-4,9):4,}):

    '''
    通过指定特定格子的数量，随机生成分数 / 步数奖励字典 {(pos_x, pos_y):(bonus_step, bonus_score)} 。
    **同类奖惩(step/score)不会位于同一行或同一列。**（暂时未生效）
    使用固定的随机数种子，保证每次生成的随机字典相同。
    - m、n: 矩阵的尺寸。
    - init_loca: 起始位置，排除在可选范围之外。
    - element: 步数、分数奖惩的数量字典，每类奖惩的个数不能超过 min(m,n)。
    '''

    for i in element.values():
        if i > min(m,n):
            raise ValueError(f'某类元素的个数超过了矩阵的尺寸。')
        
    rd.seed(seed)

    global_legal_pos = [(i, j) for i in range(m) for j in range(n) if (i, j) != init_loca] #所有可选位置

    bonus_dict = {}

    for i in element: # i/(step/score)，对同类奖惩进行循环
        local_legal_pos = copy.deepcopy(global_legal_pos) #创建同类 (step/score) 格子的合法选区
        for j in range(element[i]): #j/同类 (step/score) 分数格子
            selected_pos = rd.sample(local_legal_pos, 1)[0]
            bonus_dict[selected_pos] = i # 把坐标和该 (step/score) 奖惩组成键值对，添加到 bonus_dict 中
            local_legal_pos.remove(selected_pos) #从同类 (step/score) 的合法选区中移除抽取的选区（想不通为什么删掉这一行就会报错……）
            global_legal_pos.remove(selected_pos) #从所有合法选区中移除抽取的选区
            for k in local_legal_pos: #k: 当前类的合法坐标。把和该 (step/score) 同行、同列的坐标从同类 (step/score) 合法选区中移除
                if (k[0] == selected_pos[0]) or (k[1] == selected_pos[1]):
                    local_legal_pos.remove(k)

    rd.seed()

    return bonus_dict

if __name__ == '__main__':

    resgen = strict_elegen(seed=11, m=7, n=7, init_loca=(3,3), 
                             element={(4,-5):2, (3,-4):2, (2,-3):2, (1,-2):2,
                                      (-1,3):6, (-2,5):6, (-3,7):6, (-4,9):6,})
    resgen_values = [i for i in resgen.values()]
    resgen_values.sort(key=lambda i:i[0], reverse=True)
    print(resgen)

    test_dict_0 = {0:{'m':7, 'n':7, 'init_loca':(3,3), 'init_step':8, 'init_role':0, 'element':{}},}

    test_dict_1 = {
            0:{'m':7, 'n':7, 'init_loca':(3,3), 'init_step':8, 'init_role':0, 'element':{}},
            1:{'m':7, 'n':7, 'init_loca':(3,3), 'init_step':8, 'init_role':1, 'element':{}},
            2:{'m':7, 'n':7, 'init_loca':(3,3), 'init_step':8, 'init_role':0, 'element':{}},
            3:{'m':7, 'n':7, 'init_loca':(3,3), 'init_step':8, 'init_role':1, 'element':{}},
            }
    
    for i in test_dict_1:
        bonus_dict = strict_elegen(seed=i, m=test_dict_1[i]['m'], n=test_dict_1[i]['n'],
                                     init_loca=test_dict_1[i]['init_loca'])
        test_dict_1[i]['element'] = bonus_dict
    print (test_dict_1)

    # for i in test_dict_1.keys():
    #     bonus_dict = restrict_elegen(seed=i, m=test_dict_1[i]['m'], n=test_dict_1[i]['n'],
    #                                         init_loca=test_dict_1[i]['init_loca'])
    #     test_dict_1[i]['element'] = bonus_dict
    # print(test_dict_1)
