# Generated by Django 2.1.5 on 2019-01-18 08:08

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0018_auto_20190117_1357'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='dislikes_comment',
            field=models.ManyToManyField(related_name='dislikes_comment', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='likes_comment',
            field=models.ManyToManyField(related_name='likes_comment', to=settings.AUTH_USER_MODEL),
        ),
    ]
