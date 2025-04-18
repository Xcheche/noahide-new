from django.contrib import admin
from .models import Post, Comment,Tag,Subscriber
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at',)
    search_fields = ('title', 'content')
    list_filter = ('created_at', 'updated_at')
    
    
    ordering = ('-created_at',)
    
    
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'name', 'created_at')
    search_fields = ('content',)
    list_filter = ('created_at',)
    
    ordering = ('-created_at',)    
    
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    
    ordering = ('name',)
    
    
    
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email',)
    search_fields = ('email',)
    
    ordering = ('email',)
    list_filter = ('email',)    
# Register your models here.

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Tag, TagAdmin)   
admin.site.register(Subscriber, SubscriberAdmin) 