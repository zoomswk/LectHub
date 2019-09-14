from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("Hello, world.")

def upload(request):
    return HttpResponse("Hello, world. Upload")

def vid(request, uid):
    context = {'uid': uid}
    return render(request, 'player.html', context)