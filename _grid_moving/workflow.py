
'''
实验流程控制模块。
'''

import kernel, trigger
from config import config

def launch():
    
    exp = kernel.Experiment()
    EventMarker = trigger.Trigger(mode='LSL')

    # 信息录入
    exp.overture()
    EventMarker.send(value=1)

    # 指导语与练习
    exp.page_pic(filename='0_welcome.png')
    exp.page_pic(filename='1.1_grid.png')
    exp.page_pic(filename='1.2_grid.png')
    exp.page_pic(filename='1.3_grid.png')
    exp.page_pic(filename='1.4_grid.png')
    ## 练习 1
    exp.page_pic(filename='1.5_grid_ex1.png')
    exp.STAGE_grid(grid_series=config.grid_series_exercise_1, stage=0, shuffle=False, process_name='grid_exercise_1')
    exp.page_pic(filename='1.6_grid.png')
    ## 练习 2
    exp.page_pic(filename='1.7_grid_ex2.png')
    exp.STAGE_grid(grid_series=config.grid_series_exercise_2, stage=0, shuffle=False, process_name='grid_exercise_2')
    ## 练习 3
    exp.page_pic(filename='1.8_grid_ex3.png')
    exp.STAGE_grid(grid_series=config.grid_series_exercise_3, stage=0, shuffle=False, process_name='grid_exercise_3')

    # 前测
    exp.page_pic(filename='1.9_grid_ready.png')
    EventMarker.send(value=2)
    exp.STAGE_grid(grid_series=config.grid_series_formal, stage=1, shuffle=True, process_name='grid_1')
    EventMarker.send(value=3)

    # 选择与讨论（实验操纵，阶段 1~3）
    ## stage 1 / behaviour
    exp.page_pic(filename='2.1_choice.png')
    exp.page_pic(filename='2.2_choice.png')
    exp.page_pic(filename='2.3_choice_ready.png')
    exp.STAGE_choice(stage=1, mode='opinion')

    exp.page_pic(filename='2.4_discussion_same.png' if exp.Condition_similarity == '1' else '2.4_discussion_diff.png')
    EventMarker.send(value=111)
    exp.STAGE_discussion(stage=1, duration=5)
    EventMarker.send(value=112)

    ## stage 2 / value
    exp.page_pic(filename='2.3_choice_ready.png')
    exp.STAGE_choice(stage=2, mode='opinion')

    exp.page_pic(filename='2.4_discussion_same.png' if exp.Condition_similarity == '1' else '2.4_discussion_diff.png')
    EventMarker.send(value=121)
    exp.STAGE_discussion(stage=2, duration=5)
    EventMarker.send(value=122)

    ## stage 3 / social event
    exp.page_pic(filename='2.3_choice_ready.png')
    exp.STAGE_choice(stage=3, mode='opinion')

    exp.page_pic(filename='2.4_discussion_same.png' if exp.Condition_similarity == '1' else '2.4_discussion_diff.png')
    EventMarker.send(value=131)
    exp.STAGE_discussion(stage=3, duration=5)
    EventMarker.send(value=132)

    # 后测
    exp.page_pic(filename='3.1_grid.png')
    exp.page_pic(filename='3.2_grid.png')
    exp.page_pic(filename='3.3_grid_ready.png')

    EventMarker.send(value=4)
    exp.STAGE_grid(grid_series=config.grid_series_formal, stage=2, shuffle=True, process_name='grid_2')
    EventMarker.send(value=5)

    # 结束阶段
    EventMarker.send(value=255)
    exp.finale()

if __name__ == '__main__':

    launch()