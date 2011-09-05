from django.conf.urls.defaults import patterns, include, url

import views

urlpatterns = patterns('',
    url(r'^(?P<card_uuid>[\w\d-]+)$', views.login_by_uuid, name='member-uuid-to-profile'),       
)
