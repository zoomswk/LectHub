from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django import forms
# Create your views here.
def index(request):
    return HttpResponse("Hello, world.")


'''
Upload section
'''
from django import forms

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    author = forms.CharField(max_length=50)
    file = forms.FileField()
    

def upload(request):
    
    form = UploadFileForm(request.POST,request.FILES)
    if request.method=='GET': ## For default view
        return render(request, 'vidhub/test.html')
    elif request.method=='POST':
        uploadedFile=request.FILES['file']
        fileName= "storage/"+uploadedFile.name
        with open(fileName, "wb") as f:
            for chunk in uploadedFile.chunks():
                f.write(chunk)
            
        return HttpResponse("Hello, world. Upload POST")
    else:
        return HttpResponse("WTF")




def vid(request, uid):
    context = {'uid': uid}
    return render(request, 'player.html', context)
