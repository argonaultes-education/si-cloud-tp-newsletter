from identifier import Identifier
from prometheus_client import Gauge
from datetime import datetime
from hashlib import md5
import hmac

SECRET_KEY=b'secret'

class ItemCounter:
    MAX_QUERIES = 300
    MIN_INTERVAL_TIME_S = 300
    def __init__(self, identifier : Identifier):
        self.__g = Gauge(f'gauge_{identifier.identifier}', f'count http requests of {identifier.identifier}')
        self.__identifier = identifier
        self.__reset()

    def inc(self):
        self.__g.inc(2.5)
        self.__counter += 1
        self.__last_date = datetime.now()

    def __reset(self):
        self.__g.set(2024)
        self.__counter = 0
        self.__start_date = datetime.now()
        self.__last_date = self.__start_date

    @property
    def total_seconds(self):
        return self.__last_date - self.__start_date

    @property
    def validation_code(self):
        if self.__counter >= self.MAX_QUERIES and self.total_seconds >= self.MIN_INTERVAL_TIME_S:
            response_hash = hmac.new(SECRET_KEY, self.__identifier.identifier.encode('UTF-8'), md5)
            response = response_hash.hexdigest()
            self.__reset()
            return response
        return self.__identifier.identifier

class MySingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        instance = super().__call__(*args, **kwargs)
        if cls not in cls._instances:
            cls._instances[cls] = instance
        return cls._instances[cls]

class AppCounter(metaclass=MySingleton):

    def __init__(self):
        self.__counters = {}

    def add_counter(self, identifier : Identifier):
        if identifier.identifier in self.__counters.keys():
            self.__counters[identifier.identifier].inc()
        else:
            self.__counters[identifier.identifier] = ItemCounter(identifier)

    def get_validation_code(self, identifier : Identifier):
        if identifier.identifier in self.__counters:
            return self.__counters[identifier.identifier].validation_code
        else:
            raise ValueError('identifier does not exist')
        