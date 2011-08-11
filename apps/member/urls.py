from django.conf.urls.defaults import patterns, include, url

import views

urlpatterns = patterns('',
    url(r'^(?P<card_uuid>[\w\d-]+)$', views.login_by_uuid, name='member-uuid-to-profile'),       
    url(r'^credit/buy$', views.buy_credit, name='member-credit-buy'),       
    url(r'^service/list$', views.service_list, name='member-service-list'),       
    url(r'^service/buy$', views.service_buy, name='member-service-buy'),       
)
