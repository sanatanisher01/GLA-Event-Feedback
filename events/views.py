import os
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from .models import Event, CSVFile
from .forms import CustomAuthenticationForm, EventForm, CSVUploadForm

# Create your views here.

def index(request):
    events = Event.objects.all().order_by('-date')
    return render(request, 'events/index.html', {'events': events})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and username == 'Ankurrai@gla':
                login(request, user)
                messages.success(request, f'Welcome, {username}!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'events/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('index')

@login_required
def dashboard(request):
    try:
        # Get all events ordered by date (newest first)
        events = Event.objects.all().order_by('-date')

        # Get all CSV files
        csv_files = CSVFile.objects.all().select_related('event')

        # Count statistics
        csv_count = csv_files.count()
        visualization_count = csv_count  # Each CSV can be visualized

        # Render the enhanced dashboard template
        return render(request, 'events/dashboard_enhanced.html', {
            'events': events,
            'csv_files': csv_files,
            'csv_count': csv_count,
            'visualization_count': visualization_count
        })
    except Exception as e:
        # Log the error
        import traceback
        print(f"Dashboard error: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        print("Traceback:")
        traceback.print_exc()

        # Show error message
        messages.error(request, f"An error occurred while loading the dashboard. Please try again or contact support.")
        return redirect('index')

@login_required
def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                event = form.save(commit=False)
                # Handle image upload separately to catch Cloudinary errors
                if 'image' in request.FILES:
                    event.image = request.FILES['image']
                event.save()
                messages.success(request, 'Event added successfully!')
                return redirect('dashboard')
            except Exception as e:
                print(f"Event creation error: {str(e)}")
                messages.error(request, f"Error saving event: {str(e)}")
    else:
        form = EventForm()
    return render(request, 'events/add_event.html', {'form': form, 'action': 'Add'})

@login_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            try:
                updated_event = form.save(commit=False)
                # Handle image upload separately to catch Cloudinary errors
                if 'image' in request.FILES:
                    updated_event.image = request.FILES['image']
                updated_event.save()
                messages.success(request, 'Event updated successfully!')
                return redirect('dashboard')
            except Exception as e:
                print(f"Event update error: {str(e)}")
                messages.error(request, f"Error updating event: {str(e)}")
    else:
        form = EventForm(instance=event)
    return render(request, 'events/add_event.html', {'form': form, 'event': event, 'action': 'Edit'})

@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    # Handle both GET and POST for simplicity in emergency mode
    event_name = event.name
    try:
        event.delete()
        messages.success(request, f'Event "{event_name}" deleted successfully!')
    except Exception as e:
        messages.error(request, f'Error deleting event: {str(e)}')
    return redirect('dashboard')

@login_required
def upload_csv(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                csv_file = form.save(commit=False)
                csv_file.event = event
                # Handle file upload separately to catch Cloudinary errors
                if 'file' in request.FILES:
                    csv_file.file = request.FILES['file']
                csv_file.save()
                messages.success(request, 'CSV file uploaded successfully!')
                return redirect('dashboard')
            except Exception as e:
                print(f"CSV upload error: {str(e)}")
                messages.error(request, f"Error uploading CSV: {str(e)}")
    else:
        form = CSVUploadForm()
    return render(request, 'events/upload_csv.html', {'form': form, 'event': event})

@login_required
def view_csv(request, csv_id):
    csv_file = get_object_or_404(CSVFile, id=csv_id)
    data = []
    headers = []

    try:
        # Handle both local files and Cloudinary URLs
        if hasattr(csv_file.file, 'url'):
            # For Cloudinary files
            import requests
            response = requests.get(csv_file.file.url)
            content = response.content.decode('utf-8')
            df = pd.read_csv(io.StringIO(content))
        else:
            # For local files
            df = pd.read_csv(csv_file.file.path)

        headers = df.columns.tolist()
        data = df.values.tolist()
    except Exception as e:
        messages.error(request, f'Error reading CSV file: {str(e)}')

    return render(request, 'events/view_csv.html', {
        'csv_file': csv_file,
        'headers': headers,
        'data': data,
    })

@login_required
def download_csv(request, csv_id):
    csv_file = get_object_or_404(CSVFile, id=csv_id)

    # Handle both local files and Cloudinary URLs
    if hasattr(csv_file.file, 'url'):
        # For Cloudinary files
        import requests
        response = requests.get(csv_file.file.url)
        content = response.content
        http_response = HttpResponse(content, content_type='text/csv')
    else:
        # For local files
        with open(csv_file.file.path, 'rb') as f:
            http_response = HttpResponse(f.read(), content_type='text/csv')

    http_response['Content-Disposition'] = f'attachment; filename="{csv_file.filename()}"'
    return http_response

@login_required
def visualize_data(request, csv_id):
    csv_file = get_object_or_404(CSVFile, id=csv_id)
    charts = []
    chart_type = request.GET.get('chart_type', 'all')

    try:
        # Handle both local files and Cloudinary URLs
        if hasattr(csv_file.file, 'url'):
            # For Cloudinary files
            import requests
            response = requests.get(csv_file.file.url)
            content = response.content.decode('utf-8')
            df = pd.read_csv(io.StringIO(content))
        else:
            # For local files
            df = pd.read_csv(csv_file.file.path)

        # Generate charts for numeric columns
        numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
        categorical_columns = df.select_dtypes(include=['object']).columns.tolist()
        date_columns = []

        # Try to identify date columns
        for col in df.columns:
            if df[col].dtype == 'object':
                try:
                    pd.to_datetime(df[col])
                    date_columns.append(col)
                except:
                    pass

        # Remove identified date columns from categorical columns
        categorical_columns = [col for col in categorical_columns if col not in date_columns]

        # Bar charts for categorical data
        if chart_type in ['all', 'bar']:
            for col in categorical_columns[:3]:  # Limit to first 3 categorical columns
                if len(df[col].unique()) <= 15:  # Only if there are 15 or fewer unique values
                    plt.figure(figsize=(10, 6))
                    ax = df[col].value_counts().plot(kind='bar', color='#4361ee')
                    plt.title(f'Distribution of {col}')
                    plt.xlabel(col)
                    plt.ylabel('Count')

                    # Add value labels on top of bars
                    for i, v in enumerate(df[col].value_counts()):
                        ax.text(i, v + 0.1, str(v), ha='center')

                    plt.tight_layout()

                    buffer = io.BytesIO()
                    plt.savefig(buffer, format='png')
                    buffer.seek(0)
                    image_png = buffer.getvalue()
                    buffer.close()
                    plt.close()

                    chart = base64.b64encode(image_png).decode('utf-8')
                    charts.append({
                        'title': f'Bar Chart: Distribution of {col}',
                        'type': 'bar',
                        'image': chart
                    })

        # Pie charts for categorical data with few unique values
        if chart_type in ['all', 'pie']:
            for col in categorical_columns[:3]:  # Limit to first 3 categorical columns
                if 2 <= len(df[col].unique()) <= 8:  # Only if there are 2-8 unique values
                    plt.figure(figsize=(9, 7))
                    df[col].value_counts().plot(kind='pie', autopct='%1.1f%%',
                                              colors=plt.cm.Paired(range(len(df[col].unique()))))
                    plt.title(f'Distribution of {col}')
                    plt.ylabel('')
                    plt.legend(df[col].value_counts().index, loc='best')
                    plt.tight_layout()

                    buffer = io.BytesIO()
                    plt.savefig(buffer, format='png')
                    buffer.seek(0)
                    image_png = buffer.getvalue()
                    buffer.close()
                    plt.close()

                    chart = base64.b64encode(image_png).decode('utf-8')
                    charts.append({
                        'title': f'Pie Chart: Distribution of {col}',
                        'type': 'pie',
                        'image': chart
                    })

        # Histograms for numeric data
        if chart_type in ['all', 'histogram']:
            for col in numeric_columns[:3]:  # Limit to first 3 numeric columns
                plt.figure(figsize=(10, 6))
                df[col].plot(kind='hist', bins=15, color='#38b000', edgecolor='black', alpha=0.7)
                plt.axvline(df[col].mean(), color='red', linestyle='dashed', linewidth=1, label=f'Mean: {df[col].mean():.2f}')
                plt.axvline(df[col].median(), color='blue', linestyle='dashed', linewidth=1, label=f'Median: {df[col].median():.2f}')
                plt.title(f'Histogram of {col}')
                plt.xlabel(col)
                plt.ylabel('Frequency')
                plt.legend()
                plt.tight_layout()

                buffer = io.BytesIO()
                plt.savefig(buffer, format='png')
                buffer.seek(0)
                image_png = buffer.getvalue()
                buffer.close()
                plt.close()

                chart = base64.b64encode(image_png).decode('utf-8')
                charts.append({
                    'title': f'Histogram: Distribution of {col}',
                    'type': 'histogram',
                    'image': chart
                })

        # Box plots for numeric data
        if chart_type in ['all', 'box']:
            for col in numeric_columns[:3]:  # Limit to first 3 numeric columns
                plt.figure(figsize=(10, 6))
                df.boxplot(column=[col])
                plt.title(f'Box Plot of {col}')
                plt.ylabel(col)
                plt.grid(False)
                plt.tight_layout()

                buffer = io.BytesIO()
                plt.savefig(buffer, format='png')
                buffer.seek(0)
                image_png = buffer.getvalue()
                buffer.close()
                plt.close()

                chart = base64.b64encode(image_png).decode('utf-8')
                charts.append({
                    'title': f'Box Plot: Distribution of {col}',
                    'type': 'box',
                    'image': chart
                })

        # Scatter plots for pairs of numeric columns
        if chart_type in ['all', 'scatter'] and len(numeric_columns) >= 2:
            for i in range(min(2, len(numeric_columns))):
                for j in range(i+1, min(3, len(numeric_columns))):
                    col1, col2 = numeric_columns[i], numeric_columns[j]
                    plt.figure(figsize=(10, 6))
                    plt.scatter(df[col1], df[col2], alpha=0.5, color='#4361ee')
                    plt.title(f'Scatter Plot: {col1} vs {col2}')
                    plt.xlabel(col1)
                    plt.ylabel(col2)

                    # Add trend line
                    if len(df) > 1:  # Need at least 2 points for a line
                        z = np.polyfit(df[col1], df[col2], 1)
                        p = np.poly1d(z)
                        plt.plot(df[col1], p(df[col1]), "r--", alpha=0.8,
                                label=f'Trend: y={z[0]:.2f}x+{z[1]:.2f}')
                        plt.legend()

                    plt.tight_layout()

                    buffer = io.BytesIO()
                    plt.savefig(buffer, format='png')
                    buffer.seek(0)
                    image_png = buffer.getvalue()
                    buffer.close()
                    plt.close()

                    chart = base64.b64encode(image_png).decode('utf-8')
                    charts.append({
                        'title': f'Scatter Plot: {col1} vs {col2}',
                        'type': 'scatter',
                        'image': chart
                    })

        # Line charts for time series data if date columns exist
        if chart_type in ['all', 'line'] and date_columns and numeric_columns:
            for date_col in date_columns[:1]:  # Use first date column
                for num_col in numeric_columns[:2]:  # Use first 2 numeric columns
                    try:
                        # Convert to datetime and sort
                        temp_df = df[[date_col, num_col]].copy()
                        temp_df[date_col] = pd.to_datetime(temp_df[date_col])
                        temp_df = temp_df.sort_values(by=date_col)

                        plt.figure(figsize=(12, 6))
                        plt.plot(temp_df[date_col], temp_df[num_col], marker='o', linestyle='-', color='#4361ee')
                        plt.title(f'Time Series: {num_col} over {date_col}')
                        plt.xlabel(date_col)
                        plt.ylabel(num_col)
                        plt.xticks(rotation=45)
                        plt.grid(True, alpha=0.3)
                        plt.tight_layout()

                        buffer = io.BytesIO()
                        plt.savefig(buffer, format='png')
                        buffer.seek(0)
                        image_png = buffer.getvalue()
                        buffer.close()
                        plt.close()

                        chart = base64.b64encode(image_png).decode('utf-8')
                        charts.append({
                            'title': f'Line Chart: {num_col} over Time',
                            'type': 'line',
                            'image': chart
                        })
                    except Exception as e:
                        # Skip this chart if there's an error
                        pass

        # Heatmap for correlation between numeric columns
        if chart_type in ['all', 'heatmap'] and len(numeric_columns) >= 2:
            plt.figure(figsize=(10, 8))
            corr = df[numeric_columns].corr()
            sns.heatmap(corr, annot=True, cmap='coolwarm', linewidths=0.5, fmt='.2f')
            plt.title('Correlation Heatmap')
            plt.tight_layout()

            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            image_png = buffer.getvalue()
            buffer.close()
            plt.close()

            chart = base64.b64encode(image_png).decode('utf-8')
            charts.append({
                'title': 'Correlation Heatmap',
                'type': 'heatmap',
                'image': chart
            })

    except Exception as e:
        messages.error(request, f'Error generating visualizations: {str(e)}')

    # Get available chart types based on data
    available_chart_types = [
        {'id': 'all', 'name': 'All Charts'},
        {'id': 'bar', 'name': 'Bar Charts'},
        {'id': 'pie', 'name': 'Pie Charts'},
        {'id': 'histogram', 'name': 'Histograms'},
        {'id': 'box', 'name': 'Box Plots'}
    ]

    if len(numeric_columns) >= 2:
        available_chart_types.append({'id': 'scatter', 'name': 'Scatter Plots'})
        available_chart_types.append({'id': 'heatmap', 'name': 'Correlation Heatmap'})

    if date_columns and numeric_columns:
        available_chart_types.append({'id': 'line', 'name': 'Line Charts'})

    return render(request, 'events/visualize_data.html', {
        'csv_file': csv_file,
        'charts': charts,
        'current_chart_type': chart_type,
        'available_chart_types': available_chart_types
    })
