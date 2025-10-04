from kernel import Event
from config import config

def launch():

    exp = Event()

    exp.overture()
    exp.prelude()

    exp.intermezzo(duration=config.duration['wait_resting_state'])

    exp.disp_text(wait=config.duration['wait_intro'], auto=False, text_0=config.text['welcome'])

    for i in range(config.stim_params['block']):

        exp.block(block_index=i)

    exp.finale()



if __name__ == '__main__':

    launch()