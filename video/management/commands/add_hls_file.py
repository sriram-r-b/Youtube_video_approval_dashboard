import subprocess
import os
import json
from django.core.management.base import BaseCommand, CommandError
from django.core.files import File
from video.models import Video
from .download import download
import shutil
class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        folder_path = 'drive_download_folder'
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            shutil.rmtree(folder_path)
        os.mkdir(folder_path)
        download()
        file_list = os.listdir(folder_path)
        Video.objects.all().delete()
        print(file_list)
        for file in file_list:
            if file.endswith('.zip'):
                zip_path = os.path.join(folder_path, file)
                hls_path = os.path.join(folder_path, file.replace(".zip","_hls"))
                
                input_video_path = os.path.join(folder_path, file.replace(".zip",".mp4"))
                subprocess.call(['unzip',zip_path,"-d",hls_path])
                input_data_path = os.path.join(folder_path, file.replace('.zip', '.json'))
                with open(input_data_path, 'r') as json_file:
                    data = json.load(json_file)
                videofile = open(input_video_path, 'rb')
                video=File(videofile, name=input_video_path)
                output_thumbnail_path= os.path.join(hls_path,"finalthumbnail.jpg")
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
                obj.slug=obj.id
                obj.hls = hls_path+"/final_hls.m3u8" 
                obj.thumbnail = output_thumbnail_path
                obj.status = 'Completed'
                obj.is_running = False
                obj.save()