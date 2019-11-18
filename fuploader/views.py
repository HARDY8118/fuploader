from django.shortcuts import render
from django.http import HttpResponse
from fuploader.forms import fileuploadform
import pyAesCrypt
import os
from os import listdir
from os.path import isfile, join
from django.core.files import File

def handle_uploaded_file(f):
    with open('uploads/'+f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    pyAesCrypt.encryptFile('uploads/'+f.name,'uploads/'+f.name+'.aes', "password", 128*1024)
    os.remove('uploads/'+f.name)
    
def index(request):
    if request.method=='POST':
        uploadform=fileuploadform(request.POST,request.FILES)
        if uploadform.is_valid:
            handle_uploaded_file(request.FILES['file'])
            return HttpResponse("Uploaded")
    else:
        uploadform=fileuploadform(request.POST,request.FILES)
        onlyfiles = [f for f in listdir('uploads/') if isfile(join('uploads/',f))]
    return render(request,'index.html',{'form':uploadform,'files':onlyfiles})

def downloads(request):
    
    onlyfiles = [f for f in listdir('uploads/') if isfile(join('uploads/',f))]
    # return HttpResponse(request,'downloads.html',{'files':'onlyfiles'})
    return render(request,'downloads.html',{'files':onlyfiles})

def download(request,file_name):
    pyAesCrypt.decryptFile('uploads/'+file_name,'temp_files/'+file_name[:-3],"password",128*1024)
    
    filename=file_name[:-3]
    print(filename)
    path_to_file="http://localhost:8000/temp_files/"+filename
    # response = HttpResponse(mimetype='application/force-download')
    # response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(file_name)
    # response['X-Sendfile'] = smart_str(path_to_file)
    return HttpResponse("<a href='"+path_to_file+"' download >expirelink</a>")