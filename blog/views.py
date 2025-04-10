from django.shortcuts import get_object_or_404, render
from django.views.generic import (TemplateView,ListView, DetailView)

from blog.models import Post
from src import settings
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
# Create your views here.


class HomeView(TemplateView):
    template_name = 'blog/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the published posts to the context
        context['posts'] = Post.objects.filter(status='published').order_by('-created_at')
        
        # Pagination
        paginator = Paginator('posts', 2)  # Show 3 posts per page
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Add paginated posts to context
        context['page_obj'] = page_obj
        return context
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
    
    
    

class PostDetailView(DetailView):
    template_name = 'blog/post_detail.html'
    model = Post
    context_object_name = 'post'
    
    
    
    
#All posts by a specific user

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  
    context_object_name = 'posts'

    def get_queryset(self):
        User = get_user_model()  # Get the actual custom User model
        user = get_object_or_404(User.objects.all(), username=self.kwargs.get('username'))
        return Post.objects.filter(author=user, status='published').order_by('-created_at')