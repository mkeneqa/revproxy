#!/usr/bin/env python

from cmd.greet_cmd import GreetCommand
from cmd.rproxy_cmd import RproxyCommand
from cleo import Application

application = Application()
application.add(GreetCommand())
application.add(RproxyCommand())

if __name__ == '__main__':
    application.run()
