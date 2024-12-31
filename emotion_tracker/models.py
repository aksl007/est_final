import os
from django.db import models
from django.conf import settings

class YouTubeVideo(models.Model):
    video_id = models.CharField(max_length=50, unique=True)
    video_url = models.URLField()
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField()
    thumbnail_url = models.URLField()
    channel_url = models.URLField()
    duration = models.IntegerField(default=0)

    happy = models.IntegerField(default=0)
    anger = models.IntegerField(default=0)
    sadness = models.IntegerField(default=0)
    panic = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    actions = ['delete_selected']  # 여러 항목을 한 번에 삭제하는 기능 활성화

    def __str__(self):
        return f'{self.title} / {self.author} / {self.description}'
    def delete(self, *args, **kwargs):
        # 관련된 모든 FrameDetection 객체의 파일 삭제
        for frame_detection in self.framedetection_set.all():
            if frame_detection.frame_filename:
                if os.path.isfile(frame_detection.frame_filename.path):
                    os.remove(frame_detection.frame_filename.path)
        # YouTubeVideo 객체 삭제
        super().delete(*args, **kwargs)


class FrameDetection(models.Model):
    video = models.ForeignKey(YouTubeVideo, on_delete=models.CASCADE)
    frame_number = models.IntegerField()
    confidence = models.FloatField(null=True, blank=True)
    detection_class = models.IntegerField(null=True, blank=True)
    frame_filename = models.FileField(upload_to='')

    def __str__(self):
        return f'{self.frame_number} / {self.confidence} / {self.detection_class}'
    
    def delete(self, *args, **kwargs):
        # 파일이 존재하면 삭제
        if self.frame_filename:
            if os.path.isfile(self.frame_filename.path):
                os.remove(self.frame_filename.path)
        super().delete(*args, **kwargs)
