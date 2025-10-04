import json
import random
import statistics

def generate_array(
    mean: float, 
    var: float, 
    bound_lower: float, 
    bound_uper: float, 
    length=9, 
    tolerance_mean=0.0005,
    tolerance_var=0.0005,
    max_iterations=100000
):
    """
    生成一个符合指定均值和方差的数组，元素在指定范围内。
    """
    iteration_count = 0
    
    while iteration_count < max_iterations:
        iteration_count += 1
        
        array = []
        
        while len(array) < length:
            val = random.gauss(mean, var**0.5)
            if bound_lower <= val <= bound_uper:
                array.append(val)
        
        current_mean = statistics.mean(array)
        current_var = statistics.pvariance(array)
        
        if (abs(current_mean - mean) <= tolerance_mean) and (abs(current_var - var) <= tolerance_var):
            return array
    
    raise ValueError("生成数组失败，达到最大迭代次数。")

def reorder_hard(array_easy, array_hard):
    """
    根据 array_easy 的元素大小排序顺序，重新排列 array_hard 的元素。
    """
    sorted_indices_easy = sorted(range(len(array_easy)), key=lambda x: array_easy[x])
    
    sorted_hard = sorted(array_hard)
    
    array_hard_reordered = [0] * len(array_hard)
    
    for rank, idx in enumerate(sorted_indices_easy):
        array_hard_reordered[idx] = sorted_hard[rank]
    
    return array_hard_reordered

if __name__ == "__main__":

    def write_json(array_num=100, 
                   mean_S=0.525, mean_N=0.475, 
                   var_easy=0.020, var_hard=0.080, 
                   bound_lower=0.05, bound_uper=0.95, 
                   tolerance_mean=0.005, 
                   tolerance_var=0.00025):
        """
        生成多个数组并保存到 JSON 文件中，确保 hard_S 和 hard_N 的排列顺序与 easy_S 和 easy_N 保持一致。
        """
        easy_S = {}
        easy_N = {}
        hard_S = {}
        hard_N = {}
        _finished = 0

        for i in range(array_num):
            array_easy_S = generate_array(
                mean=mean_S, 
                var=var_easy, 
                bound_lower=bound_lower, 
                bound_uper=bound_uper, 
                tolerance_mean=tolerance_mean, 
                tolerance_var=tolerance_var
            )
            
            array_easy_N = generate_array(
                mean=mean_N, 
                var=var_easy, 
                bound_lower=bound_lower, 
                bound_uper=bound_uper, 
                tolerance_mean=tolerance_mean, 
                tolerance_var=tolerance_var
            )
            
            array_hard_S = generate_array(
                mean=mean_S, 
                var=var_hard, 
                bound_lower=bound_lower, 
                bound_uper=bound_uper, 
                tolerance_mean=tolerance_mean, 
                tolerance_var=tolerance_var
            )
            
            array_hard_N = generate_array(
                mean=mean_N, 
                var=var_hard, 
                bound_lower=bound_lower, 
                bound_uper=bound_uper, 
                tolerance_mean=tolerance_mean, 
                tolerance_var=tolerance_var
            )
            
            array_hard_S_re = reorder_hard(array_easy_S, array_hard_S)
            array_hard_N_re = reorder_hard(array_easy_N, array_hard_N)
            
            easy_S[i] = array_easy_S
            hard_S[i] = array_hard_S_re
            easy_N[i] = array_easy_N
            hard_N[i] = array_hard_N_re

            _finished += 1
            print(f'完成进度: {_finished/array_num*100:.1f}%。')
        
        with open(file='random_array.json', mode='w', encoding='utf-8') as fin:
            array_dict = {
                'easy_S': easy_S, 
                'easy_N': easy_N,
                'hard_S': hard_S,
                'hard_N': hard_N,
            }
            json.dump(array_dict, fin, ensure_ascii=False, indent=4)
            print("done.")

    write_json()
