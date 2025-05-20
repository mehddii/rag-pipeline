from django.db import models
from django.db import models
from django.utils import timezone

class ChunkingStrategy(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    parameters = models.JSONField(default=dict)

    def __str__(self):
        return self.name

class AIModel(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    provider = models.CharField(max_length=50, blank=True)
    api_key_required = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Document(models.Model):
    content = models.TextField()
    metadata = models.JSONField(default=dict)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    chunking_strategie = models.ForeignKey(ChunkingStrategy, on_delete=models.SET_NULL, null=True, blank=True)
    ai_model = models.ForeignKey(AIModel, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Document uploaded at {self.uploaded_at.strftime('%Y-%m-%d %H:%M')}"