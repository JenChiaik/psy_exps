'''
解析 json 文件。
'''

import os, json


def keys_to_int(d: dict) -> dict:
    
    return {int(k): v for k, v in d.items()}


def match_dict(
    json_path: str,
    task_mode: str, report_mode: str,
    Perf_0: float = None, Perf_1: float = None
    ) -> dict:
    """
    根据参数匹配对应的字典组（四个子字典）。
    - json_path: JSON 文件路径。
    - task_mode: 'exercise', 'solo', 'dual'。
    - report_mode: 'confidence', 'ratio'。
    - Perf_0, Perf_1: 双方的能力（d'）。仅在 dual 模式下有效，solo / exercise 为 None。
    """

    with open(file=json_path, mode='r', encoding='utf-8') as file:
        array_dict = json.load(file)

    for key in array_dict:
        array_dict[key] = keys_to_int(array_dict[key])

    if task_mode == 'exercise' and report_mode == 'confidence':
        return {
            'sub0_w': array_dict['block_soloCF_exercise_w'],
            'sub0_b': array_dict['block_soloCF_exercise_b'],
            'sub1_w': array_dict['block_soloCF_exercise_w'],
            'sub1_b': array_dict['block_soloCF_exercise_b'],
        }

    elif task_mode == 'exercise' and report_mode == 'ratio':
        return {
            'sub0_w': array_dict['block_soloRT_exercise_w'],
            'sub0_b': array_dict['block_soloRT_exercise_b'],
            'sub1_w': array_dict['block_soloRT_exercise_w'],
            'sub1_b': array_dict['block_soloRT_exercise_b'],
        }

    elif task_mode == 'solo' and report_mode == 'confidence':
        return {
            'sub0_w': array_dict['block_soloCF_normal_w'],
            'sub0_b': array_dict['block_soloCF_normal_b'],
            'sub1_w': array_dict['block_soloCF_normal_w'],
            'sub1_b': array_dict['block_soloCF_normal_b'],
        }

    elif task_mode == 'solo' and report_mode == 'ratio':
        return {
            'sub0_w': array_dict['block_soloRT_normal_w'],
            'sub0_b': array_dict['block_soloRT_normal_b'],
            'sub1_w': array_dict['block_soloRT_normal_w'],
            'sub1_b': array_dict['block_soloRT_normal_b'],
        }

    elif task_mode == 'dual' and report_mode == 'confidence':
        if Perf_0 >= Perf_1:
            return {
                'sub0_w': array_dict['block_dualCF_normal_w'],
                'sub0_b': array_dict['block_dualCF_normal_b'],
                'sub1_w': array_dict['block_dualCF_hard_w'],
                'sub1_b': array_dict['block_dualCF_hard_b'],
            }
        else:
            return {
                'sub0_w': array_dict['block_dualCF_hard_w'],
                'sub0_b': array_dict['block_dualCF_hard_b'],
                'sub1_w': array_dict['block_dualCF_normal_w'],
                'sub1_b': array_dict['block_dualCF_normal_b'],
            }

    elif task_mode == 'dual' and report_mode == 'ratio':
        if Perf_0 >= Perf_1:
            return {
                'sub0_w': array_dict['block_dualRT_normal_w'],
                'sub0_b': array_dict['block_dualRT_normal_b'],
                'sub1_w': array_dict['block_dualRT_hard_w'],
                'sub1_b': array_dict['block_dualRT_hard_b'],
            }
        else:
            return {
                'sub0_w': array_dict['block_dualRT_hard_w'],
                'sub0_b': array_dict['block_dualRT_hard_b'],
                'sub1_w': array_dict['block_dualRT_normal_w'],
                'sub1_b': array_dict['block_dualRT_normal_b'],
            }

    else:
        raise ValueError(f'未知组合: task_mode={task_mode}, report_mode={report_mode}')



if __name__ == '__main__':

    import numpy as np
    import random as rd

    json_path = os.path.join(os.path.dirname(__file__), 'stim_array.json')

    stim_dicts = match_dict(
        json_path=json_path,
        task_mode='dual', report_mode='ratio',
        Perf_0=0.75, Perf_1=0.85
        )

    p = rd.randint(0,99)

    print(f"sub0_w[{p}] =", stim_dicts['sub0_w'][p],'\n',np.mean(stim_dicts['sub0_w'][p]), np.var(stim_dicts['sub0_w'][p]), '\n\n')
    print(f"sub0_b[{p}] =", stim_dicts['sub0_b'][p],'\n',np.mean(stim_dicts['sub0_b'][p]), np.var(stim_dicts['sub0_b'][p]), '\n\n')
    print(f"sub1_w[{p}] =", stim_dicts['sub1_w'][p],'\n',np.mean(stim_dicts['sub1_w'][p]), np.var(stim_dicts['sub1_w'][p]), '\n\n')
    print(f"sub1_b[{p}] =", stim_dicts['sub1_b'][p],'\n',np.mean(stim_dicts['sub1_b'][p]), np.var(stim_dicts['sub1_b'][p]), '\n\n')
