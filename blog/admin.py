from django.contrib import admin
from django.contrib import admin
from blog.models import Post, Comment, LikeDislike

# Register your models here.

admin.site.register(Post)
admin.site.register(LikeDislike)
@admin.register(Comment)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ["user", "blog"]