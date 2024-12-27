from youtube_comment_downloader import YoutubeCommentDownloader

def get_top_comments(video_id, max_comments=10):
    # 유튜브 댓글 다운로더 객체 생성
    downloader = YoutubeCommentDownloader()
    
    # 댓글 가져오기
    comments = downloader.get_comments(video_id, sort_by=0)  # 인기 댓글 기준
    top_comments = []
    
    # 최대 댓글 수만큼 가져오기
    for comment in comments:
        if len(top_comments) >= max_comments:
            break
        top_comments.append({
            "author": comment['author'],       # 댓글 작성자
            "text": comment['text'],           # 댓글 내용
            "likes": comment['votes'],         # 좋아요 수
            "time": comment['time']            # 작성 시간
        })
    
    return top_comments

def format_duration(seconds):
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes}:{secs:02}"  # MM:SS 형식