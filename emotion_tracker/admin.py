from django.contrib import admin
from .models import YouTubeVideo, FrameDetection

# FrameDetection을 YouTubeVideo 모델의 인라인으로 추가
class FrameDetectionInline(admin.TabularInline):  # TabularInline을 사용하여 테이블 형식으로 표시
    model = FrameDetection
    extra = 1  # 기본적으로 표시되는 빈 폼 수
    fields = ('frame_number', 'confidence', 'detection_class', 'frame_filename')  # 표시할 필드

@admin.register(YouTubeVideo)
class YouTubeVideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'video_id', 'created_at')  # 유튜브 비디오 목록에서 보여줄 필드
    search_fields = ('title', 'author', 'video_id')  # 검색할 수 있는 필드
    list_filter = ('created_at',)  # 날짜 필터
    inlines = [FrameDetectionInline]  # 프레임 디텍션 정보를 유튜브 비디오 페이지에 표시

@admin.register(FrameDetection)
class FrameDetectionAdmin(admin.ModelAdmin):
    list_display = ('video', 'frame_number', 'confidence', 'detection_class')  # 프레임 디텍션 목록에서 보여줄 필드
    search_fields = ('video__title', 'frame_number')  # 유튜브 비디오 제목과 프레임 번호로 검색
    list_filter = ('detection_class',)  # 디텍션 클래스에 따른 필터링