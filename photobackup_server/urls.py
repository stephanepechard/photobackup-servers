from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^up/$', 'photobackup_server.views.up_view'),
)
