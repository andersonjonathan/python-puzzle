import os
import sys

import pygame

from .. import actions
from ..graphics_framework import JGF
from ..graphics_framework.colors import BLACK, MEDIUM_GRAY, ORANGE, GRAY, BLUE_ISCH
from ..graphics_framework.fonts import BUTTON_FONT, HEADER_FONT
from ..utils.level_handler import get_lock_status, get_levels


class Menu(JGF):
    """
    This is the menu class, it handles the menu
    """

    def __init__(self):
        """
        Creates all graphical data.
        """
        super(Menu, self).__init__((400, 400), 'Python puzzle menu')
        self.levels = get_levels()  # Levels to show in scrollable list. (List of numbers)

        self.add_button('Exit', (300, 340), JGF.EXIT)
        self.add_button('Help', (190, 340), JGF.HELP)

        self.placement_height = 0
        self.item_distance = 30
        self.menu_list_height = len(self.levels) * self.item_distance + self.placement_height
        self.menu_box_height = 240
        self.menu_box_placement = (20, 70)
        self.menu_box = pygame.surface.Surface((360, self.menu_box_height))
        self.menu_list_container = pygame.surface.Surface((360, self.menu_list_height))
        self.menu_box.blit(self.menu_list_container, (0, 0))
        self.menu_list_container.fill(GRAY)

        self.menu_header = HEADER_FONT.render("Choose a level:", True, BLUE_ISCH)
        self.menu_header_box = pygame.Rect((0, 0), (self.width, self.menu_box_placement[1]))
        self.levels_lock = get_lock_status()
        self.level_texts = []
        self.open_levels = []
        self.scroll_y = 0
        self.render_level_list()

    def render_level_list(self):
        self.placement_height = 0
        self.levels_lock = get_lock_status()
        self.level_texts = []
        level_open = True
        self.open_levels = []
        self.menu_list_container.fill(GRAY)
        for l in self.levels:
            if level_open:
                color = ORANGE
                self.open_levels.append(l)
            else:
                color = MEDIUM_GRAY
            tmp = BUTTON_FONT.render("Level " + str(l), True, color)
            self.level_texts.append(tmp)
            self.menu_list_container.blit(tmp, (10, self.placement_height))
            self.placement_height += self.item_distance
            if self.levels_lock[str(l)] == '0':
                level_open = False

        self.scroll_y = 0

    def event_dispatcher(self, e):
        """
        This is the event dispatcher that takes the pygame event and translates it in to a menu event
        """
        if e.type == pygame.QUIT:
            return JGF.EXIT
        elif e.type == pygame.MOUSEBUTTONDOWN:
            if e.button == 1:
                pos = pygame.mouse.get_pos()
                if self.menu_box.get_rect().move(*self.menu_box_placement).collidepoint(*pos):  # in menu list
                    return JGF.MENU_CLICK
                else:
                    event = self.get_button_collision(pos)
                    if event is not None:
                        return event
            if e.button == 4 and self.menu_list_height > self.menu_box_height:
                return JGF.SCROLL_UP
            if e.button == 5 and self.menu_list_height > self.menu_box_height:
                return JGF.SCROLL_DOWN
        elif e.type == pygame.KEYDOWN and self.menu_list_height > self.menu_box_height:
            if e.key == pygame.K_UP:
                return JGF.SCROLL_UP
            if e.key == pygame.K_DOWN:
                return JGF.SCROLL_DOWN

    def event_handler(self, event):
        """
        The logic of the action behind the menu.
        """
        if event is None:
            pass
        elif event == JGF.EXIT:
            sys.exit(1)
        elif event == JGF.SCROLL_UP:
            self.scroll_y = min(self.scroll_y + self.item_distance, 0)
        elif event == JGF.SCROLL_DOWN:
            self.scroll_y = max(self.scroll_y - self.item_distance, self.menu_box_height - self.menu_list_height)
        elif event == JGF.MENU_CLICK:
            pos = pygame.mouse.get_pos()
            choice = (pos[1] - self.menu_box_placement[1] - self.scroll_y) / self.item_distance
            if choice in self.open_levels:
                self.return_value = actions.GAME, choice
                return False
        elif event == JGF.HELP:
            self.return_value = actions.HELP, None
            return False

    def update(self):
        """Updates the graphics"""
        self.screen.fill(BLACK)
        self.screen.blit(self.menu_box, self.menu_box_placement)
        pygame.draw.rect(self.screen, BLACK, self.menu_header_box)
        self.screen.blit(self.menu_header, (20, 20))
        self.menu_box.blit(self.menu_list_container, (0, self.scroll_y))
        super(Menu, self).update()