# Create your views here.

from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from django import forms
from django.contrib.auth.models import User

from models import AudioMeta, Users, Bookmark

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    marks = forms.TimeField(required=False)
    file  = forms.FileField()
    
def main(request):
    return render_to_response("index.html", locals())

import re
extension_re = re.compile(r"\.([^\.]+)$")

@csrf_exempt
#@login_required
def upload(request, usrid):
    if request.method == "POST":


        this = AudioMeta()
        this.name = request.POST['title']
        #try:
        this.user_id = User.objects.get(id=usrid)
        #except:
            #return HttpResponseForbidden()
        this.annotations = 0
        this.transcriptions = 0
        this.plays = 0
        this.likes = 0

        if request.FILES:
            this.bytes = request.FILES['file'].size
            try:
                this.type = extension_re.search(request.FILES['file'].name).group(1).lower()
            except:
                this.type = "wav"
            this.save()
            try:
                marks = request.POST['marks']
                for secs in [int(i.strip()) for i in marks.split(",")]:
                    m = Bookmark(aud_id = this, time = secs)
                    m.save()
            except:
                pass
            handle_uploaded_file(request.FILES['file'], this.id, this.type)
        else:
            return HttpResponseForbidden()

        return HttpResponseRedirect('/')
    else:
        form = UploadFileForm()
        return render_to_response('upload.html', {'form': form, 'usrid':usrid})

@csrf_exempt
def auth(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        try:
            if User.objects.get(username = username): pass
        except:
            return HttpResponse(content="0")

        user = User.objects.get(username = username)
        if not user.check_password(password): return HttpResponse(content="0")
        # If true, we just return the userid because we're lazy
        return HttpResponse(content=str(user.id))
    else:
        return HttpResponse(content="0")

@csrf_exempt
def registration(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        try:
            if User.objects.get(email = email): return HttpResponseRedirect("/registration/")
        except:
            pass
        try:
            if User.objects.get(username = username): return HttpResponseRedirect("/registration/")
        except:
            pass
        u = User(username = username, password=password, email=email)
        u.save()
        U = Users(user=u, karma=0, transcriptions=0, annotations=0)
        U.save()
        return HttpResponseRedirect("/")
    else:
        return render_to_response("registration.html", locals())

import os
def handle_uploaded_file(f, id, ext):
    aud_dir = '/home/leegao/webapps/notetag/notetag/audio/'
    ext = ext.split()[0].lower()
    destination = open(aud_dir+str(id)+'.'+ext, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
    if ext != "wav":
        os.system("ffmpeg -i %s%s.%s %s%s.wav"%(aud_dir,id,ext,aud_dir,id))
    if ext != "mp3":
        os.system("ffmpeg -i %s%s.%s %s%s.mp3"%(aud_dir,id,ext,aud_dir,id))