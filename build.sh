#!/usr/bin/env bash
# exit on error
set -o errexit

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir -p staticfiles
mkdir -p media/csv_files
mkdir -p media/event_images

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate

# Create default admin user
python manage.py create_default_user
