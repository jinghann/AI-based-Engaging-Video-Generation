from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.conf import settings
from django.urls import reverse
from django.core.files import File
from django.core import serializers
from django.views .generic import ListView,DetailView
from django.contrib.auth.models import User
from .models import Project,ProjectFile
from posts.models import Post,PostFile,Comment
from posts.views import PostListView
from .AIalgo import generateAIseq
import time
import filetype
import uuid # for generating unique file name
import json
import ast
from PIL import Image
import cv2
import numpy as np
import random
from moviepy.editor import *


# global var for referencing the files user upload from frontend
# used for user customization of video
fileSrc = []   # the file path
custDur = []
custSpeed = []
# For saving and serving generated video during editing,
# and will also help with refering the video to store when creating post and project
VIDEO_PATH = settings.MEDIA_ROOT + '/generatedVideos/output_video.mp4'
VIDEO_URL = settings.MEDIA_URL + 'generatedVideos/output_video.mp4'

# For saving project and creating post purpose
AISeq = []
AIAlgo = ""
custSeq = []


# View functions which render a new template


@login_required
def createVideoHome(request):
    '''
    Render Create Video Home Page
    '''
    drafts = Project.objects.filter(author=request.user).order_by('-date_created')

    return render(request,'videos/create_video_home.html',{'draft':drafts})

@login_required
def editVideoMain(request):
    '''
    Render Edit Video Main Page starting a new project
    '''

    return render(request,'videos/edit_video_main.html')


@login_required
def editVideoMainFromDraft(request,pk_id,*args,**kwargs):
    '''
    Render Edit Video Main Page continuing with draft project
    '''
    global fileSrc,custDur,custSpeed
    # receive project object id from request
    project = Project.objects.get(pk=pk_id)
    project_files = ProjectFile.objects.filter(project=project)

    custDur = ast.literal_eval(project.cust_dur)
    custSpeed = ast.literal_eval(project.cust_speed)

    # 初始化fileSrc,custDur,custSpeed
    img_urls = []
    fileSrc = []
    org_dur = []
    for pjfile in project_files:
        url = pjfile.file.url
        img_urls.append(url)
        src = url.replace(settings.MEDIA_URL,settings.MEDIA_ROOT+'/')
        fileSrc.append(src)
    for src in fileSrc:
        if filetype.guess(src).mime.startswith("image"):
            org_dur.append([0,2])
        elif filetype.guess(src).mime.startswith("video"):
            org_dur.append([0,VideoFileClip(src).duration])

    msg = {'project':project,
            'project_files':project_files,
            'img_urls':img_urls,
            'org_dur':org_dur}

    return render(request,'videos/edit_video_main_continue_draft.html',msg)


@login_required
def createPost(request):
    '''
    Handle creating post functions
    redirect to system home Page
    '''
    if request.method == "POST":
        title = request.POST.get('post-title')
        content = request.POST.get('post-content')
        is_private = request.POST.get('post-visibility')
        author = request.user

        # 存储数据到数据库
        # create a new post record
        new_post = Post(title = title,
                        content = content,
                        author = author,
                        is_private=is_private,
                        AI_algo = AIAlgo,
                        AI_seq = AISeq,
                        cust_seq = custSeq,
                        cust_dur = custDur,
                        cust_speed = custSpeed)

        with open(VIDEO_PATH,'rb') as vf:
            # 生成随机文件名
            file_name = uuid.uuid4().hex
            new_post.video.save(file_name,File(vf))
        new_post.save()

        # save all the uploaded files
        for src in fileSrc:
            new_postfile = PostFile(post = new_post)
            # 生成随机文件名
            file_name = uuid.uuid4().hex
            with open(src,'rb') as f:
                new_postfile.file.save(file_name,File(f))


    # 返回到home页面
    return redirect('/')

@login_required
def saveProject(request,pj_id,*args,**kwargs):
    '''
    Handle saving project as draft function
    Redirect to create video home Page
    '''
    if request.method == "POST":
        title = request.POST.get('save-title')
        new_project = Project(title=title,
                              AI_algo=AIAlgo,
                              cust_seq=custSeq,
                              cust_dur=custDur,
                              cust_speed=custSpeed,
                              author=request.user)

        with open(VIDEO_PATH,'rb') as vf:
            # 生成随机文件名
            file_name = uuid.uuid4().hex
            new_project.thumbnail.save(file_name,File(vf))

        new_project.save()

        for src in fileSrc:
            new_projectfile = ProjectFile(project=new_project)
            # 生成随机文件名+原文件类型后缀
            file_name = uuid.uuid4().hex + '.' + src.split('.')[-1]
            with open(src,'rb') as f:
                new_projectfile.file.save(file_name,File(f))
        # delete the original project if any
        if pj_id != 9999:
            old_project = Project.objects.get(pk=pj_id)
            old_project.delete()

        # 返回到create video home 页面
        return redirect('/create-video')


