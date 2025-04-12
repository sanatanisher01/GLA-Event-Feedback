from django.db import models
from django.utils import timezone
import os
from cloudinary.models import CloudinaryField

# Create your models here.

def event_image_path(instance, filename):
    # File will be uploaded to MEDIA_ROOT/event_images/<event_id>/<filename>
    return f'event_images/event_{instance.id}/{filename}'

class Event(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField()
    venue = models.CharField(max_length=200)
    highlights = models.TextField()
    form_link = models.URLField()
    # Use CloudinaryField for images in production, fallback to ImageField in development
    try:
        image = CloudinaryField('image', folder='event_images', blank=True, null=True,
                             transformation={'quality': 'auto:good', 'fetch_format': 'auto'},
                             format='jpg')
    except Exception as e:
        print(f"CloudinaryField error: {str(e)}")
        # Fallback to standard ImageField if Cloudinary is not configured
        image = models.ImageField(upload_to=event_image_path, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

def csv_file_path(instance, filename):
    # File will be uploaded to MEDIA_ROOT/csv_files/event_<id>/<filename>
    return f'csv_files/event_{instance.event.id}/{filename}'

class CSVFile(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='csv_files')
    # Use CloudinaryField for files in production, fallback to FileField in development
    try:
        file = CloudinaryField('raw', folder='csv_files', resource_type='raw', blank=False, null=False)
    except Exception as e:
        print(f"CloudinaryField error: {str(e)}")
        # Fallback to standard FileField if Cloudinary is not configured
        file = models.FileField(upload_to=csv_file_path)
    upload_date = models.DateTimeField(default=timezone.now)
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.event.name} - {os.path.basename(self.file.name)}"

    def filename(self):
        return os.path.basename(self.file.name)
