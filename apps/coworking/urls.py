from django.conf.urls.defaults import patterns, include, url

import views

urlpatterns = patterns('',
    url(r'^credit/buy$', views.buy_credit, name='coworking-credit-buy'),
    url(r'^pack/buy/(?P<pack_id>\d+)$', views.buy_pack, name='coworking-pack-buy'), 
    url(r'^pack/buy', views.buy_pack, name='coworking-pack-buy'),       
    url(r'^service/list$', views.service_list, name='coworking-service-list'),       
    url(r'^service/buy$', views.service_buy, name='coworking-service-buy'),       
)
