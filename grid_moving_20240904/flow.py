
'''
实验流程控制模块。
'''

import kernel
from config import config

def launch():
    
    exp = kernel.Experiment()

    # 信息录入与欢迎界面
    exp.overture()

    # 指导语
    exp.page_pic(filename='welcome.png')
    exp.page_pic(filename='grid_guide_1.png')
    # exp.page_pic(filename='grid_guide_2_clue.png' if exp.Condition_Clue == '1' else 'grid_guide_2_noclue.png')
    exp.page_pic(filename='grid_guide_3_clue.png' if exp.Condition_Clue == '1' else 'grid_guide_3_noclue.png')
    exp.page_pic(filename='grid_guide_4.png')

    # 练习阶段
    exp.page_pic(filename='grid_guide_exercise.png')
    exp.STAGE_task(grid_series=config.grid_series_exercise, stage=0)
    exp.clear_info()

    # 合作任务（设置 1 个阶段）
    exp.page_pic(filename='grid_ready.png')
    exp.STAGE_task(grid_series=config.grid_series_formal, stage=1)

    # 后续实验预测试
    exp.page_pic(filename='opinion_guide_1.png')
    exp.page_pic(filename='opinion_guide_2.png')
    exp.STAGE_opinion(stage=1)
    exp.page_pic(filename='discussion_guide_same.png' if exp.Condition_Topic == '1' else 'discussion_guide_diff.png')
    exp.STAGE_discussion(stage=1, duration=120)

    exp.page_pic(filename='opinion_ready.png')
    exp.STAGE_opinion(stage=2)
    exp.page_pic(filename='discussion_guide_same.png' if exp.Condition_Topic == '1' else 'discussion_guide_diff.png')
    exp.STAGE_discussion(stage=2, duration=120)

    exp.page_pic(filename='opinion_ready.png')
    exp.STAGE_opinion(stage=3)
    exp.page_pic(filename='discussion_guide_same.png' if exp.Condition_Topic == '1' else 'discussion_guide_diff.png')
    exp.STAGE_discussion(stage=3, duration=120)

    # 结束阶段
    exp.finale()

if __name__ == '__main__':

    launch()
