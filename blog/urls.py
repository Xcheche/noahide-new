from django.urls import path
from .views import (HomeView,PostDetailView,UserPostListView)
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    # path('blog/', PostListView.as_view(), name='post_list'),
    path('blog/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'), # Post list view for a specific user
]  
