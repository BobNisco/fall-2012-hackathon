from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'resnet_app.views.index'),
    # url(r'^resnet/', include('resnet.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^cpanel/$', 'resnet_app.views.cpanel'),
    url(r'^cpanel/open', 'resnet_app.views.cpanel_open'),
    url(r'^accounts/login/$', login),
    url(r'^accounts/logout/$', logout),
    url(r'^reports/$', 'resnet_app.views.profile'),
    url(r'^reports/(?P<reportID>[^\.]+)', 
               'resnet_app.views.view_report'),
    url(r'^devices/find/', 'resnet_app.views.find_device'),
)
