__author__ = 'mhooks'
from char.models import Character
from bot.models import Fight
from bot.models import FightLog
from bot.models import BonusItem
from django.conf import settings

from django.core.management.base import BaseCommand, CommandError

import discord
import requests
import json
import asyncio
from asgiref.sync import sync_to_async
from char.models import Character
from bot.models import Fight

client = discord.Client()

@sync_to_async
def get_new_character(user):
     ###
    # Generate a random character for users
    ###
    try:
        char = Character.objects.get(user=user.name)
        message = "You already have a user, %s! %s the %s" % (user.name, char.name, char.race.name)
    except:
        char = Character().random_char_get(user=user.name)
        char.save()
        message = "%s we generated you a character for *** Pen and Pixel Dungeons ***. You are a %s named %s. " \
              "Strength: %s, Constitution %s, Intelligence %s, Dexterity %s, Wisdom %s, Charisma %s " \
              "\n\n*** The call of adventure is upon you! Answer it! ***"
        message = message % (char.user, char.race.name, char.name, char.strength,
                         char.constitution, char.intelligence, char.dexterity,
                         char.wisdom, char.charisma)
         
    return(message)

@sync_to_async
def do_fight(user):
    # try:
        #import pdb; pdb; set_trace()
    character = Character.objects.get(user=user.name)
    fight = Fight().random_fight(character)
    if fight.win:
        win = "Won. You will go on to another fight today and gain experience!"
    else:
        win = "Lost. You're gonna have to lick your wounds and go home for the day."
    if fight.item:
        item = " with your %s" % fight.item
    else:
        item = ""
    message = "Holy crap %s! You just fought a %s%s and %s"
    message = message % (fight.character.name, fight.monster.name, item, win)
    
    # except:
    #     message = "You don't have a character yet. Please type 'generate character please' to get one."

    return(message)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$new-character'):

        def check(m):
            return m.author == message.author and m.content.isdigit() 
            
        m = await get_new_character(message.author)
        await message.channel.send(m)

    if message.content.startswith('$fight!'):

        def check(m):
            return m.author == message.author and m.content.isdigit() 
            
        m = await do_fight(message.author)
        await message.channel.send(m)
        


class Command(BaseCommand):
    args = 'none'
    help = 'chat with somebody'

    def handle(self, *args, **options):
        # TODO: Need some optimizations to filter out users without an sshkey
        client.run(settings.DISCORD_API_KEY)
        # fight = Fight().random_fight('RadCash')
        # import pdb; pdb.set_trace()