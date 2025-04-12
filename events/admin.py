from django.contrib import admin
from .models import Event, CSVFile

# Register your models here.

class CSVFileInline(admin.TabularInline):
    model = CSVFile
    extra = 0

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'venue', 'created_at')
    search_fields = ('name', 'venue')
    list_filter = ('date',)
    inlines = [CSVFileInline]

@admin.register(CSVFile)
class CSVFileAdmin(admin.ModelAdmin):
    list_display = ('event', 'filename', 'upload_date', 'description')
    list_filter = ('event', 'upload_date')
    search_fields = ('event__name', 'description')
