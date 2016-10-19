import abc
import pygame
pygame.init()

from .fonts import BUTTON_FONT
from .colors import GREEN_ISCH, GRAY


class JGF:
    """
    Since pygame is a pain in the ***, I have made my self a simple framework.
    JGF (Jonathans Graphical Framework) =)
    """
    __metaclass__ = abc.ABCMeta

    # Events
    EXIT = 0
    SCROLL_DOWN = 1
    SCROLL_UP = 2
    MENU_CLICK = 3
    BACK = 4
    TEST = 5
    RESTART = 6
    SCROLL_UP_LEFT = 7
    SCROLL_DOWN_LEFT = 8
    SNIPPET_CLICK = 9
    GAME_CLICK = 10
    MOVE = 11
    DELETE = 12
    HELP = 13
    NEXT = 14

    def __init__(self, size, caption):
        """Initialize the window"""
        self.width = size[0]
        self.height = size[1]
        self.size = size
        self.caption = caption
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption(caption)
        self.buttons = []
        self.return_value = None
        self.sound = True

    def add_button(self, content, placement, action):
        """Add button to screen"""
        text = BUTTON_FONT.render(content, 1, GREEN_ISCH)
        text_pos = text.get_rect().move(*placement)
        text_pos.inflate_ip(40, 20)
        self.buttons.append((text, text_pos, action))

    def draw_buttons(self):
        """Draw buttons on screen"""
        for btn in self.buttons:
            pygame.draw.rect(self.screen, GRAY, btn[1])
            self.screen.blit(btn[0], btn[1].move(20, 10))

    def get_button_collision(self, pos):
        """Get button collision"""
        for t, k, v in self.buttons:
            if k.collidepoint(*pos):
                return v

    def update(self):
        """Update the graphics"""
        self.draw_buttons()
        pygame.display.flip()

    @abc.abstractmethod
    def event_dispatcher(self, e):
        """This is the event dispatcher that takes the pygame event and translates it in to a JGF event"""
        return

    @abc.abstractmethod
    def event_handler(self, event):
        """
        This is the event handler that performs a task given a JGF event.
        Return False to break the loop and return to the caller.
        """
        return

    def run(self, sound=True):
        """
        Function for running the program waiting for pygame events and triggering JGF events
        """
        self.sound = sound
        while True:
            for e in pygame.event.get():
                event = self.event_dispatcher(e)
                tmp = self.event_handler(event)
                if tmp == False:
                    return self.return_value
            self.update()

    def reset_window(self):
        """Reset the window to the original size"""
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption(self.caption)
        self.update()
