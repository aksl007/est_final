# Generated by Django 3.2.25 on 2024-12-23 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emotion_tracker', '0004_alter_framedetection_frame_filename'),
    ]

    operations = [
        migrations.AlterField(
            model_name='framedetection',
            name='frame_filename',
            field=models.FileField(upload_to='media/'),
        ),
    ]
