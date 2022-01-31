#
#   Copyright (c)2013
#   All rights reserved.
#

from event.models import Event
from tastypie.resources import ModelResource
from tastypie.authorization import DjangoAuthorization
from tastypie.authentication import SessionAuthentication

class EventResource(ModelResource):
    class Meta:
        queryset = Event.objects.all()
        resource_name = 'event'
        authorization = DjangoAuthorization()
        authentication = SessionAuthentication()

#   vim: fdm=indent fdn=2
