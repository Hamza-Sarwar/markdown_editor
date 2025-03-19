from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
    """Model for document tags"""
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name

class Document(models.Model):
    """Model for Markdown documents"""
    title = models.CharField(max_length=200)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    tags = models.ManyToManyField(Tag, blank=True, related_name='documents')
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-updated']