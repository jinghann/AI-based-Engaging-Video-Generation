import numpy as np
from skimage import io
from skimage import data, img_as_float,color
from skimage.measure import compare_ssim as ssim
from skimage.transform import rescale, resize, downscale_local_mean
from sklearn.metrics import pairwise_distances

def get_ssim_image(i,j):
    img0=data.load(i)
    img1=data.load(j)
    img0 = resize(img0, (224, 224))
    img1 = resize(img1, (224, 224))
    if img0.shape[-1] == 4:
        img0 = color.rgba2rgb(img0)
    if img1.shape[-1] == 4:
        img1 = color.rgba2rgb(img1)
    img0 = img_as_float(img0)
    img1 = img_as_float(img1)
    similarity = ssim(img0, img1, data_range=max(img0.max(),img1.max()) - min(img0.min(),img1.min()),multichannel=True)

    return similarity

def get_ssim(i,j):
    return get_ssim_image(i,j)

def calc_ssim(imgs,i):
    sim=[1-get_ssim_image(i, j) for j in imgs]
    if (len(imgs)-1)==0:
        return 0
    return np.array(sim).sum().item()/(len(imgs)-1)

def pairwise_ssim(i,j):
    if np.array_equal(i,j):
        return 1

    i=i.reshape(224,224,3)
    j=j.reshape(224,224,3)
    return ssim(i, j, data_range=max(i.max(), j.max()) - min(i.min(), j.min()),
                      multichannel=True)

def get_img(i):
    img = io.imread(i)
    img = resize(img, (224, 224))
    img = color.rgb2lab(img)
    img = img_as_float(img)
    return img

def get_ssim_matrix(vm_source):

    imgs=[]
    for i in vm_source:
        img=get_img(i)
        imgs.append(img.reshape(-1))
    imgs=np.stack(imgs)
    maxtrix=pairwise_distances(X=imgs,metric=pairwise_ssim,n_jobs=32)

    import os
    for index,i in enumerate(vm_source):
        if os.path.basename(i).startswith('frame_'):
            maxtrix[index,:]=0
            maxtrix[:,index]=0
    return maxtrix



if __name__=='__main__':
    vm_source=['/home/liuchang/TaobaoItem/results/5829465570947hh7aT1M/big_005_6.jpg',
     '/home/liuchang/TaobaoItem/results/5829465570947hh7aT1M/big_007_5.jpg']
    matrix=get_ssim_matrix(vm_source)
    print(matrix)
    print(matrix.shape)