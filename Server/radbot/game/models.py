#
#   Copyright (c)2013
#   All rights reserved.
#

import random
from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    #gm = models.ForeignKey(User)
    name = models.CharField(max_length=32)
    #map = models.FileField(upload_to='maps/', null=True, blank=True)

    def __unicode__(self):
        return unicode(self.name)


class Encounter(models.Model):
    game = models.ForeignKey(Game)
    name = models.CharField(max_length=32)

    def __unicode__(self):
        return unicode(self.name)


class EncounterMember(models.Model):
    encounter = models.ForeignKey(Encounter)
    character = models.ForeignKey('char.Character', null=True, blank=True)
    monster = models.ForeignKey('srd20.Monster', null=True, blank=True)
    initiative = models.IntegerField()

    def __unicode__(self):
        u_str = '[%s] %s - ' % (self.encounter.game, self.encounter.id)
        if self.character:
            u_str += '%s : ' % self.character
        elif self.monster:
            u_str += '%s : ' % self.monster
        else:
            u_str += 'UNKNOWN : '
        u_str += '%s' % self.initiative
        return unicode(u_str)


class EncounterEvent(models.Model):
    encounter = models.ForeignKey(Encounter)
    timestamp = models.DateTimeField(auto_now_add=True)
    notes = models.TextField()

    def __unicode__(self):
        return unicode('[%s : %s] - %s' % (self.encounter, self.timestamp, self.notes))

#   vim: fdm=index fdn=2
