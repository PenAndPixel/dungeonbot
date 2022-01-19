__author__ = 'Miller Hooks'

from django.core.management.base import BaseCommand, CommandError

from bot import models

import irc.bot
import irc.strings
from irc.client import ip_numstr_to_quad, ip_quad_to_numstr

from char.models import Name, Character


class DungeonBot(irc.bot.SingleServerIRCBot):
    def __init__(self, channel, nickname, server, port=6667):
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        self.channel = channel

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")

    def on_welcome(self, c, e):
        c.join(self.channel)

    def on_privmsg(self, c, e):
        self.do_command(e, e.arguments[0])

    def on_pubmsg(self, c, e):
        a = e.arguments[0].split(":", 1)
        if len(a) > 1 and irc.strings.lower(a[0]) == irc.strings.lower(self.connection.get_nickname()):
            self.do_command(e, a[1].strip())
        return

    def on_dccmsg(self, c, e):
        c.privmsg("You said: " + e.arguments[0])

    def on_dccchat(self, c, e):
        if len(e.arguments) != 2:
            return
        args = e.arguments[1].split()
        if len(args) == 4:
            try:
                address = ip_numstr_to_quad(args[2])
                port = int(args[3])
            except ValueError:
                return
            self.dcc_connect(address, port)

    def do_command(self, e, cmd):
        nick = e.source.nick
        c = self.connection
#        import pdb; pdb.set_trace()
        try:
            db_cmd = models.IO.objects.get(call=cmd)
        except:
            db_cmd = None
        cmd_split = cmd.split(":", 1)
        if cmd == "disconnect":
            self.disconnect()
        elif cmd == "die":
            self.die()
        elif cmd == "stats":
            for chname, chobj in self.channels.items():
                c.notice(nick, "--- Channel statistics ---")
                c.notice(nick, "Channel: " + chname)
                users = chobj.users()
                users.sort()
                c.notice(nick, "Users: " + ", ".join(users))
                opers = chobj.opers()
                opers.sort()
                c.notice(nick, "Opers: " + ", ".join(opers))
                voiced = chobj.voiced()
                voiced.sort()
                c.notice(nick, "Voiced: " + ", ".join(voiced))

        elif cmd == "generate character please":
            ###
            # Generate a random character for users
            ###

            from char.models import Character
            try:
                char = Character.objects.get(user=nick)
                message = "You already have a user, %s! %s the %s" % (nick, char.name, char.race)
            except:
                char = Character().random_char_get(user=nick)
                char.save()
                message = "%s we generated you a character for #SD Dungeons. You are a %s named %s. " \
                      "Strength: %s, Constitution %s, Intelligence %s, Dexterity %s, Wisdom %s, Charisma %s " \
                      "*** The call of adventure is upon you! Answer it! ***"
                message = message % (char.user, char.race, char.name, char.strength,
                                 char.constitution, char.intelligence, char.dexterity,
                                 char.wisdom, char.charisma)

            c.privmsg(self.channels.items()[0][0], message)

        elif cmd == "fight!":
            from char.models import Character
            from bot.models import Fight
            try:

                Character.objects.get(user=nick)
                fight = Fight().random_fight(nick)
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
            except:
                message = "You don't have a character yet. Please type 'generate character please' to get one."

            c.privmsg(self.channels.items()[0][0], message)

        elif cmd == "fight":
            from srd20.models import Monster

        elif cmd == "dance_party":
            c.notice(self.channels.items()[0][0], "Teach me how to dance please.")
        elif cmd_split[0] == "JOINxx" and nick == 'RadCash':
            print nick
            c.join(cmd)
        elif cmd == "dcc":
            dcc = self.dcc_listen()
            c.ctcp("DCC", nick, "CHAT chat %s %d" % (
                ip_quad_to_numstr(dcc.localaddress),
                dcc.localport))
        elif db_cmd:
            ###
            # use the database
            ###

            c.privmsg(self.channels.items()[0][0], nick + ', ' + db_cmd.response)
        else:
            c.notice(nick, "Not understood: " + cmd)


class Command(BaseCommand):
    """

    """
    args = 'channel, nick, server, port'
    help = "Usage: testbot <server[:port]> <channel> <nickname>"

    def handle(self, *args, **options):
        import sys
        if len(args) != 3:
            print("Usage: testbot <server[:port]> <channel> <nickname>")
            sys.exit(1)

        s = args[0].split(":", 1)
        server = s[0]
        if len(s) == 2:
            try:
                port = int(s[1])
            except ValueError:
                print("Error: Erroneous port.")
                sys.exit(1)
        else:
            port = 6667
        channel = args[1]
        nickname = args[2]

        bot = DungeonBot(channel, nickname, server, port)
        bot.start()
        print "bingo"
