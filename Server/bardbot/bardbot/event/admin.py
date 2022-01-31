#
#   Copyright (c)2013
#   All rights reserved.
#

from django.contrib import admin
from bardbot.event.models import Event

class EventAdmin(admin.ModelAdmin):
    list_display = ('resource_uri', 'date', 'log')
admin.site.register(Event, EventAdmin)

#   vim: fdm=indent fdn=1
