from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'told.views.index', name='index'),
    url(r'^post/edit/(\d+)/?$', 'told.views.post_edit', name='post_edit'),
    # url(r'^toldyou/', include('toldyou.foo.urls')),

    url(r'^ajax/agree_post/?$', 'told.views.ajax_post_agree', name='ajax_post_agree'),
    url(r'^ajax/add_short_comments_post/?$', 'told.views.ajax_add_short_comments_post', name='ajax_add_short_comments_post'),
    url(r'^ajax/add_user_post_short_comment/?$', 'told.views.ajax_add_user_post_short_comment', name='ajax_add_user_post_short_comment'),


    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
