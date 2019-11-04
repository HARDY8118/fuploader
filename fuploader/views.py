from django.shortcuts import render
from django.http import HttpResponse
from fuploader.forms import fileuploadform
import pyAesCrypt
import os

def handle_uploaded_file(f):
    with open('uploads/'+f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    pyAesCrypt.encryptFile('uploads/'+f.name,'uploads/'+f.name+'.aes', "password", 64*1024)
    os.remove('uploads/'+f.name)
    
def index(request):
    if request.method=='POST':
        uploadform=fileuploadform(request.POST,request.FILES)
        if uploadform.is_valid:
            handle_uploaded_file(request.FILES['file'])
            return HttpResponse("Uploaded")
    else:
        uploadform=fileuploadform(request.POST,request.FILES)
    return render(request,'index.html',{'form':uploadform})

def sendHello(request):
    return HttpResponse("<h1>Open</h1>")
