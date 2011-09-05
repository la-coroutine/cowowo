import settings
from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'coroutine.views.home', name='home'),
    # url(r'^coroutine/', include('coroutine.foo.urls')),

                       # (r'^api/', include('mysite.api.urls')),

    url(r'^member/', include('userena.urls')),
    url(r'^member/', include('apps.member.urls')),
    url(r'^coworking/', include('apps.coworking.urls')),

    url(r'^admin/', include(admin.site.urls)),
)

## Static Media
if settings.DEBUG:
    urlpatterns += patterns('',
      (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )

urlpatterns += staticfiles_urlpatterns()

