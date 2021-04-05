from . import util

def get_vms_cvpr(product_dir):
    imgs=util.get_all_image_wo_shopicon((product_dir))
    for i in range(len(imgs)):
        if imgs[i].endswith('frame.jpg'):
            imgs[i]=imgs[i][:-len('frame.jpg')]+'mp4'
    return imgs