from djongo import models
from django.utils import timezone
from django.contrib.auth.models import User



def user_directory_path_upload(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'uploadedFiles/user_{0}/{1}'.format(instance.user.id, filename)

def user_directory_path_generate(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'generatedVideos/user_{0}/{1}'.format(instance.user.id, filename)

class Project(models.Model):
    '''
    Model to store video project for futuring editing
    '''
    title = models.CharField(max_length=100,default="New Project")
    date_created = models.DateTimeField(default=timezone.now) #date created
    thumbnail = models.FileField(upload_to="projectFiles/")
    AI_algo = models.TextField()
    cust_seq = models.TextField()
    cust_dur = models.TextField()
    cust_speed = models.TextField()
    author = models.ForeignKey(User, on_delete =  models.CASCADE) #if the user who created the video is deleted, the project is then deleted.

    def __str__(self):
        return "{}'s Project".format(self.author.username)

class ProjectFile(models.Model):
    '''
    Model to store user uploaded files for draft project - either image or video file
    '''
    file = models.FileField(upload_to='projectFiles/')
    project = models.ForeignKey(Project,on_delete=models.CASCADE) # uploaded files will be deleted when a project is deleted

    def __str__(self):
        return self.file.url
