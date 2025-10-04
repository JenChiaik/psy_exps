import kernel
from config import config

def launch():

    exp = kernel.Event(json_file='random_array.json')

    exp.overture()
    exp.prelude()

    exp.disp_pic(pic_0='1.png', pic_1='1.png', wait=2, auto=False)
    exp.disp_pic(pic_0='2.png', pic_1='2.png', wait=2, auto=False)
    exp.disp_pic(pic_0='3.png', pic_1='3.png', wait=2, auto=False)

    exp.disp_text(text_0=config.text['start_exercise'], text_1=config.text['start_exercise'], 
                  wait=2, auto=False)
    exp.block_SD(mode='solo', block_index=0, 
                 signal_num=config.trail_num['exercise'][0], noise_num=config.trail_num['exercise'][1])
    exp.disp_text(text_0=config.text['stage_end'], text_1=config.text['stage_end'], wait=2, auto=True)

    exp.disp_text(text_0=config.text['start_formal'], text_1=config.text['start_formal'], 
                  wait=2, auto=False)
    exp.block_SD(mode='solo', block_index=1, 
                 signal_num=config.trail_num['solo'][0], noise_num=config.trail_num['solo'][1])
    exp.disp_text(text_0=config.text['stage_end'], text_1=config.text['stage_end'], wait=2, auto=True)

    exp.disp_text(text_0=config.text['call_me'], text_1=config.text['call_me'], 
                  wait=2, auto=False)

    exp.disp_pic(pic_0='4.png', pic_1='4.png', wait=2, auto=False)
    exp.disp_text(text_0=config.text['start_formal'], text_1=config.text['start_formal'], 
                  wait=2, auto=False)
    exp.block_SD(mode='dual', block_index=2, 
                 signal_num=config.trail_num['dual'][0], noise_num=config.trail_num['dual'][1])
    exp.disp_text(text_0=config.text['stage_end'], text_1=config.text['stage_end'], wait=2, auto=True)

    exp.finale()

