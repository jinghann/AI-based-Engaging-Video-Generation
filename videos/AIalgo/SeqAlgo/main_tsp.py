import os
import sys
from . import ssim, util, random_select

def getAISequence(file_list):
    """
    function called by django view.py
    """
    n = len(file_list)
    matrix = ssim.get_ssim_matrix(file_list)
    seq,_ = random_select.random_select(matrix,N=n,time_limit_min=0.1)

    # print result sequence of file index
    print("output sequence:\n",seq)
    # print result sequence of file path
    print([file_list[i] for i in seq])
    return seq



if __name__ == '__main__':
    folder = './Images'
    file_list = [os.path.join(folder,file) for file in os.listdir(folder)]
    print("input file list:\n",file_list)

    seq = getAISequence(file_list)

