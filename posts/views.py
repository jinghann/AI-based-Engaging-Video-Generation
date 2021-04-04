from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse,JsonResponse
from django.views .generic import ListView,DetailView,TemplateView,DeleteView
from .models import Post,Comment
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# def home(request):
#     context = {
#         'posts': Post.objects.all()
#     }
#     return render(request,'posts/home.html',context)


class PostListView(ListView):
    model = Post
    template_name = 'posts/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted'] # order the posts from newest to oldest
    paginate_by = 6

    def get_queryset(self):
        return Post.objects.filter(is_private=False).order_by('-date_posted')



class UserPostListView(ListView):
    model = Post
    template_name = 'posts/user_posts.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']  # newest post at top
    paginate_by = 6

    def get_queryset(self):
        user = get_object_or_404(User,username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(TemplateView):
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
         context = super(PostDetailView, self).get_context_data(**kwargs)
         context['post'] = Post.objects.get(pk=self.kwargs.get('pk'))
         context['comments'] = Comment.objects.filter(post=context['post']).order_by('-date_commented') # latest comment first
         return context

def deletePost(request,post_id,*args,**kwargs):
    post_to_delete = Post.objects.get(pk=post_id)
    if post_to_delete.author == request.user:
        #delete the post
        post_to_delete.delete()

    return redirect('/user-posts/'+request.user.username+'/')

def about(request):
    return render(request,'posts/about.html',{'title':'About'})

def createNewComment(request):
    if request.method == 'POST':
        content = request.POST.get('comment')
        post_id = request.POST.get('post_id')
        author = request.user
        post = Post.objects.get(pk=post_id)
        new_comment = Comment(post=post,author=author,content=content)
        new_comment.save()
        return JsonResponse({'success':1})
