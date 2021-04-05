import time
import random
def __generate_evaluate(input_pair):
    n_range,to_select_N,matrix=input_pair
    seq=random.sample(n_range,to_select_N)
    seq_v=0
    for index,i in enumerate(seq[1:]):
        seq_v+=matrix[i][seq[index]]
    return seq,seq_v

def random_select(m,N=20,worker=4,time_limit_min=0.5):
    to_select_N=N
    n_range=list(range(len(m)))
    matrix=m
    from multiprocessing import pool
    pool=pool.Pool(worker)
    t0=time.time()
    bst=1000
    bst_seq=None
    while time.time()-t0<time_limit_min*60:
        for seq,seq_v in pool.imap_unordered(__generate_evaluate,[(n_range,to_select_N,matrix)]*worker):
            if seq_v<bst:
                bst=seq_v
                bst_seq=seq
    return bst_seq,bst

if __name__ == '__main__':
    import numpy as np
    matrix=np.random.rand(5,5)
    seq,seq_v=random_select(matrix,N=3,time_limit_min=0.1,worker=16)
    print(seq,seq_v)


