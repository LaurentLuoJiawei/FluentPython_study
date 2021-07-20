"""
    Des：命令模式
    Date: 2021.05.17
"""
from abc import ABC, abstractmethod

class App:
    pass

class Menu:
    pass

class Command:
    def __call__(self):
        return self.execute

    def execute(self, data):
        pass

class OpenCommand(Command):
    def execute(self, data):
        pass

class PasteCommand(Command):
    def execute(self, data):
        pass

class MacroCommand(Command):
    def __init__(self, commands):
        self.commands = list(commands)

    def execute(self, data):
        for com in self.commands:
            com()


# 维护command 列表实现
commands_list = []
