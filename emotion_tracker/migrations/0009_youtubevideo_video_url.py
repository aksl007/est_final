# Generated by Django 3.2.25 on 2024-12-23 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emotion_tracker', '0008_alter_framedetection_frame_filename'),
    ]

    operations = [
        migrations.AddField(
            model_name='youtubevideo',
            name='video_url',
            field=models.URLField(default=1),
            preserve_default=False,
        ),
    ]
