from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import Http404
from .forms import CommentForm
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post,Comment
from django import forms
from django.http import HttpResponse
try:
    from django.utils import simplejson as json
except ImportError:
    import json

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
import bleach
from django.conf import settings
from blog.tree_dfs import *
#Comment.objects.all().delete()
deletedComments=init_graph()
print (deletedComments)

# Create your views here.
#context={"img":"blog/lsup.png"}
def home(request):
	return render(request, 'blog/home.html')
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5
    #success_url = '/blog/'




class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class BranchPostListView(ListView):
    model = Post
    template_name = 'blog/branch_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        #user = get_object_or_404(User, username=self.kwargs.get('username'))
        #return Post.objects.filter(branch=self.kwargs.get('branch')).order_by('-date_posted')
        BRANCH_CHOICES =['Computer',
                        'Electrical',
                        'Civil',
                        'I.T',
                        'Mechanical',
                        'All']
        valid_url = False
        for i in BRANCH_CHOICES:
            if (i==self.kwargs.get('branch')):
                valid_url=True
        if (valid_url==False):
            raise Http404
        posts = Post.objects.none()
        posts_all = Post.objects.all()
        if (self.kwargs.get('branch')=="All"):
            posts=posts_all
        else:
            for post in posts_all:
                for i in range(len(post.branch)):
                    if (post.branch[i] == self.kwargs.get('branch') or post.branch[i]=="All"):
                        current_post = Post.objects.filter(pk=post.pk) # to convert post object into queryset
                        posts|=current_post
        return posts.order_by('-date_posted')

class YearPostListView(ListView):
    model = Post
    template_name = 'blog/year_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        #user = get_object_or_404(User, username=self.kwargs.get('username'))
        #return Post.objects.filter(branch=self.kwargs.get('branch')).order_by('-date_posted')
        YEAR_CHOICES =['First','Second','Third','Fourth']
        valid_url = False
        for i in YEAR_CHOICES:
            if (i==self.kwargs.get('year_of_admission')):
                valid_url=True
        if (valid_url==False):
            raise Http404

        posts = Post.objects.none()
        posts_all = Post.objects.all()
        for post in posts_all:
            for i in range(len(post.year_of_admission)):
                if (post.year_of_admission[i] == self.kwargs.get('year_of_admission')):
                    current_post = Post.objects.filter(pk=post.pk) # to convert post object into queryset
                    posts|=current_post

        posts_branch = Post.objects.none()
        if (self.kwargs.get('branch')=="All"):
            posts_branch=posts
        else:
            for post in posts:
                for i in range(len(post.branch)):
                    if (post.branch[i] == self.kwargs.get('branch') or post.branch[i]=="All"):
                        current_post = Post.objects.filter(pk=post.pk) # to convert post object into queryset
                        posts_branch|=current_post
        return posts_branch.order_by('-date_posted')

class CommentFormView(LoginRequiredMixin, CreateView):

    model = Comment
    fields=['content']
    def form_valid(self, form):
        global deletedComments
        print (self.request.POST.get('parent_id'))
        print (Comment.objects.count())

        if (Comment.objects.count()>0 and deletedComments==1):
            print ('lets see')

            deletedComments=init_graph()

        deletedComments+=1
        addNode()
        if (self.request.POST.get('parent_id')!='none'):
            form.instance.parent = Comment.objects.filter(pk=self.request.POST.get('parent_id')).first()
            addEdge(int(self.request.POST.get('parent_id')),deletedComments)

        print (adj)
        form.instance.author = self.request.user
        posts_all = Post.objects.filter(pk=self.kwargs.get('pkey'))
        for post in posts_all:
            form.instance.post = post
        content = form.instance.content
        print (content)
        cleaned_text = bleach.clean(content, settings.BLEACH_VALID_TAGS, settings.BLEACH_VALID_ATTRS, settings.BLEACH_VALID_STYLES)
        form.instance.content = cleaned_text
        return super().form_valid(form)
    #form_class = CommentForm
    #print (form_class)
    #success_url = '/'

