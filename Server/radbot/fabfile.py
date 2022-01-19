from fabric.api import settings, abort, run, \
    cd, local, sudo, env, hosts
from fabric.contrib.console import confirm
import datetime


def bot_connect():
    local("./manage.py superbot irc.snoonet.org '##bottest' MoneySkullzBot")

def open_dungeon():
    local("./manage.py dungeonbot irc.snoonet.org '#sdandd' RadDungeonBot")

def reset_db(file=None):
    local('./manage.py flush --noinput')
    local('./manage.py syncdb --all')
    #local('./manage.py migrate --fake')
    local('ls -Art deployment/fixtures/*.json| tail -n 1')
    if file:
        if file == 'recent':
            local('for f in `ls -Art deployment/fixtures/*.json| tail -n 1`; do ./manage.py loaddata $f; done ')
        else:
            local('./manage.py loaddata %s' % file)
    else:
        local('./manage.py loaddata deployment/fixtures/current.json')

    local('./manage.py createsuperuser')


def rs():
    local('ifconfig && ./manage.py runserver 0.0.0.0:8000')


def quick(message):
    local('git commit -a -m "%s"' % message)
    local('git push')


def n():
    local('rm test.DB')
    local('./manage.py syncdb')
    local('./manage.py loaddata estimator/fixtures/unified_dataset.json')
    local('./manage.py runserver 0.0.0.0:8000')


def create_fixtures(user=None):
    filename = "%s-%s" % (datetime.datetime.now().strftime('%Y-%m-%d-%H%M%S'), user)
    local("./manage.py dumpdata estimator --indent 3 > deployment/fixtures/%s.json" % filename)
