from django.urls import path
from . import views

urlpatterns = [
    path('', views.createVideoHome, name='create-video-home'),
    path('edit-video/', views.editVideoMain, name='edit-video-main'),
    path('edit-video-draft/<int:pk_id>/', views.editVideoMainFromDraft, name='edit-video-main-draft'),
    path('upload-file/',views.uploadFiles,name='upload-file'),
    path('customize-video/',views.updateVideo,name='customize-video'),
    path('create-post/',views.createPost,name='create-post'),
    path('save-project/<int:pj_id>/',views.saveProject,name='save-project'),
    path('delete-draft/<int:pj_id>/', views.deleteDraft, name='delete-draft'),
]
