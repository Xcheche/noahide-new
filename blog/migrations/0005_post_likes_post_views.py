# Generated by Django 5.1.7 on 2025-04-18 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_subscriber_alter_post_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='likes',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='post',
            name='views',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
