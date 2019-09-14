from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django import forms
from django.conf import settings

from django.views.decorators.csrf import csrf_exempt

from .models import Video
import moviepy.editor as mp
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
        fileName = "storage/"+uploadedFile.name
        Video.objects.create(title=request.POST['title'], author=request.POST['author'], video_url=uploadedFile.name, rev_id=0, subtitle_url='')
        # Write File mp4
        with open(fileName, "wb") as f:
            for chunk in uploadedFile.chunks():
                f.write(chunk)

        # Convert to mp3
        
        clip = mp.VideoFileClip(fileName).subclip(0)
        clip.audio.write_audiofile(fileName[:-4]+".mp3")
        #
        
        return HttpResponse("Uploaded" + settings.REV_ACCESS_TOKEN)
    else:
        return HttpResponse("WTF")

@csrf_exempt
def revai_callback(request):
    job = request.POST['job']
    video = Video.objects.get(rev_id=job['id'])
    if job['status'] == 'transcribed':
        video.subtitle_url = 'ready'
    else:
        video.subtitle_url = 'failed'
    return HttpResponse("Callback received.")

def vid(request, uid):
    context = {'uid': uid}
    return render(request, 'player.html', context)