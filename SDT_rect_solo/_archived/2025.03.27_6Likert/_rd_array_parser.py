import os, json
import numpy as np

def json_loader(file_name='random_array.json'):

    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, file_name)
    with open(file=file_path, mode='r', encoding='utf-8') as file:

        data = json.load(file)

    return data



def json_parser(data:dict):
    
    for key_out in data.keys():

        mean_list = []
        var_list = []

        for key_in in data[key_out].keys():

            mean_list.append(np.mean(data[key_out][key_in]))
            var_list.append(np.var(data[key_out][key_in]))

        print (
            f"\n{key_out}\n"
            f"\tlength:{len(data[key_out])}\n"
            f"\tmeans' mean:{format(np.mean(mean_list), '.4f')}"
            f"\tvars' mean:{format(np.mean(var_list), '.4f')}"
            )




if __name__ == '__main__':

    data = json_loader()
    json_parser(data=data)