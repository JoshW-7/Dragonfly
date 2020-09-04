from django.contrib import admin

from .models import Item, File, Comment


admin.site.register(Item)
admin.site.register(File)
admin.site.register(Comment)