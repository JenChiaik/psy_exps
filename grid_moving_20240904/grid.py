
'''
单个 trial 的底层实现，不包含图形化方法。
'''

import copy
import ruamel.yaml as yaml

class Grid:
    '''
    单个 trial 矩阵。
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

        self.trial_score_0 = 0 #sub0 得分
        self.trial_score_1 = 0 #sub1 得分

        self.init_role = init_role
        self.init_step = init_step #初始步数
        self.gone_step = 0 #在当前 trial 中行进的真实步数，每次操作 +1

        self.total_bonus_step = 0 #矩阵中总步数奖励之和，在初始化 grid 阶段就确定了，不会随着操作改变
        self.get_bonus_step = 0 #在当前 trial 中获得的步数奖励之和，随着操作而改变
        self.get_bonus_step_0, self.get_bonus_step_1 = 0, 0

        self.NUM_total_bonus_step = 0 #包含步数奖励的总格子数量，在初始化 grid 阶段就确定了，不会随着操作改变
        self.NUM_get_bonus_step = 0 #在当前 grid 中获得步数奖励的次数，随着操作而改变
        self.NUM_get_bonus_step_0, self.NUM_get_bonus_step_1 = 0, 0

        # self.coop_count_0, self.race_count_0 = 0, 0 #已废弃
        # self.coop_count_1, self.race_count_1 = 0, 0 #已废弃

        # self.coop_score_0, self.race_score_0 = 0, 0 #已废弃
        # self.coop_score_1, self.race_score_1 = 0, 0 #已废弃

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
    def legal_loca(self) -> list:
        '''
        根据当前所在位置，返回可移动的合法坐标元组构成的列表。
        '''
        pos_row = [(i, self.loca[1]) for i in range(self.frame_size[0])]
        pos_col = [(self.loca[0], i) for i in range(self.frame_size[1])]
        legal = list(set(pos_col + pos_row))
        legal.remove(tuple(self.loca))
        return legal
    
    @property
    def legal_bonus(self):
        '''
        以列表形式返回所有 legal_loaa 坐标对应格子内的(step,score)元组，去重后按照步数排序。
        '''
        bonus_list = []
        for i in self.legal_loca:
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

    def move_to(self, destination:tuple):
        '''
        移动方格至特定坐标点，获得方格内容，减少剩余步数，转换操作角色。
        destination: (pos_x, pos_y)
        '''
        if destination in self.legal_loca:
            self.loca = list(destination)
            self.__bonus()
            self.role = 1 if self.role == 0 else 0
            self.gone_step += 1
            self.step -= 1

    def __bonus(self):
        '''
        检查当前方格是否有分数或步数奖励。
        如果有，获得步数或分数奖惩（当前角色），并将 self.grid_dict 对应的值变更为 (0,0)。
        * 私有方法，仅在 .move_to 中调用。
        '''
        if not self.unit_bonus[tuple(self.loca)] == (0,0):

            bonus_step, bonus_score = self.unit_bonus[tuple(self.loca)]

            # 增加奖励步数
            self.step += bonus_step

            self.get_bonus_step += bonus_step if self.unit_bonus[tuple(self.loca)][0] > 0 else 0
            self.get_bonus_step_0 += bonus_step if (self.unit_bonus[tuple(self.loca)][0] > 0 and self.role == 0) else 0
            self.get_bonus_step_1 += bonus_step if (self.unit_bonus[tuple(self.loca)][0] > 0 and self.role == 1) else 0

            self.NUM_get_bonus_step += 1 if self.unit_bonus[tuple(self.loca)][0] > 0 else 0
            self.NUM_get_bonus_step_0 += 1 if (self.unit_bonus[tuple(self.loca)][0] > 0 and self.role == 0) else 0
            self.NUM_get_bonus_step_1 += 1 if (self.unit_bonus[tuple(self.loca)][0] > 0 and self.role == 1) else 0

            # 增加奖励分数
            self.trial_score_0 += bonus_score if self.role == 0 else 0
            self.trial_score_1 += bonus_score if self.role == 1 else 0

            # 累计合作/对抗次数/分数
            # if (self.unit_bonus[tuple(self.loca)][0] >= 1) and (self.unit_bonus[tuple(self.loca)][1] <= 0):
            #     self.coop_count_0 += 1 if self.role == 0 else 0
            #     self.coop_count_1 += 1 if self.role == 1 else 0
            #     self.coop_score_0 += bonus_step if self.role == 0 else 0
            #     self.coop_score_1 += bonus_step if self.role == 1 else 0
            # elif (self.unit_bonus[tuple(self.loca)][0] <= 0) and (self.unit_bonus[tuple(self.loca)][1] >= 1):
            #     self.race_count_0 += 1 if self.role == 0 else 0
            #     self.race_count_1 += 1 if self.role == 1 else 0
            #     self.race_score_0 += bonus_step if self.role == 0 else 0
            #     self.race_score_1 += bonus_step if self.role == 1 else 0

            self.unit_bonus[tuple(self.loca)] = (0,0)
        else:
            pass

# 测试

if __name__ == '__main__':

    test = {(1,4):(2,0), (1,8):(2,3), (8,8):(-3,4), (8,2):(-1,4)}
    # a = Grid(element=test)
    # print(a)

    # try:
    #     grid2 = Grid(m=5, n=5, element=test)
    # except:
    #     print('grid2: anticipated error.')

    # try:
    #     grid3 = Grid(element={(4,4):(-1,2)})
    # except:
    #     print('grid3: anticipated error.')

    # print()

    def state(grid:Grid):
        print(f'loca:{grid.loca}, role:{grid.role}, step:{grid.step}, a:b={grid.trial_score_0}:{grid.trial_score_1}')

    def check_bonus(grid:Grid):
        print_str = ''
        if all (i == (0,0) for i in grid.unit_bonus.values()):
            print ('no bonus point left.\n')
            return
        for i,j in grid.unit_bonus.items():
            if not j == (0,0):
                print_str += f'____@loca{i}_has_bonus_{grid.unit_bonus[i]}\n'
        print (print_str)

    print('\n创建矩阵')
    b = Grid(m=10, n=9, element=test, init_role=1, init_loca=(4,4), init_step=7)
    state(b), check_bonus(b)
    # print(b.frame_size), print(), check_bonus(b)
    print('............................')
    print(b.NUM_total_bonus_step, b.NUM_get_bonus_step)
    print(b.legal_bonus)

    print('\n旋转矩阵')
    b.rotate(stage=0)
    # print(b.frame_size), print(), check_bonus(b)

    print('\nmove#1')
    b.move_to((1,4))
    # state(b), check_bonus(b)

    print('\nmove#2')
    b.move_to((1,2))
    # state(b), check_bonus(b)

    print('\nmove#3')
    b.move_to((8,2))
    b.move_to((0,6))
    # state(b), check_bonus(b)

    print('\nmove#4')
    b.move_to((8,8))
    # state(b), check_bonus(b)

    print('\nmove#5')
    b.move_to((1,8))
    # state(b), check_bonus(b)
    print(b.legal_loca)

    print('............................')
    print(b.NUM_total_bonus_step, b.NUM_get_bonus_step)

    print('\n--------\n')
    print(b)
