
class PGG:
    '''
    单个 PGG trial 的底层实现。
    '''

    def __init__(self, total_token:int, multiply:int, 
                 init_contribution_0:int, init_contribution_1:int):
        '''
        - total_token: 双方各持有的总代币数。
        - multiply: 公共池中的代币的返还倍率。
        - init_contribution_x: 双方初始投入公共池的代币数，实验中传入随机数，以防止通过场外因素探知对方的决策。
        '''
        
        self.total_token = total_token
        self.multiply = multiply
        self.contribution_0 = init_contribution_0
        self.contribution_1 = init_contribution_1

    @property
    def trial_public_token(self):
        return self.contribution_0 + self.contribution_1

    @property
    def trial_reservation_0(self):
        return self.total_token - self.contribution_0
    
    @property
    def trial_reservation_1(self):
        return self.total_token - self.contribution_1
    
    @property
    def trial_reward_0(self):
        return self.trial_reservation_0 + self.multiply * self.trial_public_token
    
    @property
    def trial_reward_1(self):
        return self.trial_reservation_1 + self.multiply * self.trial_public_token
    
    @property
    def tester(self):
        return self.__tester
    
class Invest:
    '''
    单个 invest trial 的实现。
    '''
    


if __name__ == '__main__':

    pgg = PGG(total_token=10, multiply=2, init_contribution_0=1, init_contribution_1=9)

    print(
        f'\nreward_0: {pgg.trial_reward_0}'
        f'\nreward_1: {pgg.trial_reward_1}'
        f'\ncontribution_0: {pgg.contribution_0}'
        f'\ncontribution_1: {pgg.contribution_1}'
        )
