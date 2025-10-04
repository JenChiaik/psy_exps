import json
import numpy as np

def json_parser(file='random_array.json'):

    with open(file=file, mode='r', encoding='utf-8') as fin:

        data = json.load(fin)

        easy_S = data['easy_S']
        easy_N = data['easy_N']
        hard_S = data['hard_S']
        hard_N = data['hard_N']

    return easy_S, easy_N, hard_S, hard_N

if __name__ == '__main__':

    easy_S, easy_N, hard_S, hard_N = json_parser('random_array.json')

    array_ES = easy_S.values()
    array_EN = easy_N.values()
    array_HS = hard_S.values()
    array_HN = hard_N.values()

    print(easy_S['14'])
    print(easy_N['91'])
    print(hard_S['14'])
    print(hard_N['91'])

    mean_ES, var_ES = [], []
    mean_EN, var_EN = [], []
    mean_HS, var_HS = [], []
    mean_HN, var_HN = [], []

    for _ in array_ES:
        mean_ES.append(np.mean(_))
        var_ES.append(np.var(_))

    for _ in array_EN:
        mean_EN.append(np.mean(_))
        var_EN.append(np.var(_))

    for _ in array_HS:
        mean_HS.append(np.mean(_))
        var_HS.append(np.var(_))
    
    for _ in array_HN:
        mean_HN.append(np.mean(_))
        var_HN.append(np.var(_))

    print()
    print(f'数组均值均值 {np.mean(mean_ES):.6f}, 数组方差均值 {np.mean(var_ES):.6f}')
    print(f'数组最大方差 {max(var_ES):.6f}, 数组最小方差 {min(var_ES):.6f}')
    print()
    print(f'数组均值均值 {np.mean(mean_EN):.6f}, 数组方差均值 {np.mean(var_EN):.6f}')
    print(f'数组最大方差 {max(var_EN):.6f}, 数组最小方差 {min(var_EN):.6f}')
    print()
    print(f'数组均值均值 {np.mean(mean_HS):.6f}, 数组方差均值 {np.mean(var_HS):.6f}')
    print(f'数组最大方差 {max(var_HS):.6f}, 数组最小方差 {min(var_HS):.6f}')
    print()
    print(f'数组均值均值 {np.mean(mean_HN):.6f}, 数组方差均值 {np.mean(var_HN):.6f}')
    print(f'数组最大方差 {max(var_HN):.6f}, 数组最小方差 {min(var_HN):.6f}')

    # def dyrect(dict_obj:dict, trail_index:int, array_index:int):
    #     '''
    #     返回每个动态矩形的高度和位置信息。
    #     - dict_obj: 指定解包后的 json_dict, self.easy_S / self.easy_N / self.hard_S / self.hard_N。
    #     - trail_index: 0 ~ 199，每个 block 至多包含 400 个 trail（200 signal + 200 noise）。
    #     - array_index: 0 ~ 8，每个 trail 至多包含 9 个图形。
    #     '''

    #     width = 0.1
    #     height = round(dict_obj[str(trail_index)][array_index], 3)

    #     location_x = np.linspace(start=-0.6, stop=0.6, num=9)[array_index]
    #     location_y = (-1/2 + height)/2

    #     return {'size':[width, height], 'loca':[location_x, location_y]}

    # _dict = json_parser()[0] #easy_S

    # for i in range(9):
    #     print(dyrect(dict_obj=_dict, trail_index=0, array_index=i))