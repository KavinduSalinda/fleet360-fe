from django.db import models
from django.contrib.auth.models import User


class Document(models.Model):
    file_name = models.CharField(max_length=255)
    file_hash = models.CharField(max_length=500)
    file_url = models.URLField(blank=True, null=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.file_name
    
    class Meta:
        db_table = 'documents'
