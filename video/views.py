import os 
from django.shortcuts import render
from django.urls import reverse
from django.http import FileResponse, HttpResponse
from django.shortcuts import get_object_or_404
from video.models import Video
import os
import shutil
from django.conf import settings
import os
import http.client
from .youtube_video_archive import *

base_dir =settings.MEDIA_ROOT    
# youtube upload api
from youtube_upload.client import YoutubeUploader

def all_videos(request):
    videos = Video.objects.filter(status='Completed')

    context = {
        'videos': videos,
    }

    return render(request, 'all_videos.html', context)


def serve_hls_playlist(request, video_id):
    try:
        video = get_object_or_404(Video, pk=video_id)
        print("video_id : ",video_id)
        hls_playlist_path = video.hls
        print(hls_playlist_path)
        # print(os.cwd())
        with open(hls_playlist_path, 'r') as m3u8_file:
            m3u8_content = m3u8_file.read()

        base_url = request.build_absolute_uri('/') 
        serve_hls_segment_url = base_url +"serve_hls_segment/" +str(video_id)
        m3u8_content = m3u8_content.replace('{{ dynamic_path }}', serve_hls_segment_url)
        print("serve_hls_segment_url : ",serve_hls_segment_url)


        return HttpResponse(m3u8_content, content_type='application/vnd.apple.mpegurl')
    except (Video.DoesNotExist, FileNotFoundError):
        return HttpResponse("Video or HLS playlist not found", status=404)


def serve_hls_segment(request, video_id, segment_name):
    try:
        video = get_object_or_404(Video, pk=video_id)
        hls_directory = os.path.dirname(video.hls)
        segment_path = os.path.join(hls_directory, segment_name)

        # Serve the HLS segment as a binary file response
        return FileResponse(open(segment_path, 'rb'))
    except (Video.DoesNotExist, FileNotFoundError):
        return HttpResponse("Video or HLS segment not found", status=404)


def hls_video_player(request, video_id):
    video = Video.objects.filter(slug=video_id).first()
    hls_playlist_url = reverse('serve_hls_playlist', args=[video.id])
    
    

    context = {
        'hls_url': hls_playlist_url,
        'video': video,
    }

    return render(request, 'video_player.html', context)





# Create your views here.
def upload_video(request, video_id):
    
    print("uploading video")
    uploader = YoutubeUploader(secrets_file_path=os.path.join(base_dir,"<youtube credentials path - json>"))
    # uploader.authenticate(oauth_path='oauth.json')
    uploader.authenticate(oauth_path=os.path.join(base_dir,"<youtube credentials path status,token storage - json>"))
    video = Video.objects.filter(slug=video_id).first()
    title = video.name
    file_path = video.video.path
    # uploader.authenticate()
    description = video.description
    tags=video.hashtags
    tags=tags.split(",")
    image_url=video.image_url
    # Video options
    options = {
        "title" :title, # The video title
        "description" : description, # The video description
        "tags" : tags,
        "categoryId" : "42",
        "privacyStatus" : "public", # Video privacy. Can either be "public", "private", or "unlisted"
        "kids" : False, # Specifies if the Video if for kids or not. Defaults to False.
        "thumbnailLink" : image_url # Optional. Specifies video thumbnail.

    }
    
    # upload video
    print(uploader.upload(file_path, options))
    put_data_to_db(video)
    return render(request, 'video_uploaded.html', {'video': video})
