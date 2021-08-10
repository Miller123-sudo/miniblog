from django.contrib import admin
from blog.models import Image, Post

# Register your models here.


@admin.register(Post)
class PostModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'desc']


@admin.register(Image)
class ImageModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'photo']
