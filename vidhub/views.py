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
    if request.method=='GET': ## For default view
        return render(request, 'vidhub/test.html')
    elif request.method=='POST':
        form = UploadFileForm(request.POST['title'],request.POST['author'],None)
        
        return HttpResponse("Hello, world. Upload POST")
    else:
        return HttpResponse("WTF")




def vid(request, uid):
    context = {'uid': uid}
    return render(request, 'vidhub/player.html', context)
