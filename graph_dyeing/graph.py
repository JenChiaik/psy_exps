'''
图形序列生成、染色模块。
包含形状、颜色的图形序列，及其染色方法。
'''

class GraphSeries:
    '''
    图形序列对象。
    核心属性：self.graph_series，列表。
        列表元素格式：[形状'shape', 颜色'color', 可否染色True/False]
    '''

    shape_order = ['cl','tg','sq','dm','pt'] #任何情况都按照此列表顺序对形状进行排序：圆形-三角-方形-菱形-五边形。
    shape_param = {'cl':None,'tg':(3,0),'sq':(4,45),'dm':(4,90),'pt':(5,0)} #除圆形外，其它图形的元组表示边数与旋角。
    color_param = {'r':'#d83737','g':'#65c386','b':'#275fe0','y':'#f2b21b','p':'#b28fe0',None:'#ffffff'}

    def __init__(self, *uncolored, **colored):
        '''
        所有图形按照self.allowed_shape中的顺序排序。
            *uncorlored: 须填色的图形，`shape`。
            **colored: 固定颜色的图形，shape=[`color`]。
        '''
        self.graph_series = []
        
        for i in uncolored:
            if i in self.shape_param:
                self.graph_series.append([i, None, True])
            else:
                raise ValueError('\n不存在的形状！\n')
            
        for i,j in colored.items():
            if i in self.shape_param:
                for k in j:
                    if k in self.color_param:
                            self.graph_series.append([i, k, False])
            else:
                raise ValueError('\n不存在的形状或颜色！\n')

        self.graph_series.sort(key=lambda i:self.shape_order.index(i[0]))

    def __str__(self):
        '''
        返回当前 graph_series 列表的格式化字符串：
        “形状  当前颜色  是否可染色”
        '''
        print_str = ''
        for i in self.graph_series:
            print_str += f'{i[0]}{" "*(10-len(i))}{i[1]}{" "*(10-len(str(i[1])))}{i[2]}\n'
        return '\n'+print_str
    
    def coloring(self, shape_id, color):
        '''
        为某个图形重新染色。
        shape_id: int，表示**排序后**graph_series的图形序数（从0开始）。
        color: str，需要染成的颜色。
        '''
        if self.graph_series[shape_id][2] == True:
            if 0 <= shape_id and shape_id <= len(self.graph_series)-1:
                if isinstance(shape_id,int) and color in self.color_param:
                    self.graph_series[shape_id][1] = color
        else: 
            pass

if __name__ == '__main__':

    gs = GraphSeries('cl','dm','pt',tg='b',cl=['y','g'],dm='p')
    print(gs)

    gs.coloring(0,'r')
    gs.coloring(4,'g')
    gs.coloring(6,'y')
    print(gs) #处理可染色图形

    gs.coloring(1,None)
    gs.coloring(2,'p')
    print(gs) #处理不可染色图形

