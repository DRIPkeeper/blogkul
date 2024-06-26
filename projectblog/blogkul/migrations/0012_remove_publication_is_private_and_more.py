# Generated by Django 5.0.6 on 2024-06-07 15:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogkul', '0011_remove_publication_author_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='publication',
            name='is_private',
        ),
        migrations.RemoveField(
            model_name='publication',
            name='password',
        ),
        migrations.AddField(
            model_name='publication',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
