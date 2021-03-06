# Generated by Django 2.1.4 on 2019-01-06 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_faculty_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='faculty_profile',
            name='first_name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='faculty_profile',
            name='last_name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='student_profile',
            name='first_name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='student_profile',
            name='last_name',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