class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    fields = ['content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        posts_all = Post.objects.filter(pk=self.kwargs.get('pkey'))
        for post in posts_all:
            form.instance.post = post

        content = form.instance.content
        print (content)
        cleaned_text = bleach.clean(content, settings.BLEACH_VALID_TAGS, settings.BLEACH_VALID_ATTRS, settings.BLEACH_VALID_STYLES)
        form.instance.content = cleaned_text
        return super().form_valid(form)

#CommentForm(instance=comment_first),

class PostDetailView(DetailView):
    model = Post
    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['form_only']=CommentForm()
        form_list = []
        comment_list=[]
        comments_all = Comment.objects.all()
        comments_display = Comment.objects.all()
        indent_list=[]
        x="x"
        if (Comment.objects.count()>1):
            fCom=Comment.objects.first()
            source = fCom.pk

            comments_display = dfsDisconnected(source)
            print ("Ordered List is " )
            print (comments_display)
        #print (comments_display)
            for comment in comments_display:
                print (comment)
                comments=Comment.objects.filter(pk=int(comment[0])).first()
                if (comments.post.pk == self.kwargs.get('pk')):
                    #comments.spc=int(comment[1])
                    form_list.append(CommentForm(instance=comments))
                    comment_list.append(comments)
                    indent_list.append(x*(comment[1]))
        else:
            for comments in comments_all:
                if (comments.post.pk == self.kwargs.get('pk')):
                    form_list.append(CommentForm(instance=comments))
                    comment_list.append(comments)
                    indent_list.append("")

        #context['form']=form_list

        my_list = zip(comment_list,indent_list,form_list)
        context['my_list']=my_list
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title','year_of_admission','branch', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title','year_of_admission','branch', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


@login_required
@require_POST
def like(request):
    if request.method == 'POST':
        user = request.user
        pkey = request.POST.get('pkey',None)
        ld = request.POST.get('liked')
        type = request.POST.get('type')
        ctx = None
        if type=='Post':
            post = get_object_or_404(Post,pk=pkey)
            if (ld =='Yes'):
                if post.likes.filter(id=user.id).exists():
                    # user has already liked this company
                    # remove like/user
                    #post.likes.remove(user)
                    message = 'You have liked this once.'
                else:
                    # add a new like for a company
                    post.likes.add(user)
                    if post.dislikes.filter(id=user.id).exists():
                        post.dislikes.remove(user)
                    message = 'You liked this.Your vote will be updated soon.'
            else:
                if post.dislikes.filter(id=user.id).exists():
                    # user has already liked this company
                    # remove like/user
                    #post.likes.remove(user)
                    message = 'You have disliked this once.'
                else:
                    # add a new like for a company
                    post.dislikes.add(user)
                    if post.likes.filter(id=user.id).exists():
                        post.likes.remove(user)
                    message = 'You disliked this.Your vote will be updated soon.'

            ctx = {'likes_count': post.total_likes, 'message': message}
        else :
            comment = get_object_or_404(Comment,pk=pkey)
            if (ld =='Yes'):
                if comment.likes_comment.filter(id=user.id).exists():
                    # user has already liked this company
                    # remove like/user
                    #post.likes.remove(user)
                    message = 'You have liked this once.'
                else:
                    # add a new like for a company
                    comment.likes_comment.add(user)
                    if comment.dislikes_comment.filter(id=user.id).exists():
                        comment.dislikes_comment.remove(user)
                    message = 'You liked this.Your vote will be updated soon.'
            else:
                if comment.dislikes_comment.filter(id=user.id).exists():
                    # user has already liked this company
                    # remove like/user
                    #post.likes.remove(user)
                    message = 'You already disliked this'
                else:
                    # add a new like for a company
                    comment.dislikes_comment.add(user)
                    if comment.likes_comment.filter(id=user.id).exists():
                        comment.likes_comment.remove(user)
                    message = 'You disliked this.Your vote will be updated soon.'

            ctx = {'likes_count': comment.total_likes, 'message': message}
    # use mimetype instead of content_type if django < 5
    #return redirect('blog-home')
    return HttpResponse(json.dumps(ctx), content_type='application/json')

@login_required
@require_POST
def just_parent(request):
    if request.method == 'POST':
        print (request.POST.get('parent'))
        ctx={'message':'nothing'}
    return HttpResponse(json.dumps(ctx), content_type='application/json')

'''
@login_required
@require_POST
def like(request):
    if request.method == 'POST':
        user = request.user
        pkey = request.POST.get('pkey',None)
        post = get_object_or_404(Post,pk=pkey)
        print ("like")
        if post.likes.filter(id=user.id).exists():
            # user has already liked this company
            # remove like/user
            #post.likes.remove(user)
            message = 'You already liked this'
        else:
            # add a new like for a company
            post.likes.add(user)
            if post.dislikes.filter(id=user.id).exists():
                post.dislikes.remove(user)
            message = 'You liked this'

    ctx = {'likes_count': post.total_likes, 'message': message}
    # use mimetype instead of content_type if django < 5
    #return redirect('blog-home')
    return HttpResponse(json.dumps(ctx), content_type='application/json')
'''
