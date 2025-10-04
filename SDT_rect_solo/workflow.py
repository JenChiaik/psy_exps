
from kernel import Event
from config import config

def launch():

    exp = Event()

    # 开始
    exp.overture(log_file_name='log.txt', data_file_dir='data')
    exp.prelude()

    exp.disp_pic(wait=1, auto=False, pic_0='intro_1.png')
    exp.disp_pic(wait=1, auto=False, pic_0='intro_2.png')
    exp.disp_pic(wait=1, auto=False, pic_0='intro_3.png')
    exp.disp_pic(wait=1, auto=False, pic_0='intro_4.png')

    # 练习
    exp.disp_text(wait=1, auto=False, text_0=config.text['start_exercise'])
    exp.block_SD(process_name='exercise', block_index=0, 
                 signal_num=config.trial_num[0][0], noise_num=config.trial_num[0][1])

    # block1
    exp.disp_text(wait=1, auto=False, text_0=config.text['start_formal'])
    exp.block_SD(process_name='formal_neutral', block_index=1, 
                 signal_num=config.trial_num[1][0], noise_num=config.trial_num[1][1])
    exp.intermezzo(duration=config.stim_params['duration_rest'])

    # block2
    exp.disp_pic(wait=1, auto=False, pic_0='warning.png')
    exp.disp_pic(wait=1, auto=False, 
                 pic_0='punish_MS.png' if exp.exp_param['manip_order'] == '1' \
                    else 'punish_FA.png')
    exp.disp_text(wait=1, auto=False, text_0=config.text['start_formal'])
    exp.block_SD(process_name='formal_punish_MS' if exp.exp_param['manip_order'] == '1' \
                    else 'formal_punish_FA', 
                 block_index=2, 
                 signal_num=config.trial_num[2][0], noise_num=config.trial_num[2][1])
    exp.intermezzo(duration=config.stim_params['duration_rest'])

    # block3
    exp.disp_pic(wait=1, auto=False, pic_0='warning.png')
    exp.disp_pic(wait=1, auto=False, 
                 pic_0='punish_FA.png' if exp.exp_param['manip_order'] == '1' \
                    else 'punish_MS.png')
    exp.disp_text(wait=1, auto=False, text_0=config.text['start_formal'])
    exp.block_SD(process_name='formal_punish_FA' if exp.exp_param['manip_order'] == '1' \
                    else 'formal_punish_MS', 
                 block_index=3, 
                 signal_num=config.trial_num[3][0], noise_num=config.trial_num[3][1])

    exp.finale()

if __name__ == '__main__':

    launch()