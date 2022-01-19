#
#
#

from tastypie import fields
from char.models import Character
from dash.api import UserResource
from srd20.api import MonsterResource
from tastypie.exceptions import BadRequest
from tastypie.authorization import Authorization
from game.models import Game, Encounter, EncounterMember
from tastypie.authentication import SessionAuthentication
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS

class GameResource(ModelResource):
    characters = fields.ToManyField('char.api.CharacterResource', 'character_set', blank=True, null=True)
    gm = fields.ToOneField(UserResource, 'gm')
    map = fields.FileField(attribute='map', blank=True, null=True)
    class Meta:
        queryset = Game.objects.all()
        resource_name = 'game'
        list_allowed_methods = ['get', 'post']
        authentication = SessionAuthentication()
        authorization = Authorization()
        always_return_data = True
        filtering = {
            'id': ALL,
            'name': ALL,
        }

    #   This seems to be a widely accepted recipie for doing file
    #   uploads.
    #   Not sure the originating source.
    def deserialize(self, request, data, format=None):
        if not format:
            format = request.META.get('CONTENT_TYPE', 'application/json')
        if format == 'application/x-www-form-urlencoded':
            return request.POST
        if format.startswith('multipart'):
            data = request.POST.copy()
            data.update(request.FILES)
            return data
        return super(GameResource, self).deserialize(request, data, format)

    def obj_create(self, bundle, **kwargs):
        obj = Game.objects.filter(name=bundle.data['name'], gm=bundle.request.user)
        if len(obj) > 0:
            raise BadRequest('Game already exists with that name.')
        return super(GameResource, self).obj_create(bundle, gm=bundle.request.user)

    def authorized_read_list(self, object_list, bundle):
        return object_list.filter(gm=bundle.request.user)


class EncounterResource(ModelResource):
    game = fields.ToOneField(GameResource, 'game', full=True)
    members = fields.ToManyField('game.api.EncounterMemberResource', 'encountermember_set', 
            full=True, null=True, blank=True)
    class Meta:
        queryset = Encounter.objects.all()
        resource_name = 'encounter'
        list_allow_methods = ['get', 'post']
        always_return_data = True
        authentication = SessionAuthentication()
        authorization = Authorization()
        filtering = {
            'id': ALL,
            'game': ALL_WITH_RELATIONS,
            'character': ALL,
            'member': ALL,
        }

    def obj_create(self, bundle, **kwargs):
        '''
        Provide the ability to create Encounter models associated with
        the Game.

        This should only be available of the user is the Game master.
        '''
        game_id = bundle.data.get('game__id', None)
        if game_id is not None:
            #   Ensure that there is a Game with the provided ID
            games = Game.objects.filter(id=game_id)
            if len(games) > 0:
                game = games[0]
                #   Now to make sure current user is the Game Master
                if game.gm == bundle.request.user:
                    name = bundle.data.get('name', None)
                    enc_b = super(EncounterResource, self).obj_create(bundle, game=game)
                    if name is not None:
                        enc_b.obj.name = name
                    else:
                        enc_b.obj.name = enc_b.obj.id
                    enc_b.obj.save()
                    return enc_b
        raise BadRequest('Invalid request type')

    def authorized_read_list(self, object_list, bundle):
        '''
        Provide a list of the Encounters that are associated with the
        Game.

        This method will not allow for a listing of all encounters unless
        the user is marked as an Administrator...THIS IS TODO LATER.

        If the current user is the Game Master of the Game, go ahead and
        provide them the complete list of Encounters associated with the
        Game.

        If they are not the Game Master, ensure that they are a member
        of the Encounter.
        '''
        #   Get the current Game model for the encounter
        game_id = bundle.request.GET.get("game__id", None)
        if game_id is not None:
            game = Game.objects.filter(id=game_id)
            if len(game) == 0:
                #   There was not a Game found with the provided ID.
                raise BadRequest('Game was not found with that identifier.')
            #   Check if the current User is the Game Master over the
            #   current Game
            if game[0].gm == bundle.request.user:
                return object_list.filter(game=game)
            #   User is not the Game Master, are they even a Member
            #   of the encounter
            try:
                character = Character.objects.get(user=bundle.request.user, game=game)
            except Character.DoesNotExist:
                raise BadRequest('Not a Character within the Game.')
            return object_list.filter(game=game, encountermember__character=character)
        raise BadRequest('No Game ID provided.')


class EncounterMemberResource(ModelResource):
    encounter = fields.ToOneField(EncounterResource, 'encounter')
    character = fields.ToOneField('char.api.CharacterResource', 'character', full=True, blank=True, null=True)
    monster = fields.ToOneField('srd20.api.MonsterResource', 'monster', full=True, blank=True, null=True)
    class Meta:
        queryset = EncounterMember.objects.all()
        resource_name = 'member'
        list_allow_methods = ['get', 'post', 'patch']
        authentication = SessionAuthentication()
        authorization = Authorization()
        always_return_data = True
        filtering = {
            'id': ALL,
            'character': ALL_WITH_RELATIONS,
            'encounter': ALL_WITH_RELATIONS,
        }

    def obj_create(self, bundle, **kwargs):
        '''
        Only allow for the Game Master for the current Game to create
        Members within the Encounter.
        '''
        enc = EncounterResource().get_via_uri(bundle.data['encounter'], request=bundle.request)
        if enc.game.gm != bundle.request.user:
            raise BadRequest('Must be the Game Master to add a Member')
        m_uri = bundle.data.get('monster', None)
        c_uri = bundle.data.get('character', None)
        if m_uri is None and c_uri is None:
            raise BadRequest('Missing member to add')
        #   Check to see if a user is attempting to be added
        if c_uri is not None:
            #   OH GOD DO NOT DO THIS
            #
            #   The following abomination is only here for the sake of
            #   getting this fucking thing to a "releasable" point.
            #   
            #   A re-vamp of the overall model heirarchy will be introduced
            #   within the following release.
            from char.api import CharacterResource
            character = CharacterResource().get_via_uri(c_uri, request=bundle.request)
            #   Check to see if the Character is already a Member of the Game.
            member = EncounterMember.objects.filter(encounter=enc, character=character)
            if len(member) > 0:
                raise BadRequest('Character already a member of the Encounter')
        m = super(EncounterMemberResource, self).obj_create(bundle, encounter=enc)
        return m
       
    def authorized_read_list(self, object_list, bundle):
        '''
        '''
        raise BadRequest('Only Members of an Encounter can view Memberships of an Encounter.')

#   vim: fdm=indent fdn=1
