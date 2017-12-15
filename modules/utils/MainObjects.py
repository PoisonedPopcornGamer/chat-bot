##Possibly move to /modules/utils/BaseContext later.

class MainObject(object):
    def __init__(self, **attributes):
        for i in attributes:
            self.__dict__[i] = attributes[i]

    def __iter__(self):
        for i in self.__dict__:
            yield (i, self.__dict__[i])



class Context(MainObject):
    def __getattr__(self, name): #try to get an attribute that doesn't exist, useful for being able to add anything service-specific, without throwing errors when it isn't there.
        return None


class User(MainObject):
    def __str__(self):
        return str(self.id)