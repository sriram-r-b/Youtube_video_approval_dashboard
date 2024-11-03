import subprocess
import os
import json
from django.core.management.base import BaseCommand, CommandError
from django.core.files import File
from video.models import Video

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        folder_path = 'drive_download_folder'
        file_list = os.listdir(folder_path)
        for file in file_list:
            if file.endswith('.avi'):
                input_video_path = os.path.join(folder_path, file)
                subprocess.call(['ffmpeg', '-i', input_video_path, '-c:v', 'libx264', '-crf', '19', '-preset', 'slow', '-c:a', 'aac', '-b:a', '192k', '-ac', '2', input_video_path.replace('.avi', '.mp4') ,'-y'])
                input_video_path = input_video_path.replace('.avi', '.mp4')
                input_data_path = os.path.join(folder_path, file.replace('.avi', '.json'))
                with open(input_data_path, 'r') as json_file:
                    data = json.load(json_file)
                videofile = open(input_video_path, 'rb')
                video=File(videofile, name=input_video_path)
                print(data.keys())
                obj = Video.objects.create(
                    name=data['title'], 
                    image_url=data['image_url'],
                    description=data['description'],
                    link=data['link'], 
                    keywords=data['keywords'], 
                    script=data['script'], 
                    images_query=data['images'], 
                    hashtags=data['hashtags'], 
                    video=video)
                obj.save()