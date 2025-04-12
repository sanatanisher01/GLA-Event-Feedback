import os
import dj_database_url
from .settings import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Update allowed hosts
ALLOWED_HOSTS = ['*']  # Update this with your Render domain when available

# Configure the database using environment variable provided by Render
DATABASE_URL = os.environ.get('DATABASE_URL')
DATABASES = {
    'default': dj_database_url.config(default=DATABASE_URL, conn_max_age=600)
}

# Static files configuration
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Add whitenoise middleware for static files
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

# Try to add Cloudinary to INSTALLED_APPS if available
try:
    import cloudinary
    import cloudinary.uploader
    import cloudinary_storage

    # Cloudinary is available, add it to INSTALLED_APPS
    INSTALLED_APPS += [
        'cloudinary',
        'cloudinary_storage',
    ]

    # Cloudinary configuration
    CLOUDINARY_STORAGE = {
        'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME', ''),
        'API_KEY': os.environ.get('CLOUDINARY_API_KEY', ''),
        'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET', ''),
    }

    # Check if credentials are set
    if all([CLOUDINARY_STORAGE['CLOUD_NAME'], CLOUDINARY_STORAGE['API_KEY'], CLOUDINARY_STORAGE['API_SECRET']]):
        # Media files configuration with Cloudinary
        DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
        MEDIA_URL = '/media/'
        print('INFO: Cloudinary configured successfully.')
    else:
        # Fallback to local storage if credentials are not set
        print('WARNING: Cloudinary credentials not set. Using local storage.')
        # Use local storage instead
        MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
        MEDIA_URL = '/media/'
        DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

        # Remove cloudinary from INSTALLED_APPS if credentials are not set
        INSTALLED_APPS.remove('cloudinary')
        INSTALLED_APPS.remove('cloudinary_storage')

except ImportError:
    # Cloudinary is not available, use local storage
    print('WARNING: Cloudinary package not installed. Using local storage.')
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    MEDIA_URL = '/media/'
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

# Security settings
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

# Secret key from environment variable
SECRET_KEY = os.environ.get('SECRET_KEY', SECRET_KEY)
