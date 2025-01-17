from django.shortcuts import render
import os
from pytubefix import YouTube
from django.http import JsonResponse, FileResponse, StreamingHttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import cv2
import json
from ultralytics import YOLO
from django.db import transaction
from .models import YouTubeVideo, FrameDetection
from .utils import get_top_comments, format_duration
from django.db.models import Q
import logging

logger = logging.getLogger(__name__)

def index(request):
    
    search = request.GET.get('search', None)  # 검색어 가져오기
    keyword = request.GET.get('keyword', None)  # 검색어 가져오기
    if search:
        # YouTubeVideo 모델에서 데이터를 조회
        emotions = search.split(',')
        videos = YouTubeVideo.objects.filter(
            Q(
                Q(happy__gte=emotions[0]) &
                Q(anger__gte=emotions[1]) &
                Q(sadness__gte=emotions[2]) &
                Q(panic__gte=emotions[3])
            )|
            (Q(title__icontains=keyword))
        ).order_by('-created_at')
    else:
        # YouTubeVideo 모델에서 데이터를 조회
        videos = YouTubeVideo.objects.all().order_by('-created_at')
    
    
    # 데이터를 딕셔너리 형식으로 변환하여 템플릿에 전달
    video_data = [
        {
            "title": video.title,
            "author": video.author,
            "description": video.description,
            "thumbnail_url": video.thumbnail_url,
            "channel_url": video.channel_url,  # 또는 다른 비디오 관련 URL
            "url": video.video_url,  # 또는 다른 비디오 관련 URL
            "happy": video.happy,
            "anger": video.anger,
            "sadness": video.sadness,
            "panic": video.panic,
            "video_id": video.video_id,
            "duration": format_duration(video.duration)
        }
        for video in videos
    ]
    return render(request, "emotion_tracker/index.html", {"videos": video_data})


def upload(request):
    
    return render(request, "emotion_tracker/upload.html")


def detail(request, video_id):
    video = YouTubeVideo.objects.get(video_id=video_id)
    frames = FrameDetection.objects.filter(video=video)

    data = [{
            'frame_number': frame.frame_number,
            'confidence': frame.confidence,
            'detection_class': frame.detection_class,
            'frame_filename': frame.frame_filename.url,
        } for frame in frames]
    

    # 댓글 가져오기
    comments = get_top_comments(video_id, max_comments=5)

    return render(request, "emotion_tracker/detail.html", {
        "video": video,
        "frames": json.dumps(data),  # Send JSON as a string
        "comments": json.dumps(comments),
        "duration": format_duration(video.duration)
    })

# Frames 저장 경로 설정
# FRAME_DIR = os.path.join(settings.MEDIA_ROOT, 'frames')
FRAME_DIR = settings.MEDIA_ROOT

os.makedirs(FRAME_DIR, exist_ok=True)

