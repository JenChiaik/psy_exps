import json
import random
import statistics
from typing import Dict, List

def generate_array(
    mean: float,
    var: float,
    bound_lower: float,
    bound_upper: float,
    length: int = 9, 
    tolerance_mean: float = 0.0005,
    tolerance_var: float = 0.0005,
    max_iterations: int = 100000
) -> List[float]:
    """
    生成一个符合指定均值和方差且在给定边界内的浮点数数组。
    """
    iteration_count = 0

    while iteration_count < max_iterations:
        iteration_count += 1

        array = []

        while len(array) < length:
            val = random.gauss(mean, var ** 0.5)
            if bound_lower <= val <= bound_upper:
                array.append(val)

        current_mean = statistics.mean(array)
        current_var = statistics.pvariance(array)

        if (abs(current_mean - mean) <= tolerance_mean) and (abs(current_var - var) <= tolerance_var):
            return array

    raise ValueError("在指定的容差和迭代次数内未能生成符合要求的数组。")

def adjust_array(
    easy_array: List[float],
    multi_var: float,
    mean: float
) -> List[float]:
    """
    根据 easy_array 调整生成 hard_array，方法是将每个元素与均值的离均差乘以 multi_var。
    """
    adjusted_array = []
    for val in easy_array:
        deviation = val - mean
        new_val = mean + multi_var * deviation
        adjusted_array.append(new_val)
    return adjusted_array

if __name__ == "__main__":

    def write_json(array_num: int = 200, multi_var: float = 2.0, length: int =5):
        """
        生成 easy_S, easy_N, hard_S, hard_N 数组并写入 JSON 文件。
        hard_S 和 hard_N 是基于 easy_S 和 easy_N 通过缩放离均差生成的。
        """
        easy_S: Dict[str, List[float]] = {}
        easy_N: Dict[str, List[float]] = {}

        hard_S: Dict[str, List[float]] = {}
        hard_N: Dict[str, List[float]] = {}

        for i in range(array_num):
            key = str(i)

            easy_S_array = generate_array(
                mean=0.52,
                var=0.020,
                bound_lower=0.1,
                bound_upper=0.9,
                length=length,
                tolerance_mean=0.0005,
                tolerance_var=0.00025
            )
            easy_N_array = generate_array(
                mean=0.48,
                var=0.020,
                bound_lower=0.1,
                bound_upper=0.9,
                length=length,
                tolerance_mean=0.0005,
                tolerance_var=0.00025
            )

            easy_S[key] = easy_S_array
            easy_N[key] = easy_N_array

            hard_S_array = adjust_array(
                easy_array=easy_S_array,
                multi_var=multi_var,
                mean=0.52
            )
            hard_N_array = adjust_array(
                easy_array=easy_N_array,
                multi_var=multi_var,
                mean=0.48
            )

            hard_S_array = [max(0.1, min(val, 0.9)) for val in hard_S_array]
            hard_N_array = [max(0.1, min(val, 0.9)) for val in hard_N_array]

            hard_S[key] = hard_S_array
            hard_N[key] = hard_N_array

            if (i + 1) % 10 == 0 or (i + 1) == array_num:
                print(f'已完成 {i + 1}/{array_num} 个数组 ({(i + 1)/array_num*100:.1f}%).')

        array_dict = {
            'easy_S': easy_S,
            'easy_N': easy_N,
            'hard_S': hard_S,
            'hard_N': hard_N,
        }

        with open(file='random_array.json', mode='w', encoding='utf-8') as fin:
            json.dump(array_dict, fin, ensure_ascii=False, indent=4)

    write_json(array_num=200, multi_var=2.0, length=9)
