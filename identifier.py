import re

class Identifier:

    pattern = re.compile('^[a-zA-Z]{2}$')

    def __init__(self, identifier):
        if len(identifier) != 2:
            raise ValueError('expected length is 2')
        if self.pattern.match(identifier) is None:
            raise ValueError('expected 2 a-z letters')
        self.__identifier = identifier.lower()

    @property
    def identifier(self):
        return self.__identifier