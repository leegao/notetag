from django.db import models
from django.contrib.auth.models import User
import datetime

from django.contrib import admin

class Annotation(models.Model):
    aud_id=models.ForeignKey('AudioMeta');
    user_id=models.ForeignKey(User);
    time=models.IntegerField();
    msg=models.TextField();
    date_added=models.DateTimeField(auto_now_add=True);
    
class Transcription(models.Model):
    aud_id=models.ForeignKey('AudioMeta');
    user_id=models.ForeignKey(User);
    st_time=models.IntegerField();
    end_time=models.IntegerField();
    msg=models.TextField();
    date_added=models.DateTimeField(auto_now_add=True);
    
class AudioMeta(models.Model):
    user_id=models.ForeignKey(User);
    annotations=models.IntegerField(null=True);
    transcriptions=models.IntegerField(null=True);
    plays=models.IntegerField(null=True);
    likes=models.IntegerField(null=True);
    name=models.CharField(max_length=20);
    date_added=models.DateTimeField(auto_now_add=True);
    type = models.CharField(max_length=20)
    bytes = models.IntegerField(default=0)
    length = models.IntegerField(default=0)
    def get_permalink(self):
        return '/audio/'+self.id;
    def suicide(self):
        if (datetime.datetime.now() - self.date_added  > datetime.timedelta(minutes=10)):
            self.delete();

admin.site.register(AudioMeta)


class Bookmark(models.Model):
    aud_id = models.ForeignKey('AudioMeta')
    time = models.IntegerField()
    
admin.site.register(Bookmark)
class Users(models.Model):
    user = models.ForeignKey(User)
    karma=models.IntegerField();
    transcriptions=models.IntegerField();
    annotations=models.IntegerField();
