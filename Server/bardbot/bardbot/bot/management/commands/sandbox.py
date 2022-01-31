__author__ = 'mhooks'
from char.models import Character
from bot.models import Fight
from bot.models import FightLog
from bot.models import BonusItem

from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    args = 'none'
    help = 'chat with somebody'

    def handle(self, *args, **options):
        # TODO: Need some optimizations to filter out users without an sshkey
        fight = Fight().random_fight('RadCash')
        import pdb; pdb.set_trace()