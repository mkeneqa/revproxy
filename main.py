#!/usr/bin/env python

from cmd.greet_cmd import GreetCommand
from cmd.rproxy_cmd import RproxyCommand
from cmd.copy_cmd import CopyCommand
from cleo import Application

application = Application()
application.add(GreetCommand())
application.add(RproxyCommand())
application.add(CopyCommand())

if __name__ == '__main__':
    application.run()
