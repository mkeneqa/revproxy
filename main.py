#!/usr/bin/env python

from cmd.greet import GreetCommand
from cmd.rproxy import RproxyCommand
from cmd.copy import CopyCommand
from cleo import Application

application = Application()
application.add(GreetCommand())
application.add(RproxyCommand())
application.add(CopyCommand())

if __name__ == '__main__':
    application.run()
