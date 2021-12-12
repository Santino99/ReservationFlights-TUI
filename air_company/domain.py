import re
from dataclasses import dataclass, InitVar, field
import datetime
from typing import Any, List

from typeguard import typechecked
from valid8 import validate

from validation.dataclasses import validate_dataclass
from validation.regex import pattern


@typechecked
@dataclass(frozen=True, order=True)
class Author:
    value: int

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value)

    def __str__(self):
        return str(self.value)


@typechecked
@dataclass(order=True, frozen=True)
class Name:
    value: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value, min_len=1, max_len=50, custom=pattern(r'^[A-Z][a-z]*(?:\s[A-Z][a-z]*)*$'))

    def __str__(self) -> str:
        return self.value


@typechecked
@dataclass(order=True, frozen=True)
class Surname:
    value: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value, min_len=1, max_len=50, custom=pattern(r'^[A-Z][a-z]*(?:\s[A-Z][a-z]*)*$'))

    def __str__(self) -> str:
        return self.value


@typechecked
@dataclass(order=True, frozen=True)
class Departure:
    value: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value, min_len=1, max_len=50, custom=pattern(r'^[A-Z][a-z]*(?:\s[A-Z][a-z]*)*$'))

    def __str__(self) -> str:
        return self.value


@typechecked
@dataclass(order=True, frozen=True)
class Destination:
    value: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value, min_len=1, max_len=50, custom=pattern(r'^[A-Z][a-z]*(?:\s[A-Z][a-z]*)*$'))

    def __str__(self) -> str:
        return self.value


@typechecked
@dataclass(order=True, frozen=True)
class Price:
    value_in_cents: int
    create_key: InitVar[Any] = field(default=None)
    __create_key = object()
    __max_value = 100000000000 - 1
    __parse_pattern = re.compile(r'(?P<euro>\d{0,11})(?:\.(?P<cents>\d{2}))?')

    def __post_init__(self, create_key):
        validate('create_key', create_key, equals=self.__create_key)
        validate_dataclass(self)
        validate('value_in_cents', self.value_in_cents, min_value=0, max_value=self.__max_value)

    def __str__(self) -> str:
        return f'{self.value_in_cents // 100}.{self.value_in_cents % 100:02}'

    @staticmethod
    def create(euro: int, cents: int = 0) -> 'Price':
        validate('euro', euro, min_value=0, max_value=Price.__max_value // 100)
        validate('cents', cents, min_value=0, max_value=99)
        return Price(euro * 100 + cents, Price.__create_key)

    @staticmethod
    def parse(value: str) -> 'Price':
        m = Price.__parse_pattern.fullmatch(value)
        validate('value', m)
        euro = m.group('euro')
        cents = m.group('cents') if m.group('cents') else 0
        return Price.create(int(euro), int(cents))

    @property
    def cents(self) -> int:
        return self.value_in_cents % 100

    @property
    def euro(self) -> int:
        return self.value_in_cents // 100


@typechecked
@dataclass(order=True, frozen=True)
class DepartureDateTime:
    value: datetime.datetime

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value, min_value=datetime.datetime.now())

    def __str__(self) -> str:
        return str(self.value)


@typechecked
@dataclass(order=True, frozen=True)
class TimeFlight:
    value: datetime.time

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value, min_value=datetime.time(0, 30))

    def __str__(self) -> str:
        return str(self.value)


@typechecked
@dataclass(order=True, frozen=True)
class Ticket:
    id: int
    author: Author
    name: Name
    surname: Surname
    departure: Departure
    destination: Destination
    price: Price
    departureDateTime: DepartureDateTime
    timeFlight: TimeFlight

    def __post_init__(self):
        validate_dataclass(self)

    def __str__(self):
        return str('name\t surname\t departure\t destination\t price\t departureDateTime\t timeFlight\n' +
                   str(self.name) + '\t' + str(self.surname) + '\t' + str(self.departure) + '\t' + str(self.destination) +
                   '\t' + str(self.price) + '\t' + str(self.departureDateTime) + '\t' + str(self.timeFlight) + '\n')


@typechecked
@dataclass(frozen=True)
class AirCompany:
    __tickets: List[Ticket] = field(default_factory=list, init=False)

    def clear(self):
        self.__tickets.clear()

    def tickets(self) -> int:
        return len(self.__tickets)

    def ticket(self, index: int):
        validate('index', index, min_value=0, max_value=self.tickets() - 1)
        return self.__tickets[index]

    def add_ticket(self, ticket: Ticket) -> None:
        self.__tickets.append(ticket)

    def remove_ticket(self, index: int) -> None:
        validate('index', index, min_value=0, max_value=self.tickets() - 1)
        del self.__tickets[index]

    def sort_by_departure_date(self) -> None:
        self.__tickets.sort(key=lambda x: x.departureDateTime, reverse=True)

    def sort_by_price(self) -> None:
        self.__tickets.sort(key=lambda x: x.price, reverse=True)