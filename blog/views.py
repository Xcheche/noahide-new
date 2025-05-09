from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import (TemplateView,ListView, DetailView)

from blog.forms import CommentForm
from blog.models import Post
from events.models import Event
from src import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import Http404, JsonResponse
from .models import Subscriber
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
# Create your views here.


from django.views.decorators.cache import cache_page

from django.core.cache import cache

# Set
cache.set('my_key', 'hello', timeout=60)  # 60 seconds

# Get
value = cache.get('my_key')  # returns 'hello'

# @cache_page(60 * 15)  # 15 minutes
class HomeView(ListView):
    
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    paginate_by = 3  # Number of posts per page

    def get_queryset(self):
        return Post.objects.annotate(comment_count=Count('comments')).filter(status='published').order_by('-created_at')
    
    
    #Events
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['events'] = Event.objects.filter(status='published').order_by('-created_at')  # or .upcoming() if you have a manager
        return context
    
    ## Subscribe to newsletter
    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            email = request.POST.get("email")
            try:
                validate_email(email)
                if Subscriber.objects.filter(email=email).exists():
                    return JsonResponse({"status": "error", "message": "Already subscribed!"})
                if "@"   not in email:
                    return JsonResponse({"status": "error", "message": "Invalid email address."})
                # Create a new subscriber
                Subscriber.objects.create(email=email)
                return JsonResponse({"status": "success", "message": "Subscribed successfully!"})
            except ValidationError:
                return JsonResponse({"status": "error", "message": "Enter a valid email address."})
        return JsonResponse({"status": "error", "message": "Invalid request."})
    





#comment
#@csrf_exempt  # only if you're handling this manually via AJAX

# class HomeView(TemplateView):
#     template_name = 'blog/home.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)

#         posts = Post.objects.filter(status='published').order_by('-created_at')
        
#         # Get the number of posts to show from the query string (default: 3)
#         posts_to_show = int(self.request.GET.get('show', 3))

#         # Limit the posts based on `posts_to_show`
#         context['posts'] = posts[:posts_to_show]
#         context['posts_to_show'] = posts_to_show
#         context['total_posts'] = posts.count()  # To check if more posts exist
#         return context
    
    
    

# class PostDetailView(DetailView):
#     template_name = 'blog/post_detail.html'
#     model = Post
#     context_object_name = 'post'
    
#     def get_object(self, queryset=None):
#         post = super().get_object(queryset)
#         post.views += 1
#         post.save(update_fields=['views'])
#         return post
    
    
    

class PostDetailView(LoginRequiredMixin, DetailView):
    template_name = 'blog/post_detail.html'
    model = Post
    context_object_name = 'post'
# for views
    def get_object(self, queryset=None):
        post = super().get_object(queryset)
        post.views += 1
        post.save(update_fields=['views'])
        return post
    
    def get_object(self, queryset=None):
        post = super().get_object(queryset)
        post.views += 1
        post.save(update_fields=['views'])
        # Clear the cache for the deleted post
        cache_key = f'post_detail_{post.id}'
        cache.delete(cache_key)
        return post
# for comments
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = self.object.comments.all().order_by('-created_at')
        return context

    @method_decorator(csrf_exempt)  # only needed if not using {% csrf_token %}
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()  # Get the post instance
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = self.object
                comment.save()
                return JsonResponse({"status": "success", "message": "Comment submitted!"})
            return JsonResponse({"status": "error", "message": "Invalid form data."})
        return JsonResponse({"status": "error", "message": "Invalid request."})
    
    
    
#All posts by a specific user

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  
    context_object_name = 'posts'
    
    paginate_by = 3

    def get_queryset(self):
        User = get_user_model()  # Get the actual custom User model
        user = get_object_or_404(User.objects.all(), username=self.kwargs.get('username'))
        return Post.objects.filter(author=user, status='published').order_by('-created_at')
    
    
    
    
    
# Likes

@login_required
def add_like(request, pk):
    if request.method != 'POST':
        raise Http404("Invalid request")
    post = get_object_or_404(Post, pk=pk)

    if request.user not in post.likes.all():
        post.likes.add(request.user)

    return redirect('post_detail', pk=pk)

    
    
# Remove likes
@login_required
def unlike(request, pk):
    if request.method != 'POST':
        raise Http404("Invalid request")
    post = get_object_or_404(Post, pk=pk)

    if request.user in post.likes.all():
        post.likes.remove(request.user)

    return redirect('post_detail', pk=pk)




#Share post

def generate_share_link(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    share_url = request.build_absolute_uri(
        reverse('post_detail', args=[str(post.id)])
    )
    return render(request, 'blog/share_link_output.html', {'share_url': share_url})




def videocall(request):
    return render(request, 'blog/videocall.html')