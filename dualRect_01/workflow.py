
from kernel import Event
from config import config

class Experiment:

    def __init__(self):

        self.event = Event()
        self.event.overture()
        self.event.prelude()
        self.event.tempVars()

        if self.event.exp_num % 2 == 1:
            self.order = 0
            self.map_mode = {0:'confidence', 1:'ratio'}
        elif self.event.exp_num % 2 == 0:
            self.order = 1
            self.map_mode = {0:'ratio', 1:'confidence'}
        else:
            raise ValueError('invalid exp_num, must be an integer')

        self.map_assets = {  # (block_order, sub): {index: asset}
            (0, 0): {1:'1_intro.jpg', 2:'2_intro_sub0.jpg', 
                     3:'3_soloCF_sub0.jpg', 4:'4_dualCF_sub0.jpg', 5:'5_dual.jpg', 
                     6:'3_soloRT_sub0.jpg', 7:'4_dualRT_sub1.jpg', 8:'5_dual.jpg'},

            (0, 1): {1:'1_intro.jpg', 2:'2_intro_sub1.jpg', 
                     3:'3_soloCF_sub1.jpg', 4:'4_dualCF_sub1.jpg', 5:'5_dual.jpg', 
                     6:'3_soloRT_sub1.jpg', 7:'4_dualRT_sub1.jpg', 8:'5_dual.jpg'},

            (1, 0): {1:'1_intro.jpg', 2:'2_intro_sub0.jpg', 
                     3:'3_soloRT_sub0.jpg', 4:'4_dualRT_sub0.jpg', 5:'5_dual.jpg', 
                     6:'3_soloCF_sub0.jpg', 7:'4_dualCF_sub1.jpg', 8:'5_dual.jpg'},

            (1, 1): {1:'1_intro.jpg', 2:'2_intro_sub1.jpg', 
                     3:'3_soloRT_sub1.jpg', 4:'4_dualRT_sub1.jpg', 5:'5_dual.jpg', 
                     6:'3_soloCF_sub1.jpg', 7:'4_dualCF_sub1.jpg', 8:'5_dual.jpg'},
                     }



    def launch(self):

        if self.event._debug:
            self.event.page_Ready_text(
                text_0='警告：实验正以调试模式运行。\n\n如果您是被试，请勿继续，并呼唤主试！', 
                text_1='警告：实验正以调试模式运行。\n\n如果您是被试，请勿继续，并呼唤主试！',
                allowed_bt=config.allowed_bt['next']
            )

        # pic1 欢迎页面（空格翻页）
        self.event.page_pic(
            auto=False, timeout=config.time['intro_timeout'],
            pic_0=self.map_assets[(self.order, 0)][1],
            pic_1=self.map_assets[(self.order, 1)][1],
            )
        # pic2 注意事项（被试Y_A翻页）
        self.event.page_Ready_pic(
            pic_0=self.map_assets[(self.order, 0)][2],
            pic_1=self.map_assets[(self.order, 1)][2],
            allowed_bt=config.allowed_bt['next'],
            timeout=config.time['intro_timeout'],
            )
        # pic3 单人阶段（被试Y_A翻页）
        self.event.page_Ready_pic(
            pic_0=self.map_assets[(self.order, 0)][3],
            pic_1=self.map_assets[(self.order, 1)][3],
            allowed_bt=config.allowed_bt['next'],
            timeout=config.time['intro_timeout'],
            )
        self.event.block(
            task_mode='exercise', report_mode=self.map_mode[0], block_index=0, 
            trial_num_b=config.trail_num['exercise'][0],
            trial_num_w=config.trail_num['exercise'][1],
            )
        self.event.page_text(
            auto=False, timeout=config.time['intro_timeout'],
            text_0=config.text['call_me'],
            text_1=config.text['call_me'],
            )
        self.event.block(
            task_mode='solo', report_mode=self.map_mode[0], block_index=1, 
            trial_num_b=config.trail_num['solo'][0],
            trial_num_w=config.trail_num['solo'][1],
            )
        # pic4 双人阶段（介绍，被试Y_A翻页）
        self.event.page_Ready_text(
            text_0=config.text['call_me_if_need'],
            text_1=config.text['call_me_if_need'],
            allowed_bt=config.allowed_bt['next'],
            timeout=config.time['intro_timeout'],
            )
        self.event.page_Ready_pic(
            pic_0=self.map_assets[(self.order, 0)][4],
            pic_1=self.map_assets[(self.order, 1)][4],
            allowed_bt=config.allowed_bt['next'],
            timeout=config.time['intro_timeout'],
            )
        # pic5 双人阶段（反馈，被试Y_A翻页）
        self.event.page_Ready_pic(
            pic_0=self.map_assets[(self.order, 0)][5],
            pic_1=self.map_assets[(self.order, 1)][5],
            allowed_bt=config.allowed_bt['next'],
            timeout=config.time['intro_timeout'],
            )
        self.event.block(
            task_mode='dual', report_mode=self.map_mode[0], block_index=2, 
            trial_num_b=config.trail_num['dual'][0],
            trial_num_w=config.trail_num['dual'][1],
            )
        

        ######### 中途休息 #########
        self.event.intermezzo()
        ######### 中途休息 #########


        self.event.page_text(
            auto=False, timeout=config.time['intro_timeout'],
            text_0=config.text['switch_rule'],
            text_1=config.text['switch_rule'],
            )
        # pic6 单人阶段（被试Y_A翻页，没有练习阶段）
        self.event.page_Ready_pic(
            pic_0=self.map_assets[(self.order, 0)][6],
            pic_1=self.map_assets[(self.order, 1)][6],
            allowed_bt=config.allowed_bt['next'],
            timeout=config.time['intro_timeout'],
            )
        self.event.page_text(
            auto=True, timeout=config.time['intro_timeout'],
            text_0=config.text['no_exercise'],
            text_1=config.text['no_exercise'],
            )
        self.event.block(
            task_mode='solo', report_mode=self.map_mode[1], block_index=4, 
            trial_num_b=config.trail_num['solo'][0],
            trial_num_w=config.trail_num['solo'][1],
            )
        # pic7 双人阶段（介绍，被试Y_A翻页）
        self.event.page_Ready_pic(
            pic_0=self.map_assets[(self.order, 0)][7],
            pic_1=self.map_assets[(self.order, 1)][7],
            allowed_bt=config.allowed_bt['next'],
            timeout=config.time['intro_timeout'],
            )
        # pic8 双人阶段（反馈，被试Y_A翻页）
        self.event.page_Ready_pic(
            pic_0=self.map_assets[(self.order, 0)][8],
            pic_1=self.map_assets[(self.order, 1)][8],
            allowed_bt=config.allowed_bt['next'],
            timeout=config.time['intro_timeout'],
            )
        self.event.block(
            task_mode='dual', report_mode=self.map_mode[1], block_index=5, 
            trial_num_b=config.trail_num['dual'][0],
            trial_num_w=config.trail_num['dual'][1],
            )
        
        self.event.finale()



if __name__ == '__main__':

    exp = Experiment()
    exp.launch()
