from django.contrib import admin
from .models import Image

# Register your models here.

class ImageCreateAdmin(admin.ModelAdmin):
    list_display=('title', 'slug', 'created', 'image')
    list_filter= ('created',)

admin.site.register(Image, ImageCreateAdmin)