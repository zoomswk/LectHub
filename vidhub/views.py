from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django import forms

from .models import Video


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

        with open(fileName, "wb") as f:
            for chunk in uploadedFile.chunks():
                f.write(chunk)
        return HttpResponse("Uploaded")
    else:
        return HttpResponse("WTF")




def vid(request, uid):
    context = {'uid': uid}
    return render(request, 'player.html', context)
