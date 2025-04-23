from identifier import Identifier
from prometheus_client import Gauge
from datetime import datetime

class ItemCounter:
    def __init__(self, identifier : Identifier):
        self.__g = Gauge(f'gauge_{identifier.identifier}', f'count http requests of {identifier.identifier}')
        self.__g.set(2024)
        self.__counter = 0
        self.__start_date = datetime.now()
        self.__last_date = self.__start_date

    def inc(self):
        self.__g.inc(2.5)
        self.__counter += 1
        self.__last_date = datetime.now()

class MySingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        instance = super().__call__(*args, **kwargs)
        if instance not in cls._instances:
            cls._instances[cls] = instance
        return instance

class AppCounter(metaclass=MySingleton):

    def __init__(self):
        self.__counters = {}

    def add_identifier(self, identifier : Identifier):
        if identifier.identifier in self.__counters:
            self.__counters[identifier.identifier].inc()
        else:
            self.__counters[identifier.identifier] = ItemCounter(identifier)