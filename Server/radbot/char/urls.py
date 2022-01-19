#
#   Copyright (c)2013
#   All rights reserved.
#

from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'char.views.characters'),
)

#   vim:
