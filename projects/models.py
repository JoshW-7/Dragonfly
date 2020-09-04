from django.db import models
from django.utils import timezone
from taggit.managers import TaggableManager

from datetime import datetime


from users.models import UserProfile


class Project(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(null=True)
    user = models.ForeignKey(UserProfile, on_delete=models.PROTECT)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"<Project: {self.title}>"

    def save(self, *args, **kwargs):
        update_time = kwargs.pop("update_time", None)
        if update_time != False:
            self.date_updated = datetime.now(tz=timezone.utc)
        
        super(Project, self).save(*args, **kwargs)