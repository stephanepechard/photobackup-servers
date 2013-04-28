from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'photobackup_server.views.up_view'),
)
