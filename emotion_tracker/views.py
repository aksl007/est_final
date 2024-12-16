from django.shortcuts import render

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