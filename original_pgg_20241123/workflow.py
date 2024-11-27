
import event
from config import config

def launch():

    exp = event.Event()

    topic_mode = True if exp.exp_param['condition_A'] == '1' else False

    exp.overture()

    exp.page_pic(pic_0='0_welcome.png', pic_1='0_welcome.png', wait=2, auto=False)
    exp.page_pic(pic_0='1_QRcode_1.png', pic_1='1_QRcode_1.png', wait=2, auto=False)

    exp.page_pic(pic_0='2_choice_1.png', pic_1='2_choice_1.png', wait=2, auto=False)
    exp.page_pic(pic_0='2_choice_2.png', pic_1='2_choice_2.png', wait=2, auto=False)
    exp.STAGE_choice(topic_dict=config.topic_dict, STAGE_index=1, 
                     intermezzo='3_discussion.png', 
                     condition_same=topic_mode, duration=120)
    exp.STAGE_choice(topic_dict=config.topic_dict, STAGE_index=2, 
                     intermezzo='3_discussion.png', 
                     condition_same=topic_mode, duration=120)
    exp.STAGE_choice(topic_dict=config.topic_dict, STAGE_index=3, 
                     intermezzo='3_discussion.png', 
                     condition_same=topic_mode, duration=120)
    # exp.STAGE_choice(topic_dict=config.topic_dict, STAGE_index=1, 
    #                  intermezzo='3_discussion_same.png' if exp.exp_param['condition_A'] == '1' else '3_discussion_diff.png', 
    #                  condition_same=topic_mode, duration=120)
    # exp.STAGE_choice(topic_dict=config.topic_dict, STAGE_index=2, 
    #                  intermezzo='3_discussion_same.png' if exp.exp_param['condition_A'] == '1' else '3_discussion_diff.png', 
    #                  condition_same=topic_mode, duration=120)
    # exp.STAGE_choice(topic_dict=config.topic_dict, STAGE_index=3, 
    #                  intermezzo='3_discussion_same.png' if exp.exp_param['condition_A'] == '1' else '3_discussion_diff.png', 
    #                  condition_same=topic_mode, duration=120)

    exp.page_pic(pic_0='4_pgg_1.png', pic_1='4_pgg_1.png', wait=2, auto=False)
    exp.page_pic(pic_0='4_pgg_2.png', pic_1='4_pgg_2.png', wait=2, auto=False)

    exp.page_text(text_0=config.static_text['exercise_pgg'], text_1=config.static_text['exercise_pgg'], wait=2, auto=False)
    exp.STAGE_PGG(STAGE_index=0, STAGE_trials=1, total_token=10, multiply=0.75, 
                  show_trial_result=True, show_STAGE_reward=True)
    
    exp.page_pic(pic_0='4_pgg_3.png', pic_1='4_pgg_3.png', wait=60, auto=True)
    
    exp.page_text(text_0=config.static_text['formal_pgg'], text_1=config.static_text['formal_pgg'], wait=5, auto=True)
    exp.STAGE_PGG(STAGE_index=1, STAGE_trials=12, total_token=10, multiply=0.75, 
                  show_STAGE_reward=True, show_trial_result=True)
    
    exp.page_pic(pic_0='5_QRcode_2.png', pic_1='5_QRcode_2.png', wait=2, auto=False)
    exp.finale()

if __name__ == '__main__':

    launch()
