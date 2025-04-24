import re

pattern = re.compile('[a-zA-Z0-9\._]+@[a-zA-Z0-9]+\.[a-z]+')

class EmailValidator:

    def __init__(self, email):
        if not re.match(pattern, email):
            raise ValueError('Invalid email')
        self.__email = email

    @property
    def email(self):
        return self.__email