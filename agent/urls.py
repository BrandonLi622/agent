from django.conf.urls import patterns, include, url
from django.contrib import admin

from agent_app.views import *
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'agent.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^agent/', search),
    url(r'^home/(?P<accessToken>\w*)/$', logged_in),
    url(r'^test/', tests),
    url(r'^ajax_search/', ajax_search)
    #url(r'^w*', bad_address), #matches everything else
)
