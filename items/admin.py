from django.contrib import admin

from .models import Item, File


admin.site.register(Item)
admin.site.register(File)