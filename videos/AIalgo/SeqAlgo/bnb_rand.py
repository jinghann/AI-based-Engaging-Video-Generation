import os
import sys
import glob
import math
import cv2
import numpy as np
import multiprocessing as mp
import heapq
from random import shuffle
import time
from . import util, util_2rnn, utils
import tqdm

S = 0
results = []
known_sim = []
lam = 0.5
dynamic_list = []

def get_dynamic_score(file_list):
    ans = []
    for i in file_list:
        if not utils._dir_is_image(i):
            ans.append(utils._video_dynamic(i))
        else:
            ans.append(0)
    return np.array(ans)

def plot_penalty(A):
    global dynamic_list

    d = dynamic_list[A]

    p_func = lambda x,y:x-y if y<x else 0
    return np.sum([p_func(d[i],d[i+1]) for i in range(len(d)-1)])


def dissim(file_list):
    global known_sim

    for i in list(range(len(file_list))):
        for j in list(range(len(file_list))):
            if i >= j:
                known_sim[i][j]=math.inf # for future bnb
            elif not utils._dir_is_image(file_list[i]):
                if utils._dir_is_image(file_list[j]):#consider parallel differnt image against same video
                    known_sim[i][j] = utils._image_video_dissim(file_list[j], file_list[i])
                else:
                    known_sim[i][j] = utils._video_video_dissim(file_list[i], file_list[j])
            elif not utils._dir_is_image(file_list[j]):
                known_sim[i][j] = utils._image_video_dissim(file_list[i], file_list[j])
            else:
                known_sim[i][j] = utils._image_image_dissim(file_list[i], file_list[j])
    return

def get_dis(seq):
    global known_sim
    s = 0.0
    for i in list(range(len(seq)-1)):
        if seq[i] > seq[i+1]:
            s += known_sim[seq[i+1]][seq[i]]
        else:
            s += known_sim[seq[i]][seq[i + 1]]
    return s


def get_score(seq):
    plot = plot_penalty(seq)
    dis = get_dis(seq)
    sc = 0.5 * plot + 0.5 * dis
    #print(seq,sc)
    return  sc


def getAISequence(file_list):
    """
    function called by django views.py
    input: a list of files (image/video)
    return: the sequence index 
    """
    global known_sim, results, dynamic_list
    S = len(file_list)
    dynamic_list = get_dynamic_score(file_list)

    N = len(file_list)
    known_sim=np.zeros((N,N))
    dissim(file_list)
    
    sc=math.inf
    L = list(range(N))
    lis = []
    
    for i in range(150):
        L = list(range(N))
        shuffle(L)
        L1 = L[:S]
        shuffle(L1)
        tmp = get_score(L1)
        if sc > tmp:
            sc = tmp
            lis = L1 

    # print result sequence of file index
    print("output sequence:\n",lis)
    # print result sequence of file path
    print([file_list[i] for i in lis])
    
    # return sequence
    return lis  


if __name__ == '__main__':

    folder = './Images'
    file_list = [os.path.join(folder,file) for file in os.listdir(folder)]
    print("input file list:\n",file_list)
    getAISequence(file_list)