# View functions which do not render new templates
def uploadFiles(request):

    global fileSrc,AIAlgo,AISeq,custSeq

    if request.method == "POST" and request.is_ajax():
        # 用户选择A的I模型
        model = request.POST.get('model')
        # 用户上传的图片/视频
        files = request.FILES.getlist('uploads[]')
        # 保存文件
        saveFiles(files)
        # 1. 获得AI模型输出的顺序
        ai_seq = getAIsequence(model,fileSrc)
        custSeq = ai_seq
        # 更新全局变量
        AISeq = ai_seq
        AIAlgo = model
        # 2. 生成视频
        video = generateVideo(ai_seq)
        # 3. 保存生成的视频
        save_path = VIDEO_PATH
        video.write_videofile(save_path,fps=24)
        # 4. 将生成的视频url返回前端
        video_url = VIDEO_URL
        backInfo = {
            'sequence': ai_seq,
            'initDuration': custDur,
            'speed': custSpeed,
            'url': video_url
        }

        return JsonResponse(backInfo,safe=False)

def updateVideo(request):
    global custSeq, custDur, custSpeed
    backInfo = []
    if request.method == "POST" and request.is_ajax():
        cust_seq = request.POST.getlist("seq")
        cust_dur = request.POST.getlist("duration")
        cust_speed = request.POST.getlist("speed")
        print("User customizing sequence: ",cust_seq)
        print("custom duartion: ",cust_dur) # ['0,2'.'0,2.5']
        print("custom speed: ",cust_speed) # ['1','1','1']

        cust_seq = [int(index) for index in cust_seq]
        # 更新custSeq
        custSeq = cust_seq
        # 更新custDur、custSpeed
        for i in range(len(cust_seq)):
            src_index = cust_seq[i]
            custDur[src_index] = [float(val) for val in cust_dur[i].split(',')]
            custSpeed[src_index] = float(cust_speed[i])

        # 生成视频
        video = generateVideo(cust_seq)
        # 保存生成的视频
        save_path = VIDEO_PATH
        video.write_videofile(save_path,fps=24)
        # 将生成的视频url返回前端
        video_url = VIDEO_URL
        backInfo = {
            'url': video_url
        }

        return JsonResponse(backInfo,safe=False)


def getAIsequence(algo, file_srcs):
    """
    function to get AI-empowered sequence of files
    arguments:
    algo: choosen AI algorithm
    file_srcs: an array of file paths
    """
    print('Processing file list:\n',file_srcs)
    new_seq = generateAIseq.main(algo, file_srcs)

    return new_seq

def generateVideo(new_seq):
    """
    argument: a list of file paths of image / short videos
    return: a composed video
    """

    clips = []
    for src_index in new_seq:
        src = fileSrc[src_index]
        if filetype.guess(src).mime.startswith("image"):
            video_clip = generateVideofromImage(src_index)

        elif filetype.guess(src).mime.startswith("video"):
            video_clip = generateVideofromVideo(src_index)

        else:
            print("Error: Uploaded file has wrong type!")

        clips.append(video_clip)
    concat_video = concatenate_videoclips(clips, method="compose")

    return concat_video


def generateVideofromImage(src_index):
    """
    generate video clip from an image (image/*)
    uisng moviepy
    arguments:
    src_index - image file path index from fileSrc
    """
    src = fileSrc[src_index]
    duration = custDur[src_index]
    speed = custSpeed[src_index]
    img = Image.open(src)
    # apply duration cut and speed up
    # for image the actual effect will vary in clip duration
    clip = ImageClip(np.array(img)).set_duration(duration[1]-duration[0]).fx(vfx.speedx,speed)
    # image clip default duration is 2s
    # clip.write_videofile("./output_test.mp4",fps=24)
    return clip

def generateVideofromVideo(src_index):
    """
    generate video clip from a video (video/*)
    using moviepy
    src_index - video file path index from fileSrc
    """
    # for moviepy VideoFileClip to create the video clip from python InMemoryUploadedFile object,
    # need to save the file object into a file first
    # haven't think of a better way to do this
    src = fileSrc[src_index]
    duration = custDur[src_index]
    speed = custSpeed[src_index]

    start = time.time()
    clip = VideoFileClip(src)
    print('Time-clip: ',time.time()-start)
    # apply duration cut and speed up
    clip = VideoFileClip(src).subclip(duration[0],duration[1]).fx(vfx.speedx,speed)

    return clip

def saveFiles(files):
    """
    function to save user uploaded images/videos on server for AI algorithm to process
    """
    global fileSrc,custDur, custSpeed,custSeq
    # 重置全局变量
    fileSrc = []
    custDur = []
    custSpeed = []
    custSeq = []


    src_list = []

    for i in range(len(files)):
        # 新文件src
        name = '{}.{}'.format(i,files[i].name.split('.')[-1])
        src = settings.MEDIA_ROOT + '/processing_files/'+ name
        # 保存图片到服务器
        if files[i].content_type.startswith("image"):
            img = Image.open(files[i])
            img.save(src)
            src_list.append(src)
            custDur.append([0,2])
            custSpeed.append(1)
        # 保存视频到服务器
        elif files[i].content_type.startswith("video"):
            start = time.time()
            with open(src,'wb+') as vidfile:
                for chunk in files[i].chunks():
                    vidfile.write(chunk)
            src_list.append(src)

            print('Time: ',time.time()-start)
            custDur.append([0,VideoFileClip(src).duration])
            custSpeed.append(1)
        else:
            print('File type not acceptable.')

    fileSrc = src_list

def deleteDraft(request,pj_id,*args,**kwargs):
    to_delete = Project.objects.get(pk=pj_id)
    to_delete.delete()
    return redirect('/create-video')
