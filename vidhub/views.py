from django.shortcuts import render
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
        form = UploadFileForm(request.GET['title'],request.GET['author'], request.FILES)
        if form.is_valid():
            #handle_uploaded_file(request.FILES['file'])
            return HttpResponse('OW M FG')
        else:
            return HttpResponse('Error parsing')
        return HttpResponse("Hello, world. Upload POST")
    else:
        return HttpResponse("WTF")




'''
Vid View section
'''
def vid(request):
    return HttpResponse("Vid welcome.")