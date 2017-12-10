##Possibly move to /modules/utils/BaseContext later.

class _MainObject(object):
    def __init__(self, attributes:dict):
        for i in attributes:
            self.__dict__[i] = attributes[i]



class Context(_MainObject):
    def __getattr__(self, name): #try to get an attribute that doesn't exist, useful for being able to add anything service-specific, without throwing errors when it isn't there.
        return None