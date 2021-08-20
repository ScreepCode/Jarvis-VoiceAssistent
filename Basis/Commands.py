from Modules import Greeting, Test


class Cmd(object):
    def __init__(self, callables, module):
        self.callables = callables
        self.module = module

cmds = [
    Cmd(["hallo", "hey", "hi", "moin"], Greeting.greet), 
    Cmd(["test"], Test.ausgabe)
]


def performCommand(command):
    for cmd in cmds:
        if command in cmd.callables:
            cmd.module(command)