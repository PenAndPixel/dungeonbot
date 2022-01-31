#
#   Copyright (c)2013
#   All rights reserved.
#

from tastypie import fields
from tastypie.resources import ModelResource, ALL
from srd20.models import Spell, Feat, Ability, CharacterClass, Monster, MonsterAbility, Race, Skill

class SpellResource(ModelResource):
    class Meta:
        queryset = Spell.objects.all()
        resource_name = 'spell'


class FeatResource(ModelResource):
    class Meta:
        queryset = Feat.objects.all()
        resource_name = 'feat'


class AbilityResource(ModelResource):
    class Meta:
        queryset = Ability.objects.all()
        resource_name = 'ability'


class CharacterClassResource(ModelResource):
    class Meta:
        queryset = CharacterClass.objects.all()
        resource_name = 'srd/class'


class MonsterResource(ModelResource):
    class Meta:
        queryset = Monster.objects.all()
        resource_name = 'monster'
        ordering = [
            'initiative',
        ]
        filtering = {
            'name': ('startswith', 'istartswith'),
        }


class MonsterAbilityResource(ModelResource):
    class Meta:
        queryset = MonsterAbility.objects.all()
        resource_name = 'monster_ability'


class RaceResource(ModelResource):
    class Meta:
        queryset = Race.objects.all()
        resource_name = 'race'


class SkillResource(ModelResource):
    ability = fields.ToOneField(AbilityResource, 'ability', full=True)
    class Meta:
        queryset = Skill.objects.all()
        resource_name = 'skill'

#   vim: fdm=indent fdn=1
