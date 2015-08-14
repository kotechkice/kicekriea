from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^stdnt/', include('stdnt.urls', namespace='stdnt')),
    url(r'^tch/', include('tch.urls', namespace='tch')),
)
