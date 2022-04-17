from cleo import Command


class GreetCommand(Command):
    """
    Greets someone

    greet
        {xpath : Who do you want to greet?}
    """

    def handle(self):
        name = self.argument('name')

        if name:
            text = 'Hello {}'.format(name)
        else:
            text = 'Hello'

        if self.option('yell'):
            text = text.upper()

        self.line(text)