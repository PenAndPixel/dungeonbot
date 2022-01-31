#
#   Copyright (c)2013
#   All rights reserved.
#

from django.contrib import admin
from bardbot.game.models import Game, Encounter, EncounterMember, EncounterEvent

class GameAdmin(admin.ModelAdmin):
    list_display = ('name', )
admin.site.register(Game, GameAdmin)

class EncounterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
admin.site.register(Encounter, EncounterAdmin)

class EncounterMemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'encounter', 'character', 'monster', 'initiative')
admin.site.register(EncounterMember, EncounterMemberAdmin)

class EncounterEventAdmin(admin.ModelAdmin):
    list_display = ('id', 'encounter', 'timestamp', 'notes')
admin.site.register(EncounterEvent, EncounterEventAdmin)

#   vim: fdm=indent fdn=1
