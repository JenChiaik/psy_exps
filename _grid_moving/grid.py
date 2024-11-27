
'''
单个 trial 的底层实现，不包含图形化方法。
'''

import copy
from config import config

class Grid:
    '''
    单个矩阵。
    '''

    def __init__(self, m:int=9, n:int=9, 
                 init_loca:tuple=(4,4), 
                 init_step:int=10, 
                 init_role:int=0, 
                 element:dict=None):
        '''
        初始化矩阵，为矩阵添加奖励格子。
        m: 矩阵的列数（横向格子数量）。
        n: 矩阵的行数（纵向格子数量）。
        element: 有特殊效果的格子，{(pos_x,pos_y):(bonus_score,bonus_steps), ...}，写在 config.py 中。
        核心属性：self.unit_bonus，为 {(#x, #y):(bonus_step, bonus_score), ...} 字典。
        '''

        self.unit_bonus = {} #{(#x, #y):(bonus_step, bonus_score), ...}
        self.frame_size = (m,n)

        self.loca = list(init_loca) #当前位置
        self.role = init_role #当前角色
        self.step = init_step #剩余步数
        self.redeem_count = 0 #使用分数兑换步数的次数（当前 trial）

        self.redeem_score = 3 #重置步数消耗的分数（每个 trial 初始值）
        self.reset_step = 11 #每次重置后步数的变化

        self.wasted_step = 0 #重置步数时浪费掉的步数
        self.wasted = 0 #存在步数浪费的次数（当前 trial）

        self.trial_score_0 = 0 #当前 grid，sub0 得分
        self.trial_score_1 = 0 #当前 grid，sub1 得分

        self.init_role = init_role
        self.init_step = init_step #初始步数
        self.gone_step = 0 #在当前 trial 中行进的真实步数，每次操作 +1

        self.contribution_0 = 0 #sub0 兑换步数的次数
        self.contribution_1 = 0 #sub1 兑换步数的次数

        if all(isinstance(i,int) for i in [m,n,init_loca[0],init_loca[1],init_step,init_role]):
            pass
        else:
            raise ValueError('错误的参数类型。')
        
        if not init_role in [0,1]:
            raise ValueError('错误的角色参数。')

        for i in range(m):
            for j in range(n):
                self.unit_bonus[(i,j)] = (0,0)

        self.__add_element(element)
        
    def __str__(self):
        '''
        仅用于控制台调试。
        '''
        print_str = ''
        for i in self.unit_bonus:
            print_str += f'loc_{i} : score_{self.unit_bonus[i][0]},step_{self.unit_bonus[i][1]}\n'
        return print_str

    def __add_element(self, element:dict):
        '''
        为矩阵特定坐标添加分数和步数。
        element: {(pos_x,pos_y):(bonus_score,bonus_steps), ...}，写在 config.yaml 中。
        * 私有接口，仅在 .__init__ 方法中调用。
        '''
        for i in element.keys():
            if (not i in self.unit_bonus.keys()) or (list(i) == self.loca):
                raise KeyError(f'element_param 中包含非法坐标 {i}')
            else:
                self.unit_bonus[i] = element[i]
                if self.unit_bonus[i][0] > 0:
                    self.total_bonus_step += self.unit_bonus[i][0]
                    self.NUM_total_bonus_step += 1
        
    def rotate(self, stage:int):
        '''
        将矩阵（包含：初始位置、奖励格子、常规格子）逆时针旋转特定度数。
        stage: 实验的阶段，0为练习阶段，1~4为实验阶段；决定了矩阵的旋转角度。
        '''
        init_loca_copy = copy.deepcopy(self.loca)
        ori_x0, ori_y0 = init_loca_copy[0], init_loca_copy[1]    

        grid_dict_copy = copy.deepcopy(self.unit_bonus)
        key_list = [i for i in grid_dict_copy.keys()]

        if stage == 0 or stage == 1: #原始状态
            pass

        elif stage == 2: #逆时针旋转90°
            self.loca = [ori_y0, self.frame_size[0] - 1 - ori_x0]
            for i in key_list:
                ori_x, ori_y = i[0], i[1]
                i = (ori_y, self.frame_size[0] - 1 - ori_x)
                self.unit_bonus[i] = grid_dict_copy[(ori_x,ori_y)]
            self.frame_size = (self.frame_size[1], self.frame_size[0])

        elif stage == 3: #逆时针旋转180°
            self.loca = [self.frame_size[0] - 1 - ori_x0, self.frame_size[1] - 1 - ori_y0]
            for i in key_list:
                ori_x, ori_y = i[0], i[1]
                i = (self.frame_size[0] - 1 - ori_x, self.frame_size[1] - 1 - ori_y)
                self.unit_bonus[i] = grid_dict_copy[(ori_x,ori_y)]

        elif stage == 4: #逆时针旋转270°
            self.loca = [self.frame_size[1] - 1 - ori_y0, ori_x0]
            for i in key_list:
                ori_x, ori_y = i[0], i[1]
                i = (self.frame_size[1] - 1 - ori_y, ori_x)
                self.unit_bonus[i] = grid_dict_copy[(ori_x,ori_y)]
            self.frame_size = (self.frame_size[1], self.frame_size[0])

        else:
            raise ValueError('错误的阶段参数！')
        
    def clear(self):
        '''
        在 trial 结束后，将网矩阵中的所有元素用 (0,0) 覆写。
        （冗余的方法，但保险起见还是保留，防止出现奇奇怪怪的问题。）
        '''
        for i in self.unit_bonus.keys():
            self.unit_bonus[i] = (0,0)

    @property
    def legal_destination(self) -> list:
        '''
        根据当前所在位置，返回可移动的合法坐标元组构成的列表。
        - allow_overdraft: 最后一步是否允许透支步数。
        - strategy_competition：控制结束条件、是否允许重置步数、是否允许主动结束游戏。
        '''

        legal = []

        for i in range(self.frame_size[1]):
            if self.step + self.unit_bonus[(self.loca[0], i)][0] >= 0:
                legal.append((self.loca[0], i))
        if tuple(self.loca) in legal:
            legal.remove(tuple(self.loca))

        for j in range(self.frame_size[0]):
            if self.step + self.unit_bonus[j, self.loca[1]][0] >= 0:
                legal.append((j, self.loca[1]))
        if tuple(self.loca) in legal:
            legal.remove(tuple(self.loca))

        return legal

    @property
    def legal_bonus(self):
        '''
        以列表形式返回所有 legal_destination 坐标对应格子内的(step, score)元组，去重后按照步数排序。
        '''
        bonus_list = []
        for i in self.legal_destination:
            bonus_list.append(self.unit_bonus[i])
        bonus_list = sorted(bonus_list, key=lambda x:x[0], reverse=True)
        return list(set(bonus_list))
        
    def __move(self, orientation:str, length:int):
        '''
        **已废弃的方法，改用 .move_to 。**
            移动方格，获得方格内容，减少剩余步数，转换操作角色。
            orientation: "u", "d", "l", "r".
            int: 朝着该方向移动的距离。
        '''
        if not orientation in ['u','d','l','r']:
            raise ValueError('错误的方向参数。')

        else:

            def execute():
                self.__bonus()
                self.role = 1 if self.role == 0 else 0
                self.step -= 1

            if (orientation == 'u') and (self.loca[1]+length <= self.frame_size[1]-1) and (self.step >= 1):
                self.loca[1] += length
                execute()
            elif (orientation == 'd') and (self.loca[1]-length >= 0) and (self.step >= 1):
                self.loca[1] -= length
                execute()
            elif (orientation == 'l') and (self.loca[0]-length >= 0) and (self.step >= 1):
                self.loca[0] -= length
                execute()
            elif (orientation == 'r') and (self.loca[0]+length <= self.frame_size[0]-1) and (self.step >= 1):
                self.loca[0] += length
                execute()
            else:
                pass

    def move_to(self, destination:tuple, end:bool=False):
        '''
        移动方格至特定坐标点，并执行特定效果。destination: (pos_x, pos_y)。
        - end: False/获取分数或换取步数，True/结束当前 trial。
        - strategy_competition：控制结束条件、是否允许重置步数、是否允许主动结束游戏。
        '''

        if end: #按 RB 结束 trial

            self.wasted += 1 if self.step != 0 else 0
            self.wasted_step += self.step

            # self.trial_score_0 -= self.step
            # self.trial_score_1 -= self.step

            self.step = -1

        else:
            if destination in self.legal_destination:
                self.loca = list(destination)
                self.__bonus()
                self.gone_step += 1
                self.role = 1 if self.role == 0 else 0
        
        # print(f'wasted in this trial(grid): {self.wasted_step}.')

    def __bonus(self):
        '''
        检查当前方格是否有分数或步数奖励。
        如果走向非空格子，获得步数或分数奖惩（当前角色），并将 self.grid_dict 对应的值变更为 (0,0)。
        如果走向空格子，则立即结束当前回合。
        - end: False/获取分数或换取步数，True/结束当前 trial。
        * 私有方法，仅在 .move_to 中调用。
        '''
        if self.unit_bonus[tuple(self.loca)] != (0,0): #得分

            bonus_step, bonus_score = self.unit_bonus[tuple(self.loca)]

            self.step += bonus_step
            self.trial_score_0 += bonus_score if self.role == 0 else 0
            self.trial_score_1 += bonus_score if self.role == 1 else 0

            self.unit_bonus[tuple(self.loca)] = (0,0)

        else: #兑换步数

            self.wasted += 1 if self.step != 0 else 0
            self.wasted_step += self.step

            # self.trial_score_0 -= self.step
            # self.trial_score_1 -= self.step

            self.trial_score_0 -= self.redeem_score if self.role == 0 else 0
            self.trial_score_1 -= self.redeem_score if self.role == 1 else 0

            self.contribution_0 += 1 if self.role == 0 else 0
            self.contribution_1 += 1 if self.role == 1 else 0

            self.step = self.reset_step

            self.redeem_score += 1 #重置步数的分数消耗增加 1
            self.redeem_count += 1
        
        # print(f'count:{self.redeem_count}, cost:{self.redeem_score}')
        # print (f'score_0:{self.trial_score_0}, score_1:{self.trial_score_1}')

# 测试

if __name__ == '__main__':

    from config import config

    print(config.grid_series_exercise_1[0])
    print(config.grid_series_exercise_1[1])
    