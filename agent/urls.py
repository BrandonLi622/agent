from django.conf.urls import patterns, include, url
from django.contrib import admin

from agent_app.views import fb_login, logged_in, bad_address
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'agent.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^agent/', fb_login),
    url(r'^home/(?P<accessToken>\w*)/$', logged_in),
    #url(r'^w*', bad_address), #matches everything else
)
