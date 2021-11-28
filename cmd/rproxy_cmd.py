from cleo import Command
from reverse_proxy_workflow import ReverseProxyWorkflow


class RproxyCommand(Command):
    """
    Executes a Reverse Proxy Command

    rproxy
        {operation? : what operation?}
        {--y|yell : If set, the task will yell in uppercase letters}
    """

    def handle(self):
        ops = self.argument('operation')
        ops = True

        if ops:
            r_proxy = ReverseProxyWorkflow()
            r_proxy.run()
        else:
            text = 'Enter Params'

        # if self.option('yell'):
        #     text = text.upper()

        # self.line(text)
