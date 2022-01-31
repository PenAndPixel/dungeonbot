#
#   Copyright (c)2013
#   All rights reserved.
#

from tastypie import fields
from game.models import Game
from dash.api import UserResource
from game.api import GameResource
from srd20.models import CharacterClass
from tastypie.exceptions import BadRequest
from tastypie.authorization import DjangoAuthorization
from tastypie.authentication import SessionAuthentication
from srd20.api import RaceResource, CharacterClassResource
from char.models import Character, CharacterHealth, Invite, Class
from tastypie.resources import ModelResource, ALL_WITH_RELATIONS, ALL

class CharacterResource(ModelResource):
    user = fields.ToOneField(UserResource, 'user', full=True)
    race = fields.ToOneField(RaceResource, 'race', full=True)
    game = fields.ToOneField(GameResource, 'game', null=True, blank=True, full=True)
    #health = fields.ToOneField('char.api.CharacterHealthResource', 'characterhealth_set', full=True, null=True, blank=True)
    class Meta:
        queryset = Character.objects.all()
        resource_name = 'char'
        always_return_data = True
        allowed_methods = ['get', 'post', 'put', 'patch']
        authentication = SessionAuthentication()
        authorization = DjangoAuthorization()
        filtering = {
            'id': ALL,
            'name': ALL,
            'game': ALL_WITH_RELATIONS,
            'user': ALL_WITH_RELATIONS,
            'level': ALL_WITH_RELATIONS,
        }

    def obj_create(self, bundle, **kwargs):
        name = bundle.data.get('name', None)
        race = bundle.data.get('race', None)
        if name is None:
            raise BadRequest('Missing required field, name.')
        chars = Character.objects.filter(user=bundle.request.user, name=name)
        if len(chars) > 0:
            raise BadRequest('Character already exists.')
        level = bundle.data.get('level', 1)
        xp = bundle.data.get('xp', 0)
        bundle.data['level'] = level
        bundle.data['xp'] = xp
        return super(CharacterResource, self).obj_create(bundle, user=bundle.request.user)

    def obj_update(self, bundle, **kwargs):
        if bundle.obj.game is not None and bundle.data['game'] == 'None':
            #   User is having a character leave a Game
            bundle.data['game'] = None
            bundle.obj.game = None
            bundle.obj.save()
            return super(CharacterResource, self).obj_update(bundle, game=None, **kwargs)
        return super(CharacterResource, self).obj_update(bundle, **kwargs)

    def authorized_read_list(self, object_list, bundle):
        #   Check if this is a request to pull the Characters for an invitation
        ns = bundle.request.GET.get('name__startswith', None)
        if ns is not None:
            #   Ensure that the current user is a Game Master
            if len(Game.objects.filter(gm=bundle.request.user)) > 0:
                #   Only return the Characters that are not currently members of
                #   any Game
                return object_list.filter(game=None)
        char_name = bundle.request.GET.get('character__name', None)
        if char_name is not None:
            #   API search is trying to read characters by name, this is something
            #   that should be allowed to the general public
            return object_list.filter(name=char_name)
        return object_list.filter(user=bundle.request.user)


class ClassResource(ModelResource):
    character = fields.ToOneField(CharacterResource, 'character')
    char_class = fields.ToOneField(CharacterClassResource, 'type', full=True)
    class Meta:
        queryset = Class.objects.all()
        resource_name = 'class'
        list_allowed_methods = ['get', 'post']
        authentication = SessionAuthentication()
        authorization = DjangoAuthorization()
        filtering = {
            'character': ALL_WITH_RELATIONS,
        }

    def obj_create(self, bundle, **kwargs):
        cls = CharacterClassResource().get_via_uri(bundle.data['type'], bundle.request)
        char = CharacterResource().get_via_uri(bundle.data['character'], bundle.request)
        return super(ClassResource, self).obj_create(bundle, character=char, type=cls, level=1)

class CharacterHealthResource(ModelResource):
    character = fields.ToOneField(CharacterResource, 'character')
    class Meta:
        queryset = CharacterHealth.objects.all()
        resource_name = 'health'
        authentication = SessionAuthentication()
        authorization = DjangoAuthorization()
        filtering = {
            'character': ALL_WITH_RELATIONS,
        }


class InviteResource(ModelResource):
    character = fields.ToOneField(CharacterResource, 'character', full=True)
    game = fields.ToOneField(GameResource, 'game', full=True)
    class Meta:
        queryset = Invite.objects.all()
        resource_name = 'invite'
        authentication = SessionAuthentication()
        authorization = DjangoAuthorization()
        filtering = {
            'character': ALL_WITH_RELATIONS,
            'game': ALL_WITH_RELATIONS,
        }

    def obj_create(self, bundle, **kwargs):
        char = CharacterResource().get_via_uri(bundle.data['character'], request=bundle.request)
        game = GameResource().get_via_uri(bundle.data['game'], request=bundle.request)
        obj = Invite.objects.filter(character=char, game=game)
        if len(obj) > 0:
            #   Invite already exists for user
            raise BadRequest('Character is already invited to this game.')
        return super(InviteResource, self).obj_create(bundle)


    def authorized_read_list(self, object_list, bundle):
        game_id = bundle.request.GET.get('game__id', None)
        if game_id is not None:
            return object_list.filter(game__id=game_id, game__gm=bundle.request.user)
        return object_list.filter(character__user=bundle.request.user)

#   vim: fdm=indent fdn=1
