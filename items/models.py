from django.db import models
from django.utils import timezone
from django.conf import settings
from django.dispatch import receiver

from taggit.managers import TaggableManager

from datetime import datetime

from users.models import UserProfile
from projects.models import Project

import os


class Item(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(null=True)
    user = models.ForeignKey(UserProfile, on_delete=models.PROTECT)
    assigned = models.ForeignKey(UserProfile, null=True, on_delete=models.PROTECT, related_name="assigned_user")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    priority = models.CharField(max_length=20, default="none")
    resolved = models.BooleanField(default=False)
    tags = TaggableManager(blank=True)
    project = models.ForeignKey(Project, null=True, on_delete=models.PROTECT)

    def __str__(self):
        return f"<Item: {self.title}>"

    def save(self, *args, **kwargs):
        update_time = kwargs.pop("update_time", None)
        if update_time != False:
            self.date_updated = datetime.now(tz=timezone.utc)
        
        super(Item, self).save(*args, **kwargs)

    def column_values(self):
        return ["Title", "Assigned", "Updated"]

    def row_values(self):
        date_updated = self.date_updated
        return [self.title, self.assigned.display_name, f"{date_updated.strftime('%B')} {date_updated.day} {date_updated.year}"]


class File(models.Model):
    file = models.FileField(upload_to="items/files/")
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.file.name.split("/")[-1]

    def get_link(self):
        return settings.MEDIA_URL + self.__str__()

@receiver(models.signals.post_delete, sender=File)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.file:
        filepath = "/".join(instance.file.url.split("/")[-2:])
        if os.path.isfile(filepath):
            os.remove(filepath)


class Comment(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(UserProfile, on_delete=models.PROTECT)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    body = models.TextField()

    def __str__(self):
        return f"<Comment: {self.item}>"

