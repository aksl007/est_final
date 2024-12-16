from django.shortcuts import render
import os
import uuid
from pytubefix import YouTube
from django.http import JsonResponse, FileResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import cv2
import json

import logging

logger = logging.getLogger(__name__)

def index(request):
    videos = [
        {
            "title": "Learn Django in 10 Minutes",
            "description": "This tutorial will teach you the basics of Django in just 10 minutes.",
            "thumbnail_url": "https://via.placeholder.com/300x200",
            "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        },
        {
            "title": "Understanding Machine Learning",
            "description": "Dive deep into the world of machine learning with this detailed explanation.",
            "thumbnail_url": "https://via.placeholder.com/300x200",
            "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        },
        {
            "title": "Web Development for Beginners",
            "description": "A complete guide to web development for absolute beginners.",
            "thumbnail_url": "https://via.placeholder.com/300x200",
            "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        },{
            "title": "Learn Django in 10 Minutes",
            "description": "This tutorial will teach you the basics of Django in just 10 minutes.",
            "thumbnail_url": "https://via.placeholder.com/300x200",
            "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        },
        {
            "title": "Understanding Machine Learning",
            "description": "Dive deep into the world of machine learning with this detailed explanation.",
            "thumbnail_url": "https://via.placeholder.com/300x200",
            "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        },
        {
            "title": "Web Development for Beginners",
            "description": "A complete guide to web development for absolute beginners.",
            "thumbnail_url": "https://via.placeholder.com/300x200",
            "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        },{
            "title": "Learn Django in 10 Minutes",
            "description": "This tutorial will teach you the basics of Django in just 10 minutes.",
            "thumbnail_url": "https://via.placeholder.com/300x200",
            "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        },
        {
            "title": "Understanding Machine Learning",
            "description": "Dive deep into the world of machine learning with this detailed explanation.",
            "thumbnail_url": "https://via.placeholder.com/300x200",
            "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        },
        {
            "title": "Web Development for Beginners",
            "description": "A complete guide to web development for absolute beginners.",
            "thumbnail_url": "https://via.placeholder.com/300x200",
            "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        },{
            "title": "Learn Django in 10 Minutes",
            "description": "This tutorial will teach you the basics of Django in just 10 minutes.",
            "thumbnail_url": "https://via.placeholder.com/300x200",
            "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        },
        {
            "title": "Understanding Machine Learning",
            "description": "Dive deep into the world of machine learning with this detailed explanation.",
            "thumbnail_url": "https://via.placeholder.com/300x200",
            "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        },
        {
            "title": "Web Development for Beginners",
            "description": "A complete guide to web development for absolute beginners.",
            "thumbnail_url": "https://via.placeholder.com/300x200",
            "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        },{
            "title": "Learn Django in 10 Minutes",
            "description": "This tutorial will teach you the basics of Django in just 10 minutes.",
            "thumbnail_url": "https://via.placeholder.com/300x200",
            "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        },
        {
            "title": "Understanding Machine Learning",
            "description": "Dive deep into the world of machine learning with this detailed explanation.",
            "thumbnail_url": "https://via.placeholder.com/300x200",
            "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        },
        {
            "title": "Web Development for Beginners",
            "description": "A complete guide to web development for absolute beginners.",
            "thumbnail_url": "https://via.placeholder.com/300x200",
            "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        },
    ]
    return render(request, "emotion_tracker/index.html", {"videos": videos})


def upload(request):
    
    return render(request, "emotion_tracker/upload.html")

def detail(request):
    
    return render(request, "emotion_tracker/detail.html")

# Frames 저장 경로 설정
FRAME_DIR = os.path.join(settings.MEDIA_ROOT, 'frames')
os.makedirs(FRAME_DIR, exist_ok=True)

@csrf_exempt
def download_video(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            youtube_url = data.get('youtube_url')
            
            if not youtube_url:
                return JsonResponse({'error': 'YouTube URL is required!'}, status=400)
            
            
            
            # YouTube 영상 다운로드
            yt = YouTube(youtube_url)
            stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
            temp_video_path = os.path.join(settings.MEDIA_ROOT, f"{uuid.uuid4()}.mp4")
            stream.download(output_path=settings.MEDIA_ROOT, filename=temp_video_path)

            # 프레임 추출
            cap = cv2.VideoCapture(temp_video_path)
            frame_rate = int(cap.get(cv2.CAP_PROP_FPS))
            frame_count = 0
            frame_paths = []

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                # 1초마다 프레임 저장
                if frame_count % frame_rate == 0:
                    frame_filename = f"{uuid.uuid4()}.jpg"
                    frame_path = os.path.join(FRAME_DIR, frame_filename)
                    cv2.imwrite(frame_path, frame)
                    frame_paths.append(frame_filename)

                frame_count += 1

            cap.release()
            os.remove(temp_video_path)

            # 프레임 파일명 리스트 반환
            return JsonResponse({'frames': frame_paths}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method!'}, status=405)


def serve_frame(request, filename):
    file_path = os.path.join(FRAME_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), content_type='image/jpeg')
    return JsonResponse({'error': 'File not found!'}, status=404)