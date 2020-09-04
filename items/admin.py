from django.contrib import admin

from .models import Item, ItemRelation, File, Comment


admin.site.register(Item)
admin.site.register(ItemRelation)
admin.site.register(File)
admin.site.register(Comment)