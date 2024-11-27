'''
实验主流程控制模块。
'''

import config
import kernel_dual

from psychopy import parallel

def launch():

    exp = kernel_dual.Experiment()
    # port = parallel.ParallelPort(address=...)

    # 信息采集与创建 I/O
    exp.overture()
    exp.kb.clearEvents()

    # 中断提示
    exp.page_text(text=config.text_dict['prelude_scan'], wait=config.wait_break)

    # 静息扫描阶段（1）
    exp.record(lable='rest_scan_stage1', notes='stage start')
    exp.intermezzo('rest')
    # exp.record('rest_1')

    # 指导语阶段（1）
    exp.record(lable='intro_stage1', notes='stage start')
    exp.page_text(text=config.text_dict['intr_welcome'], wait=config.wait_text)
    exp.page_text(text=config.text_dict['intr_1_1'], wait=config.wait_text)
    if exp.exp_cfg == '1':
        exp.page_text(text=config.text_dict['intr_1_2_1'], wait=config.wait_text)
    else:
        exp.page_text(text=config.text_dict['intr_1_2_2'], wait=config.wait_text)
    exp.page_text(text=config.text_dict['intr_1_3'], wait=config.wait_text)
    # exp.record('intr_1')

    # 填色练习阶段
    exp.record(lable='exersice', notes='stage start')
    exp.page_coloring(stage=0)
    # exp.record('try')

    # 中断提示
    exp.page_text(text=config.text_dict['prelude_indiv'], wait=config.wait_break)

    # 独立学习阶段（1）
    exp.record(lable='individual_learning_stage1', notes='stage start')
    exp.intermezzo('indv')
    # exp.record('indv_1')

    # 中断提示
    exp.page_text(text=config.text_dict['prelude_coop'], wait=config.wait_break)

    # 合作交流阶段（1）
    exp.record(lable='cooperative_learning_stage1', notes='stage start')
    exp.intermezzo('coop')
    # exp.record('coop_1')

    # 中断提示
    exp.page_text(text=config.text_dict['prelude_test'], wait=config.wait_break)

    # 测验（1）
    exp.record(lable='test_stage1', notes='stage start')
    exp.page_coloring(stage=1)
    # exp.record('test1')

    # 中断提示
    exp.page_text(text=config.text_dict['prelude_scan'], wait=config.wait_break)

    # 静息扫描阶段（2）
    exp.record(lable='rest_scan_stage2', notes='stage start')
    exp.intermezzo('rest')
    # exp.record('rest_2')

    # 分数展示
    exp.page_score()

    # 指导语阶段（2）
    exp.record(lable='intro_stage2', notes='stage start')
    exp.page_text(text=config.text_dict['intr_2_1'], wait=config.wait_text)
    if exp.exp_param['exp_config'] == '1':
        exp.page_text(text=config.text_dict['intr_2_2_1'], wait=config.wait_text)
    else:
        exp.page_text(text=config.text_dict['intr_2_2_2'], wait=config.wait_text)
    exp.page_text(text=config.text_dict['intr_1_3'], wait=config.wait_text)
    # exp.record('intr_1')

    # 独立学习阶段（2）
    exp.record(lable='individual_learning_stage2', notes='stage start')
    exp.intermezzo('indv')
    # exp.record('indv_2')

    # 中断提示
    exp.page_text(text=config.text_dict['prelude_coop'], wait=config.wait_break)

    # 合作交流阶段（2）
    exp.record(lable='cooperative_learning_stage2', notes='stage start')
    exp.intermezzo('coop')
    # exp.record('coop_2')

    # 中断提示
    exp.page_text(text=config.text_dict['prelude_test'], wait=config.wait_break)

    # 测验（2）
    exp.record(lable='test_stage2', notes='stage start')
    exp.page_coloring(stage=2)
    # exp.record('test2')

    # 结束阶段
    exp.record(lable='end', notes='stage start')
    exp.finale()

if __name__ == '__main__':

    launch()