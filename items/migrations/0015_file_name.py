# Generated by Django 3.1.1 on 2020-09-04 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0014_remove_file_upload_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]