from django.db import models
from django.shortcuts import render
from django.urls import reverse
from ckeditor.fields import RichTextField
from src import settings
from django.core.exceptions import ValidationError
from cloudinary import CloudinaryImage
from cloudinary.models import CloudinaryField
import random


# Create your models here.
# This is a custom manager for the BlogPost model
class PostManager(models.Manager):
    def published(self): # This method returns all published posts
        # It filters the posts based on the status field
        return self.filter(status="published")

    def drafts(self): # This method returns all draft posts
        # It filters the posts based on the status field
        return self.filter(status="draft")
    
    


def get_random_blog_image():
    images = [
        "https://images.unsplash.com/photo-1581091870622-1a3c6f8d3e0e",
        "https://picsum.photos/seed/picsum/300/300",
        "https://placekitten.com/300/300",
        "https://placebear.com/300/300",
    ]
    return random.choice(images)
# Post model
class Post(models.Model): # This is the main model for the blog post
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("published", "Published"),
    ]

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
   
    title = models.CharField(max_length=200, blank=False,help_text="Enter the title of the post")
    content =  RichTextField(blank=False) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")
    
    
    
    image = CloudinaryField(
        "blog",
        folder="blog_images/",
        default=get_random_blog_image,
        transformation={"width": 300, "height": 300, "crop": "fill"}
    )
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            cloudinary_image = CloudinaryImage(self.image.name)
            resized_url = cloudinary_image.build_url(width=800, height=600, crop="limit")
            
            
            # You can print or save this URL if you need it
            print("Resized image URL:", resized_url)

    tags = models.ManyToManyField('Tag',  blank=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_posts', blank=True)
    views = models.PositiveIntegerField(default=0)
    
    
    objects = PostManager()  # Custom Manager

    def __str__(self):
        return self.title
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'
        
        # Absolute URL for the post detail view
        # This method is used to generate the URL for the post detail view
    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


        
# Comment model  

BAD_WORDS = [
    'fool', 'fuck you', 'idiot', 'nonsense', 'stupid', 'bad', 'fake', 'rubbish', 'monkey', 'animal'
]

def validate_no_bad_words(content):
    if any(word in content.lower() for word in BAD_WORDS):
        raise ValidationError("Your comment contains inappropriate language.")

      
class Comment(models.Model):
    name = models.CharField(max_length=100)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    content =  models.TextField(validators=[validate_no_bad_words]) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment on {self.post.title}'
    
    
#Tag model    
class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    posts = models.ManyToManyField('Post', related_name='tags_in_post', blank=True)

    def __str__(self):
        return self.name    
    
    
    
class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    

    def __str__(self):
        return self.email
    class Meta:
        verbose_name = 'Subscriber'
        verbose_name_plural = 'Subscribers'    