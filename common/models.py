from django.db import models
from django.utils.text import slugify



class Category(models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(blank=True)
    
    def __str__(self):
        return str(self.title)
    
    def save(self, *args, **kwargs):
        if self.title.upper():
            self.slug = slugify(self.title.lower())
        return super().save(*args, **kwargs)
