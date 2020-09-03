# Generated by Django 3.1.1 on 2020-09-02 17:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20200902_0838'),
        ('items', '0004_item_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='assigned',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='assigned_user', to='users.userprofile'),
        ),
    ]