
from scipy.stats import norm

class Scale:
    '''
    记录和处理被试报告的置信度、比例。
    '''

    def __init__(self):

        self.scale = {
            ('exercise', 'confidence', 0): [],
            ('exercise', 'confidence', 1): [],
            ('solo', 'confidence', 0): [],
            ('solo', 'confidence', 1): [],
            ('dual', 'confidence', 0): [],
            ('dual', 'confidence', 1): [],

            ('exercise', 'ratio', 0): [],
            ('exercise', 'ratio', 1): [],
            ('solo', 'ratio', 0): [],
            ('solo', 'ratio', 1): [],
            ('dual', 'ratio', 0): [],
            ('dual', 'ratio', 1): [],
            }
        


    def ADD(self, 
            task_mode:str, report_mode:str, subject:int, 
            value:int
            ):
        '''
        添加一个置信度或比例的值。
        '''
        
        self.scale[(task_mode, report_mode, subject)].append(value)



    def cal_absMean(self, task_mode:str, report_mode:str, subject:int):
        '''
        计算报告置信度、比例绝对值的均值。
        '''

        param_list = self.scale[(task_mode, report_mode, subject)]
        mean = sum(abs(x) for x in param_list) / len(param_list) if param_list else 0

        return mean



class Perf:
    '''
    记录和处理被试判断的表现情况。
    '''

    def __init__(self):

        self.perf = {
            ('exercise', 'confidence', 0):{('b','b'): 0, ('b','w'): 0, ('w','b'): 0, ('w','w'): 0},
            ('exercise', 'confidence', 1):{('b','b'): 0, ('b','w'): 0, ('w','b'): 0, ('w','w'): 0},
            ('solo', 'confidence', 0):{('b','b'): 0, ('b','w'): 0, ('w','b'): 0, ('w','w'): 0},
            ('solo', 'confidence', 1):{('b','b'): 0, ('b','w'): 0, ('w','b'): 0, ('w','w'): 0},
            ('dual', 'confidence', 0):{('b','b'): 0, ('b','w'): 0, ('w','b'): 0, ('w','w'): 0},
            ('dual', 'confidence', 1):{('b','b'): 0, ('b','w'): 0, ('w','b'): 0, ('w','w'): 0},
            ('dual', 'confidence', 'public'):{('b','b'): 0, ('b','w'): 0, ('w','b'): 0, ('w','w'): 0},

            ('exercise', 'ratio', 0):{('b','b'): 0, ('b','w'): 0, ('w','b'): 0, ('w','w'): 0},
            ('exercise', 'ratio', 1):{('b','b'): 0, ('b','w'): 0, ('w','b'): 0, ('w','w'): 0},
            ('solo', 'ratio', 0):{('b','b'): 0, ('b','w'): 0, ('w','b'): 0, ('w','w'): 0},
            ('solo', 'ratio', 1):{('b','b'): 0, ('b','w'): 0, ('w','b'): 0, ('w','w'): 0},
            ('dual', 'ratio', 0):{('b','b'): 0, ('b','w'): 0, ('w','b'): 0, ('w','w'): 0},
            ('dual', 'ratio', 1):{('b','b'): 0, ('b','w'): 0, ('w','b'): 0, ('w','w'): 0},
            ('dual', 'ratio', 'public'):{('b','b'): 0, ('b','w'): 0, ('w','b'): 0, ('w','w'): 0},
        }



    def ADD(self, 
            task_mode:str, report_mode:str, subject:int|str, 
            actual_stim:str, choice:str
            ):
        '''
        添加一个判断结果。
        '''
        
        self.perf[(task_mode, report_mode, subject)][(actual_stim, choice)] += 1



    def cal_d(self, task_mode:str, report_mode:str, subject:int|str):
        '''
        计算 d'，经 Laplace 平滑。
        '''

        count_HT = self.perf[(task_mode, report_mode, subject)][('b', 'b')]
        count_ms = self.perf[(task_mode, report_mode, subject)][('b', 'w')]
        count_fa = self.perf[(task_mode, report_mode, subject)][('w', 'b')]
        count_CR = self.perf[(task_mode, report_mode, subject)][('w', 'w')]

        p_HT = (count_HT + 0.5) / (count_HT + count_ms + 1)
        p_FA = (count_fa + 0.5) / (count_CR + count_fa + 1)

        d = norm.ppf(p_HT) - norm.ppf(p_FA)

        return float(f'{d:.3f}')


    
    def cal_pc(self, task_mode:str, report_mode:str, subject:int|str):
        '''
        计算正确率。
        '''

        count_HT = self.perf[(task_mode, report_mode, subject)][('b', 'b')]
        count_ms = self.perf[(task_mode, report_mode, subject)][('b', 'w')]
        count_fa = self.perf[(task_mode, report_mode, subject)][('w', 'b')]
        count_CR = self.perf[(task_mode, report_mode, subject)][('w', 'w')]

        total = count_HT + count_ms + count_fa + count_CR

        return (count_HT + count_CR) / total if total > 0 else 0



if __name__ == '__main__':

    scale = Scale()
    scale.scale[('exercise', 'confidence', 0)].append(114)
    scale.scale[('exercise', 'confidence', 0)].append(514)
    print(scale.cal_absMean('exercise', 'confidence', 0))
    
    perf = Perf()
    perf.perf[('exercise', 'confidence', 0)][('b','b')] += 1
    perf.perf[('exercise', 'confidence', 0)][('b','w')] += 1
    perf.perf[('exercise', 'confidence', 0)][('w','b')] += 0
    perf.perf[('exercise', 'confidence', 0)][('w','w')] += 2
    print(perf.cal_d('exercise', 'confidence', 0))
    perf.perf[('exercise', 'confidence', 0)][('b','b')] += 15
    perf.perf[('exercise', 'confidence', 0)][('b','w')] += 5
    perf.perf[('exercise', 'confidence', 0)][('w','b')] += 5
    perf.perf[('exercise', 'confidence', 0)][('w','w')] += 15
    print(perf.cal_d('exercise', 'confidence', 0))
    perf.perf[('exercise', 'confidence', 0)][('b','b')] += 18
    perf.perf[('exercise', 'confidence', 0)][('b','w')] += 2
    perf.perf[('exercise', 'confidence', 0)][('w','b')] += 1
    perf.perf[('exercise', 'confidence', 0)][('w','w')] += 19
    print(perf.cal_d('exercise', 'confidence', 0))
    perf.ADD(
        task_mode='exercise', report_mode='confidence', subject=0,
        actual_stim='b', choice='b')
    print(perf.cal_d('exercise', 'confidence', 0))
    perf.ADD(
        task_mode='exercise', report_mode='confidence', subject=0,
        actual_stim='b', choice='w')
    print(perf.cal_d('exercise', 'confidence', 0))