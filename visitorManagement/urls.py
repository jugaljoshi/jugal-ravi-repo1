from django.conf.urls import include, url
from django.contrib import admin
admin.autodiscover()
from django.conf import settings
from django.views.static import serve

admin.autodiscover()

''''
/home/jugal/PycharmProjects/VisitorManagement/visitorManagement/urls.py:9:
RemovedInDjango110Warning: django.conf.urls.patterns()
is deprecated and will be removed in Django 1.10. Update your urlpatterns to be a list of django.conf.urls.url() instances instead.
  url(r'^admin/', include(admin.site.urls)),


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
)

if settings.MOBILE_API:
    urlpatterns += patterns('',
        (r'^mapi/', include('visitorManagement.mapi.urls')),
    )
'''

urlpatterns = [
    url(r'^', include(admin.site.urls)),
    url(r'^admin/', include(admin.site.urls)),
]

if settings.MOBILE_API:
    urlpatterns += [
        url(r'^mapi/', include('visitorManagement.mapi.urls')),
    ]

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
