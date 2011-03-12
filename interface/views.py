# Create your views here.

from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from django import forms
from django.contrib.auth.models import User

from models import AudioMeta, Users, Bookmark, Annotation, Transcription

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    marks = forms.TimeField(required=False)
    file  = forms.FileField()

def main(request):
    return render_to_response("ic.html")

def back(request):
    return HttpResponseRedirect("/")
import os
def single(request, id):
    aud = AudioMeta.objects.get(id=id)
    a = "[" 
    for i in Annotation.objects.filter(aud_id = aud):
        a += "[%s,'%s'], "%(i.time, i.msg)
    a+="]"
    b = "["
    for i in Transcription.objects.filter(aud_id = aud):
        b += "[%s,'%s'], "%(i.st_time, i.msg)
    b+="]"
    c = "["
    for i in Bookmark.objects.filter(aud_id = aud):
        c += "%s, "%i.time
    c += "]"
    name = aud.name
    f = '/home/leegao/webapps/notetag/notetag/audio/%s.mp3'%id
    size = 60
    try:
        size = os.path.getsize(f)
    except: pass
    time = size / 8000;
    return render_to_response("ind.html", locals())

@csrf_exempt
def annotate(request, id):
    u = User.objects.get(id = 1)
    aud = AudioMeta.objects.get(id=id)
    t = request.POST['t']
    a = open("/home/leegao/webapps/notetag/notetag/test.txt","w")
    a.write(t)
    a.close()
    m = request.POST['data']
    an = Annotation(user_id=u, aud_id = aud, time = int(t), msg = m)
    an.save()
    return HttpResponse(content="0")

@csrf_exempt
def transcribe(request, id):
    u = User.objects.get(id = 1)
    aud = AudioMeta.objects.get(id=id)
    t = request.POST['t']
    m = request.POST['data']
    an = Transcription(user_id=u, aud_id = aud, st_time = int(t), end_time = 0, msg = m)
    an.save()
    return HttpResponse(content="0")

import re
extension_re = re.compile(r"\.([^\.]+)$")

@csrf_exempt
#@login_required
def upload(request, usrid):
    if request.method == "POST":


        this = AudioMeta()
        try:
            this.name = request.POST['title']
        except:
            this.name = "NONE"
        
        try:
            this.user_id = User.objects.get(id=usrid)
        except:
            try:
                 this.user_id = User.objects.get(id=1)
            except:
                 pass

        this.annotations = 0
        this.transcriptions = 0
        this.plays = 0
        this.likes = 0
        
        if request.FILES:
            
            this.bytes = request.FILES['file'].size
            a = open("/home/leegao/webapps/notetag/notetag/audio/a.txt","w")
            a.write(str(request.FILES))
            a.close()
            try:
                this.type = extension_re.search(request.FILES['file'].name).group(1).lower()
            except:
                this.type = "wav"
            this.save()

            try:
                marks = request.POST['marks']
                
                for secs in [int(i.strip()) for i in marks.split(",") if i]:
                    m = Bookmark(aud_id = this, time = secs)
                    m.save()
            except:
                pass

            handle_uploaded_file(request.FILES['file'], this.id, this.type)
        else:
            return HttpResponseForbidden()

        return HttpResponse(content="1")
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
    
    try:
      if ext != "wav":
        os.system("ffmpeg -i %s%s.%s %s%s.wav"%(aud_dir,id,ext,aud_dir,id))
    except: pass
    try:
      if ext != "mp3":
        os.system("ffmpeg -i %s%s.%s %s%s.mp3"%(aud_dir,id,ext,aud_dir,id))
    except: pass


    #os.system("python2.6 %swaveform.py %s%s.wav"%(aud_dir,aud_dir,id))