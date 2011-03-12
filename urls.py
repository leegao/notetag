from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
import os
from django.contrib.auth.views import login, logout
from django.views.decorators.csrf import csrf_exempt

urlpatterns = patterns('',
    # Example:
    # (r'^notetag/', include('notetag.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:

    (r'^login/', csrf_exempt(login), {'template_name': 'login.html'}),
    (r'^registration/', 'notetag.interface.views.registration'),
    (r'^logout/', logout),
    (r'^admin/', include(admin.site.urls)),
    (r'^upload/(?P<usrid>\d+)/', 'notetag.interface.views.upload'),
    (r'^user/auth/?', 'notetag.interface.views.auth'),
    (r'^single/(?P<id>\d+)/', 'notetag.interface.views.single'),
    (r'^annotate/(?P<id>\d+)/', 'notetag.interface.views.annotate'),
    (r'^transcribe/(?P<id>\d+)/', 'notetag.interface.views.transcribe'),
    (r'^$', 'notetag.interface.views.main'),
    (r'^accounts/profile/?', 'notetag.interface.views.back'),
    (r'^accounts/', 'notetag.interface.views.back'),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',{'document_root': "/home/leegao/webapps/notetag/notetag/static/"}),
    (r'^audio/(?P<path>.*)$', 'django.views.static.serve',{'document_root': "/home/leegao/webapps/notetag/notetag/audio/"}),
)
