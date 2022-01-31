#
#   Copyright (c)2013
#   All rights reserved.
#

from django.db import models

class Event(models.Model):
    resource_uri = models.CharField(max_length=128)
    date = models.DateTimeField(auto_now_add=True)
    log = models.TextField()

    def __unicode__(self):
        return unicode('[%s] %s - %s' % (self.date, self.resource_uri, self.log))

#   vim: fdm=indent fdn=1
