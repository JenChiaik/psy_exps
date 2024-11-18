
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
    exp.page_pic(filename='1_grid.png')
    exp.page_pic(filename='2_grid.png')
    exp.page_pic(filename='3_grid.png')
    exp.page_pic(filename='4_grid.png')
    ## 练习 1
    exp.page_pic(filename='5_grid_ex1.png')
    exp.STAGE_grid(grid_series=config.grid_series_exercise_1, stage=0, shuffle=False, process_name='grid_exercise_1')
    exp.page_pic(filename='6_grid.png')
    ## 练习 2
    exp.page_pic(filename='7_grid_ex2.png')
    exp.STAGE_grid(grid_series=config.grid_series_exercise_2, stage=0, shuffle=False, process_name='grid_exercise_2')
    ## 练习 3
    exp.page_pic(filename='8_grid_ex3.png')
    exp.STAGE_grid(grid_series=config.grid_series_exercise_3, stage=0, shuffle=False, process_name='grid_exercise_3')

    #正式实验
    ## 个人分数说明
    exp.page_pic(filename='9_grid.png')
    exp.page_pic(filename='10_grid.png')

    ## 阶段 1
    exp.page_pic(filename='11a_grid_hide.png' if exp.Condition_order == '1' else '11b_grid_show.png')
    EventMarker.send(value=2)
    exp.STAGE_grid(grid_series=config.grid_series_formal, 
                   stage=1, 
                   shuffle=True, 
                   process_name='grid_hide' if exp.Condition_order == '1' else 'grid_show')
    EventMarker.send(value=3)

    ## 阶段 2
    exp.page_pic(filename='11b_grid_show.png' if exp.Condition_order == '1' else '11a_grid_hide.png')
    EventMarker.send(value=4)
    exp.STAGE_grid(grid_series=config.grid_series_formal, 
                   stage=2, 
                   shuffle=True, 
                   process_name='grid_show' if exp.Condition_order == '1' else 'grid_hide')
    EventMarker.send(value=5)

    # 结束阶段
    EventMarker.send(value=255)
    exp.finale()

if __name__ == '__main__':

    launch()