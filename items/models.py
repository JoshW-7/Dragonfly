from django.db import models
from django.utils import timezone
from taggit.managers import TaggableManager

from datetime import datetime


from users.models import UserProfile


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

