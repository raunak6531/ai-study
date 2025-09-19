from django.contrib import admin
from .models import Document

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'file_type', 'file_size', 'uploaded_at')
    list_filter = ('file_type', 'uploaded_at')
    search_fields = ('file_name',)
