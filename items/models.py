from django.db import models
from taggit.managers import TaggableManager

from users.models import UserProfile


class Item(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(null=True)
    user = models.ForeignKey(UserProfile, on_delete=models.PROTECT)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    tags = TaggableManager()

    def __str__(self):
        return f"<Item: {self.title}>"

    def column_values(self):
        return ["Title", "User", "Updated"]

    def row_values(self):
        return [self.title, self.user, self.date_updated]

