from django.db import models
from ckeditor.fields import RichTextField 
from cloudinary import CloudinaryImage

# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=200)
    description = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)  # <-- this must be here
    image = models.ImageField(upload_to='events_images/', default='https://res.cloudinary.com/dl21gihhj/image/upload/v1745158564/samples/landscapes/nature-mountains.jpg', blank=True, null=True,max_length=300)
    status = models.CharField(choices=[('published', 'Published'), ('draft', 'Draft')])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            cloudinary_image = CloudinaryImage(self.image.name)
            resized_url = cloudinary_image.build_url(width=300, height=300, crop="limit")
            
            
            # You can print or save this URL if you need it
            print("Resized image URL:", resized_url)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
