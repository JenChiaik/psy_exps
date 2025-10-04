
import os, json
import numpy as np



def generate_array(
    array_length:int,
    array_mean:float, array_var:float,
    tolerance_mean:float, tolerance_var:float,
    bound_lower:float, bound_upper:float,
    max_iterations:int = 10000
    ) -> list[float]:
    """
    使用方差分配法 + Dirichlet 分布生成满足均值/方差约束的数组。
    """
    SQ = array_var * array_length  # 数组的离均差平方和

    for _ in range(max_iterations):
        # 随机分配离均差平方和数组，并计算离均差（均为正值）
        deltas_squared = np.random.dirichlet(alpha = [1]*array_length) * SQ
        deltas = np.sqrt(deltas_squared)

        # 给离均差随机添加正负号
        signs = np.random.choice([-1, 1], size=array_length)
        deltas *= signs

        # 在均值基础上增加带符号的离均差
        array = array_mean + deltas

        # 由于离均差的正负号是随机的，因此将其校正至目标均值
        offset = array_mean - np.mean(array)
        array += offset

        # 检查
        if np.all((array >= bound_lower) & (array <= bound_upper)):
            current_mean = np.mean(array)
            current_var = np.var(array, ddof=0)

            if (
                abs(current_mean - array_mean) <= tolerance_mean and
                abs(current_var - array_var) <= tolerance_var
            ):
                return array.tolist()

    raise ValueError("生成数组失败，达到最大迭代次数。")



def bash_generator(
        array_num:int, 
        array_length:int, array_mean:float, array_var:float, 
        tolerance_mean:float, tolerance_var:float, 
        bound_lower:float, bound_upper:float
        ) -> dict[int:list[float]]:
    '''
    批量生成指定参数的数组，以字典形式写入 .json 文件中。
    '''

    dict_arrays = {}

    for i in range(array_num):
        dict_arrays[i] = generate_array(
            array_length=array_length, array_mean=array_mean, array_var=array_var, 
            bound_lower=bound_lower, bound_upper=bound_upper, 
            tolerance_mean=tolerance_mean, tolerance_var=tolerance_var
        )

    return dict_arrays



def bash_write(filename:str, **dict_arrays:dict):
    '''
    将数个字典批量写入 .json 文件，嵌套在外层字典中。
    - **dict_arrays: 'dict_name':dict_arrays
    '''

    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, filename)

    json_dict = {}

    for i in dict_arrays:
        json_dict[i] = dict_arrays[i]

    with open(file=file_path, mode='w', encoding='utf-8') as file:
        json.dump(obj=json_dict, fp=file, ensure_ascii=False, indent=4)

    print('\n\ndone.')



