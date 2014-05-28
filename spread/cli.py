#-*- coding: utf-8 -*-
import sys

from commands import CrawlerCommand, Scel2TxtCommand, TestCommand


class CLI(object):

    def __init__(self, commands=()):
        self.command_instances = list()
        self.commands = dict()
        for c in commands:
            self.add_command(c)

    def add_command(self, command_cls):
        command_instance = command_cls()
        self.command_instances.append(command_instance)
        self.commands[command_instance.command] = command_instance

    def execute(self, command_str, args):
        executor = self.commands[command_str]
        executor.set_args(args)
        executor.do()

    def run(self):
        args = sys.argv
        if not len(args) > 1:
            print("Invalid arguments numbers: %d" % len(args))
            return None

        cmd = args[1]
        cmd_args = args[2:]
        self.execute(cmd, cmd_args)


if __name__ == '__main__':
    cli = CLI(commands=(CrawlerCommand, Scel2TxtCommand, TestCommand,))
    cli.run()
