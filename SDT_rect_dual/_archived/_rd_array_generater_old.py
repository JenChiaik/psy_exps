import json
import random
import statistics

def generate_array(
    mean:float, 
    var:float, 
    bound_lower:float, 
    bound_uper:float, 
    length=9, 
    tolerance_mean=0.0005,
    tolerance_var=0.0005,
    max_iterations=100000
):
    
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
        
        if (abs(current_mean-mean) <= tolerance_mean) and (abs(current_var-var) <= tolerance_var):
            return array
    
    raise ValueError("fail.")

if __name__ == "__main__":

    def write_json(array_num=200):

        easy_S = {}
        easy_N = {}

        hard_S = {}
        hard_N = {}

        _finished = 0

        for i in range(array_num):

            easy_S[i] = generate_array(mean=0.52, var=0.020, 
                                       bound_lower=0.1, bound_uper=0.9, 
                                       tolerance_mean=0.005, tolerance_var=0.00025)
            easy_N[i] = generate_array(mean=0.48, var=0.020, 
                                       bound_lower=0.1, bound_uper=0.9, 
                                       tolerance_mean=0.005, tolerance_var=0.00025)
            hard_S[i] = generate_array(mean=0.52, var=0.040, 
                                       bound_lower=0.1, bound_uper=0.9, 
                                       tolerance_mean=0.005, tolerance_var=0.00025)
            hard_N[i] = generate_array(mean=0.48, var=0.040, 
                                       bound_lower=0.1, bound_uper=0.9, 
                                       tolerance_mean=0.005, tolerance_var=0.00025)
            
            _finished += 1
            print (f'finished {_finished/array_num*100:.1f}%.')

        with open(file='random_array.json', mode='w', encoding='utf-8') as fin:

            array_dict = {
                'easy_S':easy_S, 
                'easy_N':easy_N,
                'hard_S':hard_S,
                'hard_N':hard_N,
            }
            json.dump(array_dict, fin, ensure_ascii=False, indent=4)

    write_json()

