from django.db import models
from ckeditor.fields import RichTextField 
from cloudinary import CloudinaryImage
from cloudinary.models import CloudinaryField
# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=200)
    description = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)  # <-- this must be here
    event_image = CloudinaryField(
        "event_image",
        folder="event_images/",
        blank=True,
        null=True,
        # This is the transformation for the image
        transformation={"width": 300, "height": 300, "crop": "fill"}
    )
    status = models.CharField(choices=[('published', 'Published'), ('draft', 'Draft')])

    def save(self, *args, **kwargs):
     super().save(*args, **kwargs)
     if self.event_image:
        try:
            cloudinary_image = CloudinaryImage(self.event_image.public_id)
            resized_url = cloudinary_image.build_url(width=500, height=400, crop="limit")
            print("Resized image URL:", resized_url)
        except AttributeError:
            print("Image does not have a valid Cloudinary public_id.")
            # You can print or save this URL if you need it
          

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
