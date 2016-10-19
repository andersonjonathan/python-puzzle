import sys

import pygame

from .colors import GRAY, LIGHT_GRAY, BLACK
from .fonts import CODE_FONT
from .framework import JGF


class TextWindow(JGF):
    """
    This is the menu class, it handles the menu
    """

    def event_handler(self, event):
        """
        The logic of the action behind the menu.
        """
        if event is None:
            pass
        elif event == JGF.EXIT:
            sys.exit(1)
        elif event == JGF.BACK:
            return False
        elif event == JGF.SCROLL_UP:
            self.scroll_y = min(self.scroll_y + self.item_distance, 0)
        elif event == JGF.SCROLL_DOWN and 300 < self.help_text_height:
            self.scroll_y = max(self.scroll_y - self.item_distance, 300 - self.help_text_height)

    def event_dispatcher(self, e):
        if e.type == pygame.QUIT:
            return JGF.EXIT
        elif e.type == pygame.MOUSEBUTTONDOWN:
            if e.button == 1:
                pos = pygame.mouse.get_pos()
                event = self.get_button_collision(pos)
                if event is not None:
                    return event
            if e.button == 4:
                return JGF.SCROLL_UP
            if e.button == 5:
                return JGF.SCROLL_DOWN
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_UP:
                return JGF.SCROLL_UP
            if e.key == pygame.K_DOWN:
                return JGF.SCROLL_DOWN

    def __init__(self, lines):
        """
        Creates all graphical data.
        """
        super(TextWindow, self).__init__((400, 400), 'Python puzzle Help')
        self.add_button('Back', (300, 340), JGF.BACK)
        self.help_text_box = pygame.surface.Surface((360, 300))
        self.help_text_container = pygame.surface.Surface((360, 1000))
        self.help_text_box.blit(self.help_text_container, (0, 0))
        self.help_text_container.fill(GRAY)
        self.scroll_y = 0
        self.placement_height = 0
        self.item_distance = 15
        self.help_text_height = len(lines) * self.item_distance + self.placement_height
        for l in lines:
            tmp = CODE_FONT.render(str(l.replace('\n', '')), True, LIGHT_GRAY)
            self.help_text_container.blit(tmp, (10, self.placement_height))
            self.placement_height += self.item_distance

    def update(self):
        """Updates the graphics"""
        self.screen.fill(BLACK)
        self.screen.blit(self.help_text_box, (20, 20))
        self.help_text_box.blit(self.help_text_container, (0, self.scroll_y))
        super(TextWindow, self).update()
