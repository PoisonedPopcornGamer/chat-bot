import asyncio
class EventHook(object):

    def __init__(self):
        self.__handlers = []

    def __iadd__(self, handler): # ex: onMessage += callback
        self.__handlers.append(handler)
        return self

    def __isub__(self, handler): # ex: onMessage -= callback
        self.__handlers.remove(handler)
        return self

    def __call__(self, *args, **keywargs): # ex: onMessage()
        for handler in self.__handlers:
            asyncio.get_event_loop().create_task(handler(*args, **keywargs))