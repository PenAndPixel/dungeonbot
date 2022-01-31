from django.db import models
from srd20.models import Monster
from char.models import Character, Name
from django.utils.translation import ugettext_lazy as _
from model_utils import Choices
from model_utils.fields import StatusField

import random

__admin__ = ('IO', 'BonusItem', 'Fight', 'FightLog')

class IO(models.Model):
    """
    what are we looking for? What do we say?

    """

    call = models.CharField(max_length=255)
    response = models.TextField(blank=True)

    def __unicode__(self):
        return unicode(self.call)


class BonusItem(models.Model):
    """
    Random Bonus Item

    """
    ITEM_QUALITY = Choices(
        (1, 'awful', _("Awful")),
        (2, 'shitty', _("Shitty")),
        (3, 'pretty-ok', _("Pretty OK")),
        (4, 'good', _("Good")),
        (5, 'great', _("Great")),
        (6, 'awesome', _("Awesome")),
        (7, 'majestic', _("Majestic")),
    )
    
    ITEM_TYPE = (
        (1, 'Rock'),
        (2, 'Pencil'),
        (3, 'Knife'),
        (4, 'Sword'),
        (5, 'Chainsaw'),
        (6, 'Machine Gun'),
        (7, 'Laser'),
    )
    ITEM_EFFECT = (
        (1, 'Water'),
        (2, 'Rock'),
        (3, 'Fire'),
        (4, 'Acid'),
        (5, 'Plasma'),
    )

    quality = models.CharField(max_length=1, choices=ITEM_QUALITY)
    name = models.CharField(max_length=255)
    item  = models.CharField(max_length=1, choices=ITEM_TYPE)
    effect = models.CharField(max_length=1, choices=ITEM_EFFECT)
    total = models.IntegerField(blank=True, null=True)

    def random_item(self):
        if random.randint(0, 1):
            item = BonusItem.objects.get_or_create(
                quality=random.randint(1, 7),
                name=Name.objects.order_by('?')[0].name,
                item=random.randint(1, 7),
                effect=random.randint(1, 5),
            )[0]
            print(item)
            #import pdb; pdb.set_trace()
            base = item.quality+item.item+item.effect
            item.total = base//3
            item.save()
        else:
            item = None
        return item

    def __str__(self):
        name = "%s %s %s of %s" % (self.get_quality_display(), self.name, self.get_item_display(), self.get_effect_display())
        return name


class FightLog(models.Model):
    """
    Logging history of a single fight

    """
    ACTOR_EFFECT = (
        (0, 'Hero'),
        (1, 'Monster'),
    )

    fight = models.ForeignKey('Fight', on_delete=models.CASCADE)
    damage = models.IntegerField()
    hp = models.IntegerField()
    actor = models.CharField(max_length=1, choices=ACTOR_EFFECT)
    kill = models.BooleanField()

    def __unicode__(self):
        name = "%s does %s hp of damage\n" % (self.get_actor_display(), self.damage)
        return unicode(name)


class Fight(models.Model):
    """
    Single fight instance between a character and his enemy

    """
    timestamp = models.DateTimeField(auto_now=True)
    monster = models.ForeignKey(Monster, on_delete=models.CASCADE)
    item = models.ForeignKey(BonusItem, blank=True, null=True, on_delete=models.CASCADE)
    character = models.ForeignKey(Character, on_delete=models.CASCADE)

    char_attack = models.IntegerField()
    char_hp = models.IntegerField()
    char_hp_max = models.IntegerField()
    char_ac = models.IntegerField()
    mon_attack = models.IntegerField()
    mon_hp = models.IntegerField()
    mon_hp_max = models.IntegerField()
    mon_ac = models.IntegerField()

    win = models.BooleanField()

    def random_fight(self, character):
        #set up all the engagement vars. Based of Pathfinder, but simplified... might be totally broken.
        #Document that fight bitch!
        monster = Monster.objects.order_by('?')[0],
        item = BonusItem().random_item(),


        if item[0]:
            fight = Fight.objects.create(
                monster=monster[0],
                item=item[0],
                character=character,

                char_attack=character.base_attack_bonus(),
                char_hp_max=character.hit_points(),
                char_hp=character.hit_points(),
                char_ac=character.armor_class(),
                mon_attack=monster[0].base_attack_bonus,
                mon_hp_max=monster[0].hit_points.split(' ')[0],
                mon_hp=monster[0].hit_points.split(' ')[0],
                mon_ac=int(monster[0].armor_class.split(',')[0]),

                win=False
            )
        else:
            fight = Fight.objects.create(
                monster=monster[0],
                character=character,

                char_attack=character.base_attack_bonus(),
                char_hp_max=character.hit_points(),
                char_hp=character.hit_points(),
                char_ac=character.armor_class(),
                mon_attack=monster[0].base_attack_bonus,
                mon_hp_max=monster[0].hit_points.split(' ')[0],
                mon_hp=monster[0].hit_points.split(' ')[0],
                mon_ac=int(monster[0].armor_class.split(',')[0]),

                win=False
            )
        win = False

        fight.save()

        hero_intitiative = random.randint(0, 1)

        # LETS DO A FIGHT!
        while int(fight.char_hp) >= 0 and int(fight.mon_hp) >= 0:
            d20 = random.randint(1, 20)
            if hero_intitiative == 1:
                #if initiative hero first
                attack = fight.char_attack+d20

                if attack > fight.mon_ac:
                    # Roll 2d6
                    d6a = random.randint(1, 12)
                    d6b = random.randint(1, 12)
                    # add up dice pool with any random item bonus then apply hit
                    if item:
                        pool = d6a+d6b
                    else:
                        pool = d6a+d6b+fight.item.total
                    fight.mon_hp = int(fight.mon_hp)-pool

                    #If the monster is dead, win the fight
                    if fight.mon_hp <= 0:
                        win = True
                        print("Hero Win")

                    #log the fight
                    log = FightLog(
                        fight=fight,
                        damage=pool,
                        hp=fight.mon_hp,
                        actor=0,
                        kill=win,
                    )

                    if win:
                        fight.win=True
                        fight.save()
                    fight.save()
                    log.save()
                    print(log)

                hero_intitiative = 0

            else:
                #if initiative monster first
                attack = fight.mon_attack+d20

                if attack > fight.char_ac:
                    # Roll 2d6
                    d6a = random.randint(1, 12)
                    d6b = random.randint(1, 12)
                    # add up dice pool then apply hit
                    pool = d6a+d6b
                    fight.char_hp = int(fight.char_hp)-pool

                    #If the monster is dead, win the fight
                    if fight.char_hp <= 0:
                        win = True
                        print("Monster Win")

                    #log the fight
                    log = FightLog(
                        fight=fight,
                        damage=pool,
                        hp=fight.char_hp,
                        actor=1,
                        kill=win,
                    )
                    fight.save()
                    log.save()
                    print(log)

                hero_intitiative = 1

        return fight