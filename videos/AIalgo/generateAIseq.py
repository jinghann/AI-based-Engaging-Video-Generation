from .SeqAlgo import bnb, bnb_rand,main_tsp
import os

def main(algo, file_list):
    """
    function called by django video/views.py to generate AI-empowered sequence
    arguments:
    algo - selected AI algorithm
    file_list - a list of image/video files
    return:
    sequence of file index
    """

    if algo == 'Bnb':
        new_seq = bnb.getAISequence(file_list)
    elif algo == 'Bnb_rand':
        new_seq = bnb_rand.getAISequence(file_list)
    elif algo == 'TSP':
        new_seq = main_tsp.getAISequence(file_list)
    elif algo == 'WBP':
        pass
    elif algo == 'ShotCSP':
        pass
    else:
        # return original sequence if no AI model is specified
        return list(range(len(file_list)))
    return new_seq

if __name__ == '__main__':
    folder = './SeqAlgo/Images'
    file_list = [os.path.join(folder,i) for i in os.listdir(folder) if i != '.DS_Store']
    main('Bnb_rand',file_list)

