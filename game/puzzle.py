# coding=utf-8
import copy
from random import shuffle
from utils.level_handler import get_level_path


class Level:
    def __init__(self, path, level_nr):
        exec(open(path).read())
        self.nr = int(level_nr)
        self.name = locals()['name']
        self.variables = locals()['variables']
        self.init_values = locals()['init_values']
        self.goal_values = locals()['goal_values']
        self.pieces = locals()['pieces']
        self.clue = locals()['clue'].split('\n')
        self.values = copy.deepcopy(self.init_values)

    def reset_level(self):
        """Reset the value to the initial"""
        self.values = copy.deepcopy(self.init_values)

    @property
    def passed(self):
        """Check if level is passed"""
        tmp = True
        for i, v in enumerate(self.variables):
            if self.values[i] != self.goal_values[i]:
                tmp = False
        return tmp

    def execute_snippet(self, snippet_nr):
        """Execute a snippet"""
        for i, v in enumerate(self.variables):
            locals()[v] = self.values[i]
        exec(self.pieces[snippet_nr])
        for i, v in enumerate(self.variables):
            exec("self.values[i] = {}".format(v))

    def execute_snippet_list(self, snippet_list):
        """Execute a list of snippets"""
        for s in snippet_list:
            self.execute_snippet(s)

    @classmethod
    def get_level(cls, nr):
        """Get level file from number"""
        return cls(path=get_level_path(nr), level_nr=nr)

    def shuffle_snippets(self):
        """Shuffle the code snippets"""
        shuffle(self.pieces)
