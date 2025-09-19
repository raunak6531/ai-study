from django.db import models
from django.utils import timezone

# Create your models here.

class Document(models.Model):
    file = models.FileField(upload_to='')
    uploaded_at = models.DateTimeField(default=timezone.now)
    file_name = models.CharField(max_length=255)
    file_size = models.IntegerField()  # Size in bytes
    file_type = models.CharField(max_length=10)  # pdf, ppt, pptx

    def __str__(self):
        return self.file_name

    class Meta:
        ordering = ['-uploaded_at']
