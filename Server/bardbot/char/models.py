#
#   Copyright (c)2013
#   All rights reserved.
#

from django.db import models
from srd20.models import CharacterClass, Race
from django.contrib.auth.models import User
import random


class Name(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return unicode(self.name)

STRENGTH_MOD = {
    1: 0,
    2: 0,
    3: 0,
    4: 0,
    5: 1,
    6: 2,
    7: 3,
    8: 5,
    9: 7,
    10: 10,
    11: 13,
    12: 17,

}

class Character(models.Model):
    SEX_CHOICES = (
        ('F', 'Female'),
        ('M', 'Male'),
    )

    user = models.CharField(max_length=255)
    race = models.ForeignKey('srd20.Race', on_delete=models.CASCADE)
    game = models.ForeignKey('game.Game', null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    level = models.IntegerField()
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    xp = models.IntegerField()
    strength = models.IntegerField(default=10)
    constitution = models.IntegerField(default=10)
    intelligence = models.IntegerField(default=10)
    dexterity = models.IntegerField(default=10)
    wisdom = models.IntegerField(default=10)
    charisma = models.IntegerField(default=10)

    def __unicode__(self):
        return unicode(self.name)

    def base_attack_bonus(self):
        mod = STRENGTH_MOD[self.strength]

        return self.level+mod

    def hit_points(self):
        hp = STRENGTH_MOD[self.level]+5*5
        return hp

    def armor_class(self):
        # 10 + armor bonus + shield bonus + Dexterity modifier + other modifiers
        return 10 + 3 + 4 + self.dexterity*2

    def random_char_get(self, user="", level=1):
        first_name = Name.objects.order_by('?')[0]
        last_name = Name.objects.order_by('?')[0]
        random_char = Character(
            user=user,
            race=Race.objects.order_by('?')[0],
            name=str(first_name) + ' ' + str(last_name),
            level=level,
            xp=0,
            strength=random.randint(1, 10),
            constitution=random.randint(1, 10),
            intelligence=random.randint(1, 10),
            dexterity=random.randint(1, 10),
            wisdom=random.randint(1, 10),
            charisma=random.randint(1, 10),
        )

        return random_char

    def save(self):
        if self.pk is None:
            super(Character, self).save()
        if self.pk is not None:
            try:
                health = self.characterhealth_set.get()
            except CharacterHealth.DoesNotExist:
                health = CharacterHealth(character=self)
                health.save()
        super(Character, self).save()


class CharacterHealth(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    maximum = models.IntegerField(default=0)
    current = models.IntegerField(default=0)

    def __unicode__(self):
        return unicode('[%s] %s : %s' % (self.character.name, self.maximum, self.current))


class Class(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    type = models.ForeignKey(CharacterClass, on_delete=models.CASCADE)
    level = models.IntegerField()
    preferred = models.BooleanField()

    class Meta:
        verbose_name_plural = 'Classes'

    def __unicode__(self):
        return unicode('[%s] %s(%s)' % (self.character.name, self.type, self.level))


class Invite(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    game = models.ForeignKey('game.Game', on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return unicode('[%s] %s - %s' % (self.date, self.game, self.character))

#   vim: fdm=indent fdn=1
