from django.urls import path
from .views import (HomeView,PostDetailView,UserPostListView)
from blog import views
from django.views.decorators.cache import cache_page
urlpatterns = [
    # path('', HomeView.as_view(), name='home'),
    path('', cache_page(60 * 15)(HomeView.as_view()), name='home'),
    # path('blog/', PostListView.as_view(), name='post_list'),
    path('blog/<int:pk>/', cache_page(60 * 15)(PostDetailView.as_view()), name='post_detail'),
    
   # path('user/<str:username>', UserPostListView.as_view(), name='user-posts'), # Post list view for a specific user
    path('user/<str:username>/', cache_page(60 * 15)(UserPostListView.as_view()), name='user-posts'), # Post list view for a specific user
    
    
    #likes
    path('post/<int:pk>/like/', views.add_like, name="add_like"),
    path('post/<int:pk>/unlike/', views.unlike, name="unlike"),
    path('blog/share/link/<int:post_id>/', views.generate_share_link, name='generate_share_link'),
    #video
    path('video/', views.videocall, name='video'),
   
]  
