# Generated by Django 5.0.6 on 2024-06-23 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cloudberries', '0002_alter_category_options_post_summary'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]
