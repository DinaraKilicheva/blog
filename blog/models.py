import datetime

from django.db import models
from django.utils.text import slugify
import users


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    slug = models.SlugField(unique=True)
    author = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="blogPosts")
    category = models.ForeignKey("common.Category", on_delete=models.CASCADE, related_name="blogPosts")
    image = models.ImageField(upload_to='images', null=True, blank=True)
    views = models.BigIntegerField(default=0, blank=True)
    published_at = datetime.datetime.now().strftime("%H:%M / %d.%m.%Y")
    
    
    
    
    @property
    def likes(self):
        return self.like_dislikes.filter(type=LikeDislike.LikeDislikeTypes.LIKE).count()
    
    @property
    def dislikes(self):
        return self.like_dislikes.filter(type=LikeDislike.LikeDislikeTypes.DISLIKE).count()
    
    def save(self, *args, **kwargs):
        if self.title.upper():
            self.slug = slugify(self.title.lower())
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return str(self.title)


class Comment(models.Model):
    blog = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    parent = models.ForeignKey("self", models.CASCADE, related_name="replies", null=True, blank=True)


class LikeDislike(models.Model):
    class LikeDislikeTypes(models.IntegerChoices):
        LIKE = 1
        DISLIKE = -1
    
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="like_dislikes")
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="like_dislikes")
    type = models.SmallIntegerField(choices=LikeDislikeTypes.choices)
    
    class Meta:
        unique_together = ["post", "user"]
    
    def __str__(self):
        return f"{self.user}"
