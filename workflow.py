#!/usr/bin/env python

from cmd.greet import GreetCommand
from cmd.rproxy import RproxyCommand
from cmd.timecuts import TimecutsCommand
from cleo import Application

application = Application()
application.add(GreetCommand())
application.add(RproxyCommand())
application.add(TimecutsCommand())

if __name__ == '__main__':
    application.run()
