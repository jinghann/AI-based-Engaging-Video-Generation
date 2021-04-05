import os
import sys
import glob
import math
import cv2
import numpy as np
from . import utils
import multiprocessing as mp
import heapq


results=[]
known_sim=[]
dynamic_list=[]

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

    d=dynamic_list[A]
    #print(d)
    p_func=lambda x,y:x-y if y<x else 0
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


def sub_space(index,D,seq,length):
    # subspace seq::index
    global dynamic_list
    # (N-n)m the same if seq the same
    if len(seq) != 0:
        for i in range(len(seq)):
            num = seq[i]
            flag = num + 1
            for j in range(num):
                D[j][num] = math.inf
            while flag < length:
                D[num][flag] = math.inf
                flag += 1
    flattened_D = [y for x in D for y in x]
    minis = heapq.nsmallest((min(8, length) - len(seq) - 1), flattened_D)  # (N-n)m in lower-bound  same if seq same
    seq.append(index)
    cost_already = get_score(seq)
    mini = 0.5 * sum(minis) + cost_already # first item the same for the same seq

    # find a upper bound
    lis=[]
    num= index
    flag = num
    sum1=0
    upper_seq = seq.copy()

    while len(upper_seq) < min(8,length):
        for j in range(num):
            lis.append(D[j][num])
        while flag < length:
            lis.append(D[num][flag])
            flag += 1

        for i in range(len(lis)):
            if i in upper_seq:
                lis[i] = math.inf
                continue
            if dynamic_list[i] < dynamic_list[num]:
                lis[i] += dynamic_list[num] - dynamic_list[i]

        les = min(lis)
        ind = lis.index(les)

        sum1 += les
        upper_seq.append(ind)
        num = ind
        flag=num
        lis=[]

    sum1=0.5*sum1+cost_already

    return sum1, mini


def getAISequence(file_list, M=5):
    """
    function called by django view.py
    """
    global known_sim, results, dynamic_list

    dynamic_list = get_dynamic_score(file_list)   

    N = len(file_list)
    known_sim = np.zeros((N,N))
    dissim(file_list)

    L1 = []
    for n in range(N):
        L1.append([n])

    Lold = L1[:]
    count=0

    while True:

        Lb = []
        Ub = []
        L1 = []

        for seq in Lold:
            for nxt in list(range(N)):
                if nxt not in seq:
                    se1=seq.copy()
                    se1.append(nxt)
                    L1.append(se1)
                    d=known_sim.copy()
                    up,lo = sub_space(nxt, d, seq.copy(), N)
                    Lb.append(lo)
                    Ub.append(up)

        minUp = min(Ub)
        Lold=[]
        for i in range(len(L1)):
            if Lb[i] <= minUp:
                Lold.append(L1[i])

        count+=1
        if len(Lold)==1 or count==min(N-1,M):
            break
    # Lold[0] : index of image from the input file list in sequence
    print("output sequence:\n",Lold[0])
    # print img path in generated sequence
    print([file_list[i] for i in Lold[0]])
    return Lold[0]     



if __name__ == '__main__':
    folder = './Images'
    file_list = [os.path.join(folder,file) for file in os.listdir(folder)]
    print("input file list:\n",file_list)
    getAISequence(file_list)


