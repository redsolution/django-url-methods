import os
from grandma.make import BaseMake
from grandma.models import GrandmaSettings

class Make(BaseMake):
    def make(self):
        super(Make, self).make()
        grandma_settings = GrandmaSettings.objects.get_settings()
        grandma_settings.render_to('settings.py', 'urlmethods/grandma/settings.py', {
        })
