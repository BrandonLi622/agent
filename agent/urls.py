'''
Agent
 Copyright (c) 2014
 Brandon Li, Daniel Tahara, and Christopher Zeng
 All Rights Reserved.
 NOTICE:  All information contained herein is, and remains
 the property of the above authors The intellectual and technical
 concepts contained herein are proprietary to the authors and
 may be covered by U.S. and Foreign Patents, patents in process,
 and are protected by trade secret or copyright law. Dissemination
 of this information or reproduction of this material is strictly
 forbidden unless prior written permission is obtained from
 the authors.
 '''

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
    url(r'^ajax_search/', ajax_search),
    url(r'^ajax_aboutpage/', ajax_aboutpage),
    url(r'^refresh_data/', refresh_data),
    url(r'^reason/', why_recommended),
    #url(r'^w*', bad_address), #matches everything else
)
