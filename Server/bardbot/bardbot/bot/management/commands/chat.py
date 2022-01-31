__author__ = 'Miller Hooks'

from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    args = 'none'
    help = 'chat with somebody'

    def handle(self, *args, **options):
        # TODO: Need some optimizations to filter out users without an sshkey
	import irc
	import cleverbot
	import pdb; pdb.set_trace()