@csrf_exempt
def download_video(request):
    if request.method == 'POST':
        try:
            def process_frames():
                data = json.loads(request.body)
                youtube_url = data.get('youtube_url')
                
                # YouTube 영상 다운로드
                yt = YouTube(youtube_url)
                stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
                temp_video_path = os.path.join(settings.MEDIA_ROOT, f"{yt.video_id}.mp4")
                stream.download(output_path=settings.MEDIA_ROOT, filename=temp_video_path)

                # yt.video_id = 'NbOQWjqf6QU'
                # yt.thumbnail_url = 'https://i.ytimg.com/vi/NbOQWjqf6QU/sddefault.jpg?sqp=-oaymwEoCIAFEOAD8quKqQMcGADwAQH4AbYIgAKAD4oCDAgAEAEYciBXKEAwDw==&rs=AOn4CLBo5jdTkLCc3ScSWvxl_MF8PeBSCQ'
                # yt.title = '점점 커지는 음식 먹기 #도레미챌린지'
                # yt.author = '일오팔'
                # yt.channel_url = 'https://www.youtube.com/channel/UCJ4ETdbjB1MDhjwEZDtUlBQ'
                # yt.description = '@bomulsum_g'
                
                # Create or get the video instance
                video, created = YouTubeVideo.objects.get_or_create(
                    video_id=yt.video_id,
                    defaults={
                        'title': yt.title,
                        'author': yt.author,
                        'description': yt.description,
                        'thumbnail_url': yt.thumbnail_url,
                        'channel_url': yt.channel_url,
                        'video_url': youtube_url,
                        'duration' : yt.length,
                    }
                )
                if created == False:
                    error_response = {'error': f'이미 등록된 영상입니다.'}
                    yield json.dumps(error_response)
                    return StreamingHttpResponse(process_frames(), content_type='application/json')
                
                # video_id 에 대한
                # video_id = 'NbOQWjqf6QU'
                # frame 숫자 = 1
                # confidence = 0.53
                # class = 4
                # frame_filename = 


                # 모델 호출
                model = YOLO(os.path.join(settings.BASE_DIR, 'best.pt'))
                
                # 프레임 추출
                cap = cv2.VideoCapture(temp_video_path)
                frame_rate = int(cap.get(cv2.CAP_PROP_FPS))
                progress = 0
                frame_count = 0
                frame_num = 0
                total = 0
                detection_results = []
                emotions = [0] * 4

                with transaction.atomic():  # Using atomic transaction for bulk create
                    detections_to_create = []

                    while cap.isOpened():
                        ret, frame = cap.read()
                        if not ret:
                            break

                        # 1초마다 프레임 저장
                        if frame_count % frame_rate == 0:
                            frame_num += 1
                            frame_filename = f"{yt.video_id}_{frame_num}.jpg"
                            frame_path = os.path.join(FRAME_DIR, frame_filename)
                            
                            results = model.predict(frame)
                            # results = model.track(source=frame, persist=True)
                            results[0].save(frame_path)

                            # frame_paths.append(frame_filename)

                            progress = int((frame_count/ frame_rate / yt.length) * 100)
                            yield json.dumps({'progress': progress, 'frame': frame_filename}) + '\n'

                            # 결과에서 감지 정보 추출
                            detections = []
                            for box in results[0].boxes:
                                detections.append({
                                    'class': int(box.cls),
                                    'confidence': float(box.conf),
                                    'coordinates': box.xyxy.tolist()[0]  # [x1, y1, x2, y2]
                                })

                                # Add detections for the frame
                                detection_obj = FrameDetection(
                                    video=video,
                                    frame_number=frame_num,
                                    confidence=float(box.conf),
                                    detection_class=int(box.cls),
                                    frame_filename=frame_filename
                                )
                                detections_to_create.append(detection_obj)

                                # calculate emotion
                                total += 1
                                emotions[int(box.cls)] += float(box.conf)


                            
                            if len(results[0].boxes) == 0:
                                # Add detections for the frame
                                detection_obj = FrameDetection(
                                    video=video,
                                    frame_number=frame_num,
                                    confidence=-1,
                                    detection_class=-1,
                                    frame_filename=frame_filename
                                )
                                detections_to_create.append(detection_obj)


                            detection_results.append({
                                'frame': frame_filename,
                                'detections': detections
                            })
                                

                        frame_count += 1
                    yield json.dumps({'progress': 100, 'results': yt.video_id}) + '\n'

                total_emotion = 0
                for emotion in emotions:
                    total_emotion += emotion
                YouTubeVideo.objects.filter(video_id=yt.video_id).update(
                    happy=int(emotions[0]/total_emotion*10),
                    anger=int(emotions[1]/total_emotion*10),
                    sadness=int(emotions[2]/total_emotion*10),
                    panic=int(emotions[3]/total_emotion*10)
                )                
                # Bulk create detections
                FrameDetection.objects.bulk_create(detections_to_create)    

                cap.release()
                os.remove(temp_video_path)

            return StreamingHttpResponse(process_frames(), content_type='application/json')

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method!'}, status=405)


def serve_frame(request, filename):
    file_path = os.path.join(FRAME_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), content_type='image/jpeg')
    return JsonResponse({'error': 'File not found!'}, status=404)