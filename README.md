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

## Deployment Instructions for Render

### 1. Create a Render Account
- Go to [Render](https://render.com/) and sign up for a free account
- Connect your GitHub account to Render

### 2. Create a PostgreSQL Database
- In the Render dashboard, click on "New" and select "PostgreSQL"
- Give your database a name (e.g., `feedback-system-db`)
- Choose the free plan
- Click "Create Database"
- Note the Internal Database URL - you'll need this for your web service

### 3. Create a Web Service
- In the Render dashboard, click on "New" and select "Web Service"
- Connect your GitHub repository
- Give your service a name (e.g., `gla-event-feedback`)
- Set the Environment to "Python 3"
- Set the Build Command to `./build.sh`
- Set the Start Command to `gunicorn feedback_system.wsgi:application`

### 4. Configure Environment Variables
- In the web service settings, go to the "Environment" tab
- Add the following environment variables:
  - `DATABASE_URL`: Your Internal Database URL from step 2
  - `SECRET_KEY`: A secure random string for Django
  - `DJANGO_SETTINGS_MODULE`: `feedback_system.render_settings`
  - `PYTHON_VERSION`: `3.9.0` (or your preferred version)

### 5. Deploy Your Service
- Click "Create Web Service"
- Render will automatically build and deploy your application
- The build process will:
  - Install dependencies
  - Collect static files
  - Run database migrations

### 6. Create Default Admin User (Optional)
- After deployment, go to the "Shell" tab in your web service
- Run the following command to create the default admin user:
```bash
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('Ankurrai@gla', 'admin@example.com', 'AnkurRai@010GLA')"
```

### 7. Access Your Application
- Your application will be available at `https://your-service-name.onrender.com`
- You can set up a custom domain in the "Settings" tab if needed

### 8. Monitoring and Logs
- Render provides logs and metrics for your application
- You can view them in the "Logs" tab of your web service
