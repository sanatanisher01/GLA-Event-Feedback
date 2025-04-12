from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add_event/', views.add_event, name='add_event'),
    path('edit_event/<int:event_id>/', views.edit_event, name='edit_event'),
    path('dashboard/confirm-delete/<int:event_id>/', views.confirm_delete, name='confirm_delete'),
    path('delete_event/<int:event_id>/', views.delete_event, name='delete_event'),
    path('upload_csv/<int:event_id>/', views.upload_csv, name='upload_csv'),
    path('view_csv/<int:csv_id>/', views.view_csv, name='view_csv'),
    path('visualize/<int:csv_id>/', views.visualize_data, name='visualize_data'),
    path('download_csv/<int:csv_id>/', views.download_csv, name='download_csv'),
]
