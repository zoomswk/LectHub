import json

from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django import forms
from django.conf import settings

from django.views.decorators.csrf import csrf_exempt

from .models import Video
import moviepy.editor as mp

from rev_ai import apiclient

# Create your views here.
def index(request):
    return HttpResponse("Hello, world.")



'''
Upload section
'''
def upload(request):

    if request.method == 'GET': ## For default view
        return render(request, 'upload.html')
    elif request.method == 'POST':

        uploadedFile = request.FILES['file']
        fileName = "static/videos/"+uploadedFile.name

        # Write File mp4
        with open(fileName, "wb") as f:
            for chunk in uploadedFile.chunks():
                f.write(chunk)

        # Convert to mp3
        mp3fileName=fileName[:-4]+".mp3"
        clip = mp.VideoFileClip(fileName).subclip(0)
        mp3fileNameNoFolder = uploadedFile.name[:-4]+".mp3"
        clip.audio.write_audiofile(mp3fileName)
        # rev_ai  request

        # Create client with your access token
        client = apiclient.RevAiAPIClient(settings.REV_ACCESS_TOKEN)
        callback_url="http://35.239.24.77/vidhub/apis/revai/"
        # Submit from local file
        file_job = client.submit_job_local_file(filename=mp3fileName,callback_url=callback_url ,metadata="This_is_some_job_metadata", skip_diarization=False)
        
        video_url = "http://35.239.24.77/static/videos/" + uploadedFile.name

        Video.objects.create(title=request.POST['title'], author=request.POST['author'], video_url=video_url, rev_id=file_job.id, subtitle_url='')

        return HttpResponse("Uploaded")
    else:
        return HttpResponse("WTF")

@csrf_exempt
def revai_callback(request):
    json_result=(request.body).decode("utf-8")
    print(json_result)
    job=json.loads(json_result)['job']
    print(job)
    video = Video.objects.get(rev_id=job['id'])
    if job['status'] == 'transcribed':

        # Create client with your access token
        client = apiclient.RevAiAPIClient(settings.REV_ACCESS_TOKEN)
        fileName="static/videos/"+job['name'][:-4]+".vtt"
        caption= client.get_captions(job['id'])
        with open(fileName, "w") as f:
            f.write(caption)

        video.subtitle_url = 'http://35.239.24.77/' + fileName

        video.save()
    else:
        video.subtitle_url = 'failed'
        video.save()
    return HttpResponse("Callback received.")

def vid(request, id):
    video = Video.objects.get(id=id)
    context = {'id': id, 'video_title': video.title, 'video_author': video.author, 'video_url': video.video_url, 'subtitle_url': video.subtitle_url}
    return render(request, 'main.html', context)

def browse(request):
    return render(request, 'browse.html')
