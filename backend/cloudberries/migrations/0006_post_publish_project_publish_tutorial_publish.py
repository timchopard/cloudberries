# Generated by Django 5.0.6 on 2024-06-30 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cloudberries', '0005_project_body_project_created_on_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='publish',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='project',
            name='publish',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='tutorial',
            name='publish',
            field=models.BooleanField(default=True),
        ),
    ]
