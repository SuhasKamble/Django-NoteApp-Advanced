from django.db import models

# Create your models here.


class Note(models.Model):
    title = models.CharField(max_length=456)
    content = models.TextField()
    summary = models.CharField(max_length=678)
    slug = models.CharField(max_length=354)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.title[0:20]+"..."
