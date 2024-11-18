
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
    exp.page_pic(filename='0_welcome_trait.png')
    # exp.page_pic(filename='0_welcome_ability.png')

    # 选择与讨论（实验操纵，阶段 1~3）
    # exp.page_pic(filename='1a.1_choice_trait.png')
    # exp.page_pic(filename='1a.2_choice_operation.png')
    # exp.page_pic(filename='1a.3_choice_ready.png')
    # exp.STAGE_choice(stage=1, mode='opinion')
    # exp.page_pic(filename='1a.4_discussion_same.png' if exp.Condition_similarity == '1' else '1a.4_discussion_diff.png')
    # exp.STAGE_discussion(stage=1, duration=120)

    # exp.page_pic(filename='1a.3_choice_ready.png')
    # exp.STAGE_choice(stage=2, mode='opinion')
    # exp.page_pic(filename='1a.4_discussion_same.png' if exp.Condition_similarity == '1' else '1a.4_discussion_diff.png')
    # exp.STAGE_discussion(stage=2, duration=120)

    # exp.page_pic(filename='1a.3_choice_ready.png')
    # exp.STAGE_choice(stage=3, mode='opinion')
    # exp.page_pic(filename='1a.4_discussion_same.png' if exp.Condition_similarity == '1' else '1a.4_discussion_diff.png')
    # exp.STAGE_discussion(stage=3, duration=120)

    # # 能力测试
    # exp.page_pic(filename='1b.1_choice_ability.png')
    # exp.page_pic(filename='1b.2_choice_operation.png')
    # exp.page_pic(filename='1b.3_choice_ready.png')
    # exp.STAGE_choice(stage=1, mode='thinking')

    # 练习阶段
    exp.page_pic(filename='2.1_grid.png')
    exp.page_pic(filename='2.2_grid.png')
    exp.page_pic(filename='2.3_grid.png')
    exp.page_pic(filename='2.4_grid.png')
    exp.page_pic(filename='2.5_grid_exercise.png')
    exp.STAGE_grid(grid_series=config.grid_series_exercise, process='exercise', stage=0)
    exp.clear_info()

    # 正式任务
    exp.page_pic(filename='2.6_grid_tips.png')
    exp.page_pic(filename='2.7_grid_ready.png')
    exp.STAGE_grid(grid_series=config.grid_series_formal, process='formal', stage=2)

    # 结束阶段
    exp.finale()

if __name__ == '__main__':

    launch()
