import asyncio
from modules.services import twitch #will run in if statements later.
from  modules.utils.EventHook import EventHook # for commands later



class Bot:

    def __init__(self):
        self.bot = self
        self.add()

    def register(self, module, *, name=None):
        if not name:
            name = module.__name__
        self.bot.__dict__[name] = module

    def add(self):
        twitch.setup(self.bot)

        self.bot.twitch.onMsg += self.aprint

    async def aprint(self, ctx):
        for i in ctx:
            print(i)

if __name__ == '__main__':
    n = Bot()
    asyncio.get_event_loop().run_forever()