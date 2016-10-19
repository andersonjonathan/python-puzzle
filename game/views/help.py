import os

from .. import actions
from ..graphics_framework.text_window import TextWindow


class Help(TextWindow):
    def __init__(self):
        lines = open(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'help.txt'), 'r').readlines()
        super(Help, self).__init__(lines)
        self.return_value = actions.MENU
