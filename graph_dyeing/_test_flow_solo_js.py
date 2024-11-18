'''
实验主流程控制模块。
'''

import config
import _test_kernel_solo_js

import random as rd

from graph import GraphSeries

def launch():

    exp = _test_kernel_solo_js.Experiment()

    # 信息采集与创建 I/O
    exp.overture()
    exp.kb.clearEvents()

    # 静息扫描阶段（1）
    # exp.intermezzo('rest')
    # exp.record('rest_1')

    # 指导语阶段（1）
    exp.page_text(t_text=config.text_dict['intr_welcome'], stage_name='欢迎页面出现', min_time=0)
    exp.page_text(t_text=config.text_dict['intr_1_1'], min_time=0)
    exp.page_text(t_text=config.text_dict['intr_1_2'], min_time=0)
    exp.page_text(t_text=config.text_dict['intr_1_3'], min_time=0)
    exp.record('intr_1') #需要读取 exp_param 的 exp_config，展现不同的指导语。

    # 填色练习阶段
    order_exercise = [i for i in config.graph_dict_exercise.keys()]
    rd.shuffle(order_exercise)
    for i in order_exercise:
        exp.page_operation(GraphSeries(*config.graph_dict_exercise[i]['uncolored'], 
                                       **config.graph_dict_exercise[i]['colored']),
                                       stage=0)
    exp.write_data(f'练习阶段完成时间,{exp.clock.getTime()}')
    exp.record('try')

    # 独立学习阶段（1）
    # exp.intermezzo('indv')
    # exp.record('indv_1')

    # 合作交流阶段（1）
    # exp.intermezzo('coop')
    # exp.record('coop_1')

    # 穿插测验阶段
    # order_test1 = [i for i in config.graph_dict_test1.keys()]
    # rd.shuffle(order_test1)
    # for i in order_test1:
    #     exp.wait_operation(GraphSeries(*config.graph_dict_test1[i]['uncolored'], 
    #                                    **config.graph_dict_test1[i]['colored']),
    #                                    stage=1)
    # exp.write_data(f'穿插测验完成时间,{exp.clock.getTime()}')
    # exp.record('test1')

    # 静息扫描阶段（2）
    # exp.intermezzo('rest')
    # exp.record('rest_2')

    # 指导语阶段（2）
    # exp.render_text(t_text=config.text_dict['intr_welcome'], stage_name='欢迎页面出现')
    # exp.wait_nextpage(allowed_keys=config.keys_nextpage, min_time=1, stage_name='欢迎页面结束')
    # exp.render_text(t_text=config.text_dict['intr_2_1'])
    # exp.wait_nextpage(allowed_keys=config.keys_nextpage, min_time=1, stage_name='指导语1结束')
    # exp.render_text(t_text=config.text_dict['intr_2_2'])
    # exp.wait_nextpage(allowed_keys=config.keys_nextpage, min_time=1, stage_name='指导语2结束')
    # exp.render_text(t_text=config.text_dict['intr_2_3'])
    # exp.wait_nextpage(allowed_keys=config.keys_nextpage, min_time=1, stage_name='指导语3结束')
    # exp.record('intr_2')

    # 独立学习阶段（2）
    # exp.intermezzo('indv')
    # exp.record('indv_2')

    # 合作交流阶段（2）
    # exp.intermezzo('coop')
    # exp.record('coop_2')

    # 最终测验阶段
    # order_test2 = [i for i in config.graph_dict_test2.keys()]
    # rd.shuffle(order_test2)
    # for i in order_test2:
    #     exp.wait_operation(GraphSeries(*config.graph_dict_test2[i]['uncolored'], 
    #                                    **config.graph_dict_test2[i]['colored']),
    #                                    stage=2)
    # exp.write_data(f'最终测验完成时间,{exp.clock.getTime()}')
    # exp.record('test2')

    # 结束阶段
    exp.finale()

if __name__ == '__main__':

    launch()