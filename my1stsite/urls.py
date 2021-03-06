from django.conf import settings
from django.conf.urls import patterns, include, url
from . import views
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'my1stsite.views.home', name='home'),
    # url(r'^my1stsite/', include('my1stsite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.HomepageView.as_view(), name='home'),
    url(r'^infoholic/', include('infoholic.urls', namespace='infoholic')),
)

urlpatterns += patterns('',
    (r'^static/(.*)$', 'django.views.static.serve', {
        'document_root': settings.STATIC_ROOT
    }),
)
