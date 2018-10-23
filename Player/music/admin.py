from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Album)
admin.site.register(models.Song)

admin.site.site_header = 'Admin Page'
admin.site.site_title = 'Admin Page'
