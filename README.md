# College Event Feedback System

A secure full-stack web application for college event feedback using Django. The app has a professional and modern UI/UX design with light and dark mode support.

## Features

### Landing Page (Public)
- Show list of events with event name, date, venue, and highlights
- Each event has a button linking to the Google Form

### Manager Dashboard (Login Protected)
- Secure login system (username: Ankurrai@gla, password: AnkurRai@010GLA)
- Add new events (event name, date, venue, highlights, Google Form link)
- Upload CSV file (exported from Google Form) linked to that event
- View uploaded CSVs (preview in table)
- Download CSV
- Automatically generate visual graphs (bar, pie, line, scatter, box plots, heatmaps) from CSV feedback

## Deployment Instructions for PythonAnywhere

### 1. Create a PythonAnywhere Account
- Go to [PythonAnywhere](https://www.pythonanywhere.com/) and sign up for a free account

### 2. Upload Your Code
- From the Dashboard, go to the "Files" tab
- Create a new directory for your project: `mkdir feedback_system`
- Upload your project files using the "Upload a file" button or via Git

### 3. Set Up a Virtual Environment
```bash
# Create a virtual environment
mkvirtualenv --python=python3.9 feedback_env

# Activate the virtual environment
workon feedback_env

# Install dependencies
pip install -r requirements.txt
```

### 4. Configure MySQL Database
- Go to the "Databases" tab
- Create a new MySQL database
- Update the database settings in `feedback_system/production_settings.py`

### 5. Configure WSGI File
- Go to the "Web" tab
- Click "Add a new web app"
- Select "Manual configuration" and "Python 3.9"
- Set the path to your WSGI file: `/home/yourusername/feedback_system/wsgi_pythonanywhere.py`
- Edit the WSGI file to match your project path

### 6. Configure Static Files
- In the "Web" tab, under "Static files"
- Add:
  - URL: `/static/`
  - Directory: `/home/yourusername/feedback_system/staticfiles/`
- Add:
  - URL: `/media/`
  - Directory: `/home/yourusername/feedback_system/media/`

### 7. Collect Static Files and Migrate Database
```bash
python manage.py collectstatic --settings=feedback_system.production_settings
python manage.py migrate --settings=feedback_system.production_settings
```

### 8. Create Superuser (if needed)
```bash
python manage.py createsuperuser --settings=feedback_system.production_settings
```

### 9. Reload Web App
- Click the "Reload" button in the "Web" tab

Your application should now be live at `yourusername.pythonanywhere.com`