if __name__ == "__main__":

    filename = input('\n\n————输出的 json 文件名：————\n\n')

    if filename == 'stim_array.json':
        array_length = 4
        mean_w = 0.475
        mean_b = 0.525
        var_normal = 0.01
        var_hard = 0.04
    elif filename == 'stim_debug.json':
        array_length = 4
        mean_w = 0.475
        mean_b = 0.525
        var_normal = 0.01
        var_hard = 0.04
    else:
        raise ValueError("invalid filename.")


    bash_write(filename=filename, 
        # 练习（normal）
        block_soloCF_exercise_w = bash_generator(
            array_num=15, array_length=array_length, 
            array_mean=mean_w, array_var=var_normal, 
            tolerance_mean=0.005, tolerance_var=0.00025, 
            bound_lower=0.1, bound_upper=0.9, 
        ), 
        block_soloCF_exercise_b = bash_generator(
            array_num=15, array_length=array_length, 
            array_mean=mean_b, array_var=var_normal, 
            tolerance_mean=0.005, tolerance_var=0.00025, 
            bound_lower=0.1, bound_upper=0.9, 
        ), 
        block_soloRT_exercise_w = bash_generator(
            array_num=15, array_length=array_length, 
            array_mean=mean_w, array_var=var_normal, 
            tolerance_mean=0.005, tolerance_var=0.00025, 
            bound_lower=0.1, bound_upper=0.9, 
        ), 
        block_soloRT_exercise_b = bash_generator(
            array_num=15, array_length=array_length, 
            array_mean=mean_b, array_var=var_normal, 
            tolerance_mean=0.005, tolerance_var=0.00025, 
            bound_lower=0.1, bound_upper=0.9, 
        ), 
        # 单人（normal）
        block_soloCF_normal_w = bash_generator(
            array_num=200, array_length=array_length, 
            array_mean=mean_w, array_var=var_normal, 
            tolerance_mean=0.005, tolerance_var=0.00025, 
            bound_lower=0.1, bound_upper=0.9, 
        ), 
        block_soloCF_normal_b = bash_generator(
            array_num=200, array_length=array_length, 
            array_mean=mean_b, array_var=var_normal, 
            tolerance_mean=0.005, tolerance_var=0.00025, 
            bound_lower=0.1, bound_upper=0.9, 
        ), 
        block_soloRT_normal_w = bash_generator(
            array_num=200, array_length=array_length, 
            array_mean=mean_w, array_var=var_normal, 
            tolerance_mean=0.005, tolerance_var=0.00025, 
            bound_lower=0.1, bound_upper=0.9, 
        ), 
        block_soloRT_normal_b = bash_generator(
            array_num=200, array_length=array_length, 
            array_mean=mean_b, array_var=var_normal, 
            tolerance_mean=0.005, tolerance_var=0.00025, 
            bound_lower=0.1, bound_upper=0.9, 
        ), 
        # 双人（normal / hard）
        ## 双人（CF）
        block_dualCF_normal_w = bash_generator(
            array_num=200, array_length=array_length, 
            array_mean=mean_w, array_var=var_normal, 
            tolerance_mean=0.005, tolerance_var=0.00025, 
            bound_lower=0.1, bound_upper=0.9, 
        ), 
        block_dualCF_normal_b = bash_generator(
            array_num=200, array_length=array_length, 
            array_mean=mean_b, array_var=var_normal, 
            tolerance_mean=0.005, tolerance_var=0.00025, 
            bound_lower=0.1, bound_upper=0.9, 
        ), 
        block_dualCF_hard_w = bash_generator(
            array_num=200, array_length=array_length, 
            array_mean=mean_w, array_var=var_hard, 
            tolerance_mean=0.005, tolerance_var=0.00025, 
            bound_lower=0.1, bound_upper=0.9, 
        ), 
        block_dualCF_hard_b = bash_generator(
            array_num=200, array_length=array_length, 
            array_mean=mean_b, array_var=var_hard, 
            tolerance_mean=0.005, tolerance_var=0.00025, 
            bound_lower=0.1, bound_upper=0.9, 
        ), 
        ## 双人（RT）
        block_dualRT_normal_w = bash_generator(
            array_num=200, array_length=array_length, 
            array_mean=mean_w, array_var=var_normal, 
            tolerance_mean=0.005, tolerance_var=0.00025, 
            bound_lower=0.1, bound_upper=0.9, 
        ), 
        block_dualRT_normal_b = bash_generator(
            array_num=200, array_length=array_length, 
            array_mean=mean_b, array_var=var_normal, 
            tolerance_mean=0.005, tolerance_var=0.00025, 
            bound_lower=0.1, bound_upper=0.9, 
        ), 
        block_dualRT_hard_w = bash_generator(
            array_num=200, array_length=array_length, 
            array_mean=mean_w, array_var=var_hard, 
            tolerance_mean=0.005, tolerance_var=0.00025, 
            bound_lower=0.1, bound_upper=0.9, 
        ), 
        block_dualRT_hard_b = bash_generator(
            array_num=200, array_length=array_length, 
            array_mean=mean_b, array_var=var_hard, 
            tolerance_mean=0.005, tolerance_var=0.00025, 
            bound_lower=0.1, bound_upper=0.9, 
        ), 
    )
        
