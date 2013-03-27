from django.conf.urls import patterns, include, url
from . import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'microblog.views.home', name='home'),
    # url(r'^microblog/', include('microblog.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    #url(r'^$', views.HomepageView.as_view(), name='home'),
    #url(r'^$', views.PostListView.as_view(), name='list'),
    url(r'^$', views.HomepageView.as_view(), name='home'),
    url(r'^signup/$', 'infoholic.views.register', name='signup'),
    url(r'^login/$', 'django.contrib.auth.views.login',
        {'template_name': 'infoholic/login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
        {'template_name': 'infoholic/index.html'}, name='logout'),
    url(r'^default/$', 'infoholic.views.user_default', name='user_default'),                   
    url(r'^category/(?P<slug>[\w-]+)/$', 'infoholic.views.category_detail',
        name='category_detail'),
    url(r'^category/(?P<slug1>[\w-]+)/(?P<slug2>[\w-]+)/$',
        'infoholic.views.feed_detail', name='feed_detail'),
    #url(r'^(?P<slug>[\w-]+)/$', views.PostDetailView.as_view(), name='detail'),
)
