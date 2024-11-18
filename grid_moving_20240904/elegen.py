
'''
自动生成（固定）矩阵 bonus 字典。
'''

import random as rd

def gen_bonus(seed:int, m:int=9, n:int=9, init_loca:tuple=(4,4), ele_ratio_rev:float=2.0, step_ratio_rev:float=6.0):
    '''
    随机生成分数 / 步数奖励字典 {(pos_x, pos_y):(bonus_step, bonus_score)} 。
    使用固定的随机数种子，保证每次生成的随机字典相同。
    - ele_ratio_rev: 奖励格子（非空格子）占总格子数量比例的倒数，2.0 表示占 1/2。
    - step_ratio_rev: 步数奖励格子占奖励格子（非空格子）数量比例的倒数，6.0 表示占 1/6，设为极大值可以移除所有步数奖励格子。
    '''

    rd.seed(seed)

    # 记录所有坐标，移除起始点，然后随机选取奖励格子（非空格子）。

    whole_pos = []

    for i in range(m):
        for j in range(n):
            whole_pos.append((i,j))

    whole_pos.remove(init_loca)

    chosen = rd.sample(whole_pos, int((m*n)//ele_ratio_rev))

    # 生成步数奖励格子，其余为分数奖励

    step_bonus_count = int(len(chosen) // step_ratio_rev)
    score_bonus_count = int(len(chosen) - step_bonus_count)

    step_bonus_list = []
    score_bonus_list = []

    for i in range(step_bonus_count): #步数奖励，分数惩罚
        x = rd.randint(2, 4) #步数奖励
        y = -x-1 #分数惩罚
        step_bonus_list.append((x,y))
    
    for i in range(score_bonus_count): #步数惩罚，分数奖励
        x = rd.randint(1, 4)*2 + 1 #分数奖励
        y = 1-x//2 #步数惩罚
        score_bonus_list.append((y,x))

    bonus_list = step_bonus_list + score_bonus_list

    # 将坐标作为键，将键值对随机匹配

    bonus_dict = {}

    for i,j in zip(chosen, bonus_list):

        bonus_dict[i] = j

    # 重设随机数种子

    rd.seed()

    return bonus_dict

if __name__ == '__main__':

    print (gen_bonus(seed=114514))

