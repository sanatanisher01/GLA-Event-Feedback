from django.db import models
from django.utils import timezone
import os

# Try to import CloudinaryField, but provide a fallback if it fails
try:
    from cloudinary.models import CloudinaryField
    CLOUDINARY_AVAILABLE = True
except ImportError:
    # Create a dummy CloudinaryField that just uses ImageField
    CLOUDINARY_AVAILABLE = False
    class CloudinaryField(models.ImageField):
        def __init__(self, *args, **kwargs):
            # Remove Cloudinary-specific arguments
            for key in ['folder', 'transformation', 'format', 'resource_type']:
                if key in kwargs:
                    del kwargs[key]
            super().__init__(*args, **kwargs)

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
    if CLOUDINARY_AVAILABLE:
        image = CloudinaryField('image', folder='event_images', blank=True, null=True,
                             transformation={'quality': 'auto:good', 'fetch_format': 'auto'},
                             format='jpg')
    else:
        # Fallback to standard ImageField if Cloudinary is not available
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
    if CLOUDINARY_AVAILABLE:
        file = CloudinaryField('raw', folder='csv_files', resource_type='raw', blank=False, null=False)
    else:
        # Fallback to standard FileField if Cloudinary is not available
        file = models.FileField(upload_to=csv_file_path)
    upload_date = models.DateTimeField(default=timezone.now)
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.event.name} - {self.get_filename()}"

    def get_filename(self):
        # Handle both Cloudinary and regular file fields
        if hasattr(self.file, 'name'):
            # Regular file field
            return os.path.basename(self.file.name)
        elif hasattr(self.file, 'public_id'):
            # Cloudinary resource
            # Extract filename from the public_id (which is usually path/filename)
            return os.path.basename(self.file.public_id)
        else:
            # Fallback
            return f"file-{self.id}"

    def filename(self):
        # For backward compatibility
        return self.get_filename()
