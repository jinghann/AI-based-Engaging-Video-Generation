import glob,os

def find_info_dir(result_dir):
    product_id = os.path.basename(result_dir)
    video_prefix = '/home/liuchang/TAOBAO_items_info'
    video_dir=os.path.join(video_prefix,product_id)
    return video_dir

def find_videos(frame):
    if not os.path.basename(frame).startswith('frame'):
        return None
    video_dir=find_orginal_dir(os.path.dirname(frame))
    video_name=os.path.basename(frame)[len('frame_'):]
    video_name=video_name.split('.')[0]+'.mp4'
    video_path=os.path.join(video_dir,'videos',video_name)
    assert os.path.exists(video_path)
    return video_path

def is_video(frame):
    return frame.split('.')[-1]=='mp4'

def get_all_image(img_dir,need_sort=True):
    all_image=glob.glob(os.path.join(img_dir,'*.png'))+glob.glob(os.path.join(img_dir,'*.jpg'))+glob.glob(os.path.join(img_dir,'*.jpeg'))
    if need_sort:
        return sorted(all_image)
    else:
        return all_image

def get_all_image_wo_shopicon(img_dir):
    all_image=get_all_image(img_dir)
    return [i for i in all_image if 'shop' not in i]

def get_all_product_dir(path='/home/liuchang/Taobao_Material_New/data/gzn/datasets/NTU/LIUCHANG_taobao/*',need_sort=True,limit=None):
    all_product_dir=glob.glob(path)
    all_product_dir=[i for i in all_product_dir if os.path.isdir(i)]
    if need_sort:
        all_product_dir=sorted(all_product_dir)
    if limit is None:
        return all_product_dir
    else:
        return all_product_dir[:limit]
generated_results_path='/home/liuchang/Taobao_Material_New/generate_results/'
generated_movie_path='/home/liuchang/Taobao_Material_New/generate_results/'

def print_shots(shots):
    for i in shots:
        print(i,shots[i])


def get_innx_product_dir(item_list_path='/home/liuchang/Taobao_Material_New/INXX_items.txt',need_sort=True):
    prefix='/home/liuchang/Taobao_Material_New/data/gzn/datasets/NTU/LIUCHANG_taobao/'
    f = open(item_list_path, "r")
    all_id=f.read().split('\n')
    all_id = [os.path.join(prefix,i) for i in all_id if len(i)>=len("4175839609")]
    if need_sort:
        return sorted(all_id)
    else:
        return all_id


def get_product_npy_w_title(result_dir):
    orginal_dir=find_info_dir(result_dir)
    json_dir=os.path.join(orginal_dir,'*.json')
    json_dir=glob.glob(json_dir)[0]
    import json,jieba
    with open(json_dir,'r') as json_file:
        data = json.load(json_file)
        title=data['item']['title']
        title_seg=jieba.cut_for_search(title)

    attr_dir=os.path.join(result_dir,'attr_prob.npy')
    cat_dir = os.path.join(result_dir, 'cate_prob.npy')
    import numpy as np
    assert os.path.exists(attr_dir)
    assert os.path.exists(cat_dir)
    attr=np.load(attr_dir)
    cat=np.load(cat_dir)
    return cat,attr,title_seg

def add_feature(feature_file_dir,feature_name,data):
    import pandas as pd
    features = pd.read_csv(feature_file_dir)
    assert len(features['Image']) == len(data), '{} but data has length {}'.format(len(features['Image']),len(data))
    features[feature_name] = data
    features.to_csv(feature_file_dir, index=False)

def get_feature(feature_file_dir,feature_name,vms):
    import pandas as pd
    features = pd.read_csv(feature_file_dir)
    assert feature_name in features
    all_returns=[]
    imgs=features['Image'].to_numpy(dtype=str)
    for index,img in enumerate(vms):
        assert img in imgs
        feature=features.iloc[img==imgs]
        all_returns.append(feature[feature_name].values[0])
    return all_returns

def list2dict(scores,imgs):
    assert len(scores)==len(imgs)
    d={}
    for i in range(len(scores)):
        d[imgs[i]]=scores[i]
    return d

def get_length_cvpr(product_id):
    #obtain the length of the output sequence
    return 4
def get_seq_output_path(product_id,method):
    return os.path.join("/home/liuchang/Taobao_Material_New/generate_result", product_id,"seq_{}.pkl".format(method))
def get_feature_all_images(feature_file_dir,feature_name):
    import pandas as pd
    features = pd.read_csv(feature_file_dir)
    assert feature_name in features
    return features['Image'].tolist(),features[feature_name].tolist()