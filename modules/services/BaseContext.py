##Possibly move to /modules/utils/BaseContext later.

class BaseContext(object):
    def __init__(self, contents:str, author, timestamp:int, channel, *args, service=None, **kwargs):
        self.contents = contents
        self.author = author
        self.timestamp = timestamp
        self.channel = channel
        self.service = service
        self.postInit(*args, **kwargs)
        self.__ro = True
    __ro = False

    def postInit():
        """Overwrite this in a subclass. add any custom values"""
        pass

    def __getattr__(self, name): #try to get an attribute that doesn't exist, useful for being able to add anything service-specific.
        return None

    def __setattr__(self, name, value):
        if self.__ro == True:
            raise AttributeError('Context is read-only!')
        else:
            object.__setattr__(self, name, value)
