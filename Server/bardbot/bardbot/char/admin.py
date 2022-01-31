#
#   Copyright (c)2013
#   All rights reserved.
#

from django.contrib import admin
from bardbot.char.models import Character, Class, CharacterHealth, Invite, Name

class NameAdmin(admin.ModelAdmin):
    list_display = ('name', )
admin.site.register(Name, NameAdmin)

class CharacterAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'race', 'game', 'level', 'sex', 'xp')
admin.site.register(Character, CharacterAdmin)

class ClassAdmin(admin.ModelAdmin):
    list_display = ('character', 'type', 'level')
admin.site.register(Class, ClassAdmin)

class CharacterHealthAdmin(admin.ModelAdmin):
    list_display = ('character', 'maximum', 'current')
admin.site.register(CharacterHealth, CharacterHealthAdmin)

class InviteAdmin(admin.ModelAdmin):
    list_display = ('game', 'date', 'character')
admin.site.register(Invite, InviteAdmin)

#   vim: fdm=indent fdn=1
