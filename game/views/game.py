# coding=utf-8
import os
import pygame
import re
import sys

from .. import actions
from ..graphics_framework.text_window import TextWindow
from ..graphics_framework import JGF
from ..graphics_framework.colors import (
    BLACK,
    GREEN,
    RED,
    GRAY,
    ORANGE,
    MEDIUM_GRAY,
    LIGHT_GRAY,
    COMMENT_GRAY,
    GREEN_ISCH,
    BLUE_ISCH
)
from ..graphics_framework.fonts import (
    HEADER_FONT,
    BUTTON_FONT,
    CODE_FONT
)
from ..utils.level_handler import get_levels, get_lock_status, update_lock_status_on_level
from ..puzzle import Level

MEDIA_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'media',)


class Game(JGF):
    """This is the GUI for the python puzzle game"""
    def __init__(self, level_nr):
        super(Game, self).__init__((800, 800), 'Python puzzle')
        self.level = None
        self.menu_header = None
        self.next_text = None
        self.next_text_pos = None
        self.initial_value_height = None
        self.initial_values = None
        self.goal_values = None
        self.right_container = None
        self.right_inner = None
        self.placement_height_left = None
        self.snippets = None
        self.places = None
        self.left_container_top = None
        self.left_container_height = None
        self.left_container = None
        self.scroll_y_left = None
        self.scroll_y_right = None
        self.placement_height_right = None
        self.solution = None
        self.left_window = None
        self.left_window_size = None
        self.waiting_for_up = None
        self.clicked = None
        self.done = None
        self.left_inner = None
        self.internal_init(level_nr)
        self.return_value = actions.MENU

    def internal_init(self, level_nr):
        # Using internal init function to be able to change level with next button
        self.level = Level.get_level(level_nr)
        self.level.shuffle_snippets()
        self.menu_header = HEADER_FONT.render("Level " + str(level_nr) + ": " + self.level.name, True, BLUE_ISCH)

        # Add some buttons
        self.add_button('Menu', (710, 750), JGF.BACK)
        self.add_button('Test', (30, 750), JGF.TEST)
        self.add_button('Restart', (140, 750), JGF.RESTART)
        self.add_button('Clue', (600, 750), JGF.HELP)

        # Adding next button manually to be able to decide when to show and hide it.
        self.next_text = BUTTON_FONT.render("Next", 1, GREEN_ISCH)
        self.next_text_pos = self.next_text.get_rect().move(295, 750)
        self.next_text_pos.inflate_ip(40, 20)

        self.initial_value_height = 25 + len(self.level.variables) * 15

        self.set_initial_and_goal_variables()
        self.create_snippet_list()

        self.left_container_top = 70 + self.initial_value_height + 5
        self.left_container_height = 650 - self.initial_value_height * 2 - 10
        self.left_container = pygame.surface.Surface((385, self.left_container_height))
        self.left_container.fill(GRAY)
        self.left_inner = pygame.surface.Surface((385, 3000))
        self.left_inner.fill(GRAY)

        self.scroll_y_left = 0
        self.scroll_y_right = 0
        self.placement_height_right = 5
        self.solution = []
        self.left_window = []
        self.left_window_size = []
        self.waiting_for_up = False
        self.clicked = None
        try:
            tmp = get_levels()[int(get_levels().index(self.level.nr)) + 1]
            self.done = get_lock_status()[str(level_nr)] == '1'
        except IndexError:
            self.done = False

    def create_snippet_list(self):
        """
        This method creates a scrollable list with the code snippets.
        It also adds syntax highlighting on all reserved python words.
        """
        self.right_container = pygame.surface.Surface((385, 650 - (self.initial_value_height + 5)))  # Outer container for the scroll
        self.right_container.fill(GRAY)
        self.right_inner = pygame.surface.Surface((385, 3000))  # Inner scrolling container for the scroll.
        # The height of the scrollable area is set to 3000 which would allow a pretty long list off snippets.
        self.right_inner.fill(GRAY)

        self.placement_height_left = 5
        self.snippets = []
        i = 0
        self.places = []
        python_keywords = ['and', 'del', 'from', 'not', 'while', 'as', 'elif', 'global', 'or', 'with', 'assert', 'else',
                           'if', 'pass', 'yield', 'break', 'except', 'import', 'print', 'class', 'exec', 'in', 'raise',
                           'continue', 'finally', 'is', 'return', 'def', 'for', 'lambda', 'try']
        for v in self.level.pieces:
            rows = [l for l in v.split('\n') if l and l != "    "]  # Split on linebreak and remove empty lines
            tmp_z = self.placement_height_left
            tmp_list = []
            p = 5
            for l in rows:
                right = 10
                if any(k in l for k in python_keywords):  # if line contains keyword mark the keywords in orange
                    res = re.split('\\b(' + "|".join(python_keywords) + ')\\b', l)
                    tmp = CODE_FONT.render("", True, LIGHT_GRAY)
                    tmp_list.append({'text': tmp, 'place': (10, p)})
                    right += tmp.get_rect().right
                    for r in res:
                        if r in python_keywords:
                            color = ORANGE
                        else:
                            color = LIGHT_GRAY
                        tmp = CODE_FONT.render(r, True, color)
                        tmp_list.append({'text': tmp, 'place': (right, p)})
                        right += tmp.get_rect().right
                        bottom = tmp.get_rect().bottom
                else:
                    tmp = CODE_FONT.render(l, True, LIGHT_GRAY)
                    bottom = tmp.get_rect().bottom
                    tmp_list.append({'text': tmp, 'place': (10, p)})
                p += bottom
                self.placement_height_left += bottom
            p += 5

            self.snippets.append(pygame.surface.Surface((375, p)))
            self.snippets[i].fill(MEDIUM_GRAY)
            for t in tmp_list:
                self.snippets[i].blit(t['text'], t['place'])
            self.right_inner.blit(self.snippets[i], (5, tmp_z))
            self.places.append(tmp_z)
            self.placement_height_left += 15
            i += 1

    def set_initial_and_goal_variables(self):
        """
        Creates 2 boxes containing the initial and goal values of the variables
        """
        self.initial_values = pygame.surface.Surface((385, self.initial_value_height))
        self.initial_values.fill(MEDIUM_GRAY)
        self.goal_values = pygame.surface.Surface((780, self.initial_value_height))
        self.goal_values.fill(MEDIUM_GRAY)
        y = 5
        tmp = CODE_FONT.render("# Initial values", True, COMMENT_GRAY)
        self.initial_values.blit(tmp, (10, y))
        tmp = CODE_FONT.render("# Goal values", True, COMMENT_GRAY)
        self.goal_values.blit(tmp, (10, y))
        y += 15

        for i, v in enumerate(self.level.variables):
            if type(self.level.init_values[i]) == str:
                init_val = "'" + self.level.init_values[i] + "'"
            else:
                init_val = str(self.level.init_values[i])
            if type(self.level.init_values[i]) == str:
                goal_val = "'" + self.level.goal_values[i] + "'"
            else:
                goal_val = str(self.level.goal_values[i])
            tmp = CODE_FONT.render(v + " = " + init_val, True, LIGHT_GRAY)
            self.initial_values.blit(tmp, (10, y))
            tmp = CODE_FONT.render("assert ", True, ORANGE)
            self.goal_values.blit(tmp, (10, y))
            right = tmp.get_rect().right + 10
            tmp = CODE_FONT.render(v + " == " + goal_val, True, LIGHT_GRAY)
            self.goal_values.blit(tmp, (right, y))
            y += 15

    def event_dispatcher(self, e):
        """
        This is the event dispatcher implementation that takes the pygame event and translates it in to a JGF event
        """
        if e.type == pygame.QUIT:
            return JGF.EXIT
        elif e.type == pygame.MOUSEBUTTONUP and self.waiting_for_up:
            pos = pygame.mouse.get_pos()
            if self.left_container.get_rect().move(10, self.left_container_top).collidepoint(
                    *pos):
                return JGF.MOVE
            else:
                return JGF.DELETE
        elif e.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if e.button == 1:
                if self.left_container.get_rect().move(10, self.left_container_top).collidepoint(
                        *pos):
                    return JGF.GAME_CLICK
                elif self.right_container.get_rect().move(405, 70).collidepoint(*pos):
                    return JGF.SNIPPET_CLICK
                elif self.next_text_pos.collidepoint(*pos):
                    return JGF.NEXT
                else:
                    event = self.get_button_collision(pos)
                    if event is not None:
                        return event
            if e.button == 4 and self.right_container.get_rect().move(405, 70).collidepoint(*pos):
                return JGF.SCROLL_UP
            elif e.button == 5 and \
                    self.right_container.get_rect().move(405, 70).collidepoint(*pos) and \
                    self.placement_height_left > 650:
                return JGF.SCROLL_DOWN
            elif e.button == 4 and \
                    self.left_container.get_rect().move(10, self.left_container_top).collidepoint(*pos):
                return JGF.SCROLL_UP_LEFT
            elif e.button == 5 and \
                    self.left_container.get_rect().move(10, self.left_container_top).collidepoint(*pos) and \
                    self.placement_height_right > self.left_container_height:
                return JGF.SCROLL_DOWN_LEFT
        elif e.type == pygame.KEYDOWN:
            pos = pygame.mouse.get_pos()
            if e.key == pygame.K_UP:
                if self.right_container.get_rect().move(405, 70).collidepoint(*pos):
                    return JGF.SCROLL_UP
                elif self.left_container.get_rect().move(10, self.left_container_top).collidepoint(*pos):
                    return JGF.SCROLL_UP_LEFT
            if e.key == pygame.K_DOWN:
                if self.right_container.get_rect().move(405, 70).collidepoint(*pos) and \
                        self.placement_height_left > 650:
                    return JGF.SCROLL_DOWN
                elif self.left_container.get_rect().move(10, self.left_container_top).collidepoint(*pos) and \
                        self.placement_height_right > self.left_container_height:
                    return JGF.SCROLL_DOWN_LEFT

    def test_solution(self):
        """
        Function for testing the solution. If passed next button is enabled.
        """
        self.level.execute_snippet_list(self.solution)
        if self.level.passed:
            update_lock_status_on_level(self.level.nr)
            try:
                tmp = get_levels()[int(get_levels().index(self.level.nr)) + 1]
                self.done = True
            except IndexError:
                self.done = False
            if self.sound:
                pygame.mixer.music.load(os.path.join(MEDIA_PATH, 'victory.mp3'))
                pygame.mixer.music.play()
        else:
            if self.sound:
                pygame.mixer.music.load(os.path.join(MEDIA_PATH, 'fail.mp3'))
                pygame.mixer.music.play()
        self.goal_values.fill(MEDIUM_GRAY)
        y = 5
        tmp = CODE_FONT.render("# Goal values", True, COMMENT_GRAY)
        self.goal_values.blit(tmp, (10, y))
        y += 15
        for i, v in enumerate(self.level.variables):
            tmp = CODE_FONT.render("assert ", True, ORANGE)
            self.goal_values.blit(tmp, (10, y))
            right = tmp.get_rect().right + 10
            if self.level.goal_values[i] == self.level.values[i]:
                color = GREEN
            else:
                color = RED
            tmp = CODE_FONT.render(
                v + " == " + str(self.level.goal_values[i]) + " (" + str(self.level.values[i]) + ")",
                True, color)
            self.goal_values.blit(tmp, (right, y))
            y += 15
        self.level.reset_level()

    def restart(self):
        """
        Restart/reset the level.
        """
        self.solution = []
        self.left_inner.fill(GRAY)
        self.placement_height_right = 5
        self.scroll_y_left = 0
        self.left_window = []
        self.left_window_size = []
        self.goal_values.fill(MEDIUM_GRAY)
        y = 5
        tmp = CODE_FONT.render("# Goal values", True, COMMENT_GRAY)
        self.goal_values.blit(tmp, (10, y))
        y += 15
        for i, v in enumerate(self.level.variables):
            tmp = CODE_FONT.render("assert ", True, ORANGE)
            self.goal_values.blit(tmp, (10, y))
            right = tmp.get_rect().right + 10
            tmp = CODE_FONT.render(v + " == " + str(self.level.goal_values[i]), True, LIGHT_GRAY)
            self.goal_values.blit(tmp, (right, y))
            y += 15
            self.level.reset_level()

    def add_snippet(self):
        """
        Add snippet to left, solution, area
        """
        pos = pygame.mouse.get_pos()
        i = -1
        for p in self.places:
            if p <= (pos[1] - 70 - self.scroll_y_right):
                i += 1
            else:
                break
        if self.placement_height_right + self.snippets[i].get_rect().bottom + 5 <= 3000:
            self.left_inner.blit(self.snippets[i], (5, self.placement_height_right))
            self.placement_height_right += self.snippets[i].get_rect().bottom + 5
            self.left_window.append(self.snippets[i])
            self.left_window_size.append(self.placement_height_right)
            self.solution.append(i)
        else:
            print("Queue is full")

    def move_snippet(self):
        """
        Function for changing order of snippets in left area.
        """
        if self.clicked is None:
            return
        pos = pygame.mouse.get_pos()
        i = 0
        for p in self.left_window_size:
            if p <= (pos[1] - self.left_container_top - self.scroll_y_left):
                i += 1
            else:
                break
        if i < len(self.left_window_size):
            # Dropped on existing, give dropped the new index
            self.left_window.insert(i, self.left_window.pop(self.clicked))
            self.solution.insert(i, self.solution.pop(self.clicked))
        else:
            # Not dropped on other snippet
            self.left_window.append(self.left_window.pop(self.clicked))
            self.solution.append(self.solution.pop(self.clicked))
        self.left_inner.fill(GRAY)
        self.placement_height_right = 5
        self.left_window_size = []
        for snippet in self.left_window:
            self.left_inner.blit(snippet, (5, self.placement_height_right))
            self.placement_height_right += snippet.get_rect().bottom + 5
            self.left_window_size.append(self.placement_height_right)
            self.waiting_for_up = False
        self.clicked = None

    def remove_snippet(self):
        """
        Remove snippet from left area.
        """
        self.left_inner.fill(GRAY)
        del self.left_window[self.clicked]
        del self.solution[self.clicked]
        self.placement_height_right = 5
        self.left_window_size = []
        for snippet in self.left_window:
            self.left_inner.blit(snippet, (5, self.placement_height_right))
            self.placement_height_right += snippet.get_rect().bottom + 5
            self.left_window_size.append(self.placement_height_right)
        self.waiting_for_up = False
        self.clicked = None

    def event_handler(self, event):
        """
        This is the event handler that performs a task given a JGF event.
        """
        if event is None:
            pass
        elif event == JGF.EXIT:
            sys.exit(1)
        elif event == JGF.BACK:
            return False
        elif event == JGF.TEST:
            self.test_solution()
        elif event == JGF.RESTART:
            self.restart()
        elif event == JGF.SNIPPET_CLICK:
            self.add_snippet()
        elif event == JGF.GAME_CLICK:
            pos = pygame.mouse.get_pos()
            i = 0
            for p in self.left_window_size:
                if p <= (pos[1] - self.left_container_top - self.scroll_y_left):
                    i += 1
                else:
                    break
            if i < len(self.left_window_size):
                self.clicked = i
                self.waiting_for_up = True
        elif event == JGF.MOVE:
            self.move_snippet()
        elif event == JGF.DELETE:
            self.remove_snippet()
        elif event == JGF.SCROLL_UP:
            self.scroll_y_right = min(self.scroll_y_right + 30, 0)
        elif event == JGF.SCROLL_DOWN:
            self.scroll_y_right = max(self.scroll_y_right - 30, -(self.placement_height_left - 650))
        elif event == JGF.SCROLL_UP_LEFT:
            self.scroll_y_left = min(self.scroll_y_left + 30, 0)
        elif event == JGF.SCROLL_DOWN_LEFT:
            self.scroll_y_left = max(self.scroll_y_left - 30,
                                     -(self.placement_height_right - self.left_container_height))
        elif event == JGF.HELP:
            TextWindow(self.level.clue).run()
            self.reset_window()
        elif event == JGF.NEXT and self.done:
            try:
                self.internal_init(
                    get_levels()[int(get_levels().index(self.level.nr)) + 1])
            except IndexError:
                pass

    def update(self):
        """
        Update the graphics
        """
        self.screen.fill(BLACK)
        self.screen.blit(self.menu_header, (10, 5))
        self.screen.blit(self.initial_values, (10, 70))
        self.screen.blit(self.left_container, (10, self.left_container_top))
        self.left_container.blit(self.left_inner, (0, 0 + self.scroll_y_left))
        self.screen.blit(self.goal_values, (10, 70 + 650 - self.initial_value_height))
        self.screen.blit(self.right_container, (405, 70))
        self.right_container.blit(self.right_inner, (0, 0 + self.scroll_y_right))
        if self.done:

            pygame.draw.rect(self.screen, GRAY, self.next_text_pos)
            self.screen.blit(self.next_text, self.next_text_pos.move(20, 10))
        super(Game, self).update()
