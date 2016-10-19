# coding=utf-8
import sys

from .views.help import Help
from .actions import MENU, GAME, HELP, EXIT
from .views.game import Game
from .views.menu import Menu

if __name__ == '__main__':
    # Sound?
    SOUND = False

    action = MENU
    payload = None
    while True:
        if action == MENU:
            action, payload = Menu().run(sound=SOUND)
        elif action == GAME:
            action = Game(payload).run(sound=SOUND)
        elif action == HELP:
            action = Help().run(sound=SOUND)
        elif action == EXIT:
            sys.exit()
