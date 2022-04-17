import os

from cleo import Command
import utils.consolidate_media as CMedia
from utils.fcpxml_loader import FcpXmlLoader
import commons


class TimecutsCommand(Command):
    """
    command timecuts

    timecuts
        {xpath : Who do you want to greet?}
    """

    def handle(self):
        _xfile = self.argument('xpath')
        fcp = FcpXmlLoader(_xfile)
        fcp.export_timeline_clips_metadata()
        # fcp.load()
        # print(_xfile)
