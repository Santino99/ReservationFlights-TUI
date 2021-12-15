import sys
import datetime
from typing import Callable, Any, Tuple

import requests as requests
from valid8 import ValidationError, validate

from air_company.menu import Menu, Description, Entry
from air_company.domain import AirCompany, Ticket, Name, Surname, Departure, Destination, Price, DepartureDateTime, \
    TimeFlight, Author

api_server = 'http://localhost:8000/api/v1'


class App:
    __key = None
    __idUser = None

    def __first_menu(self):
        self.__first_menu = Menu.Builder(Description('Reservation Flights Login'), auto_select=lambda: print("Hi!")) \
            .with_entry(Entry.create('1', 'Login', is_logged=lambda: self.login())) \
            .with_entry(Entry.create('2', 'Sign in', on_selected=lambda: self.registration())) \
            .with_entry(Entry.create('0', 'Exit', on_selected=lambda: print('Bye!'), is_exit=True)) \
            .build()

    def __secondary_menu(self):
        self.__secondary_menu = Menu.Builder(Description('Reservation Flights Home'), auto_select=lambda: self.__print_tickets()) \
            .with_entry(Entry.create('1', 'Add ticket', on_selected=lambda: self.__add_ticket())) \
            .with_entry(Entry.create('2', 'Remove ticket', on_selected=lambda: self.__remove_ticket())) \
            .with_entry(Entry.create('3', 'Update ticket', on_selected=lambda: self.__update_ticket())) \
            .with_entry(Entry.create('4', 'Sort by departure date', on_selected=lambda: self.__sort_by_departure_date_time())) \
            .with_entry(Entry.create('5', 'Sort by price', on_selected=lambda: self.__sort_by_price())) \
            .with_entry(Entry.create('0', 'Logout', on_selected=lambda: self.logout(), is_exit=True)) \
            .build()

    def __init__(self):
        self.__first_menu()
        self.__secondary_menu()
        self.__airCompany = AirCompany()

    def __print_tickets(self) -> None:
        print_sep = lambda: print('-' * 140)
        print_sep()
        fmt1 = '%1s %4s %10s %15s %20s %20s %9s %25s %15s'
        fmt2 = '%1s %4s %14s %15s %20s %15s %12s %25s %13s'
        print(fmt1 % (
            '#', 'AUTHOR', 'NAME', 'SURNAME', 'DEPARTURE', 'DESTINATION', 'PRICE', 'DEPARTURE_DATE_TIME',
            'TIME_FLIGHT'))
        print_sep()
        for index in range(self.__airCompany.tickets()):
            ticket = self.__airCompany.ticket(index)
            print(fmt2 % (
                index + 1, ticket.author.value, ticket.name.value, ticket.surname.value, ticket.departure.value,
                ticket.destination.value, ticket.price, ticket.departureDateTime.value, ticket.timeFlight.value))
        print_sep()

    def login(self):
        username = input('Username: ')
        password = input('Password: ')

        res = requests.post(url=f'{api_server}/auth/login/', data={'username': username, 'password': password})
        if res.status_code != 200:
            print('Wrong Credentials!')
            return False
        json = res.json()
        self.__key = json['key']
        resGetId = requests.get(url=f'{api_server}/tickets/idUserLogged/{username}', headers={'Authorization': f'Token {self.__key}'})
        json = resGetId.json()
        self.__idUser = json['id']
        return True

    def registration(self):
        username = input('Username: ')
        email = input("Email: ")
        password = input('Password: ')
        password2 = input('Ripeti Password: ')

        res = requests.post(url=f'{api_server}/auth/registration/', data={'username': username, 'email': email, 'password1': password, 'password2': password2})
        if res.status_code == 400:
            print('Something went wrong')

    def __add_ticket(self) -> None:
        name, surname, departure, destination, price, departureDateTime, timeFlight = self.__read_ticket()
        obj = {
            "author": self.__idUser,
            "name": str(name),
            "surname": str(surname),
            "departure": str(departure),
            "destination": str(destination),
            "price": str(price),
            "departureDateTime": str(departureDateTime),
            "timeFlight": str(timeFlight)
        }
        res = requests.post(url=f'{api_server}/tickets/', json=obj, headers={'Authorization': f'Token {self.__key}'})
        self.__airCompany.clear()
        self.fetch_tickets()
        print('Ticket added!')

    def __remove_ticket(self) -> None:
        def builder(value: str) -> int:
            validate('value', int(value), min_value=0, max_value=self.__airCompany.tickets())
            return int(value)

        index = self.__read('Index (0 to cancel)', builder)
        if index == 0:
            print('Cancelled!')
            return

        to_delete = self.__airCompany.ticket(index - 1)
        res = requests.delete(url=f'{api_server}/tickets/{to_delete.id}/', headers={'Authorization': f'Token {self.__key}'})
        if res.status_code == 403:
            print("You are not authorized to delete this ticket")
        else:
            self.__airCompany.clear()
            self.fetch_tickets()
            print('Ticket removed!')

    def __update_ticket(self) -> None:
        def builder(value: str) -> int:
            validate('value', int(value), min_value=0, max_value=self.__airCompany.tickets())
            return int(value)
        index = self.__read('Index (0 to cancel)', builder)
        if index == 0:
            print('Cancelled!')
            return
        to_update = self.__airCompany.ticket(index - 1)
        name, surname, departure, destination, price, departureDateTime, timeFlight = self.__read_ticket()
        obj = {
            "id": to_update.id,
            "author": self.__idUser,
            "name": str(name),
            "surname": str(surname),
            "departure": str(departure),
            "destination": str(destination),
            "price": str(price),
            "departureDateTime": str(departureDateTime),
            "timeFlight": str(timeFlight)
        }
        res = requests.put(url=f'{api_server}/tickets/{to_update.id}/', json=obj, headers={'Authorization': f'Token {self.__key}'})
        if res.status_code == 403:
            print("You are not authorized to update this ticket")
        else:
            self.__airCompany.clear()
            self.fetch_tickets()
            print('Ticket updated!')

    def __sort_by_departure_date_time(self) -> None:
        self.__airCompany.sort_by_departure_date()

    def __sort_by_price(self) -> None:
        self.__airCompany.sort_by_price()

    def fetch_tickets(self):
        res = requests.get(url=f'{api_server}/tickets/', headers={'Authorization': f'Token {self.__key}'})
        if res.status_code != 200:
            return None

        json = res.json()
        for item in json:
            id = int(item['id'])
            author = Author(item['author'])
            name = Name(item['name'])
            surname = Surname(item['surname'])
            departure = Departure(item['departure'])
            destination = Destination(item['destination'])
            price = Price.parse(item['price'])
            departureDateTime = DepartureDateTime(datetime.datetime.strptime(item['departureDateTime'], '%Y-%m-%dT%H:%M:%SZ'))
            timeFlight = TimeFlight(datetime.datetime.strptime(item['timeFlight'], '%H:%M:%S').time())

            self.__airCompany.add_ticket(
                Ticket(id, author, name, surname, departure, destination, price, departureDateTime, timeFlight))

        return res.json()

    def __run(self) -> None:
        welcome()
        while not self.__first_menu.run() == (True, False):
            if self.__key is None:
                error_message()
            self.fetch_tickets()
            self.__secondary_menu.run()
        goodbye()

    def run(self) -> None:
        try:
            self.__run()
        except:
            print('Panic error!', file=sys.stderr)

    @staticmethod
    def __read(prompt: str, builder: Callable) -> Any:
        while True:
            try:
                line = input(f'{prompt}: ')
                if prompt == "DepartureDateTime":
                    line = datetime.datetime.strptime(line, '%d/%m/%Y %H:%M')
                    res = builder(line)
                    return res
                elif prompt == "TimeFlight":
                    line = datetime.datetime.strptime(line, '%H:%M').time()
                    res = builder(line)
                    return res
                else:
                    res = builder(line.strip())
                    return res
            except (TypeError, ValueError, ValidationError) as e:
                print(e)

    def __read_ticket(self) -> Tuple[Name, Surname, Departure, Destination, Price, DepartureDateTime, TimeFlight]:
        name = self.__read('Name', Name)
        surname = self.__read('Surname', Surname)
        departure = self.__read('Departure', Departure)
        destination = self.__read('Destination', Destination)
        price = self.__read('Price', Price.parse)
        departureDateTime = self.__read('DepartureDateTime', DepartureDateTime)
        timeFlight = self.__read('TimeFlight', TimeFlight)

        return name, surname, departure, destination, price, departureDateTime, timeFlight

    def logout(self):
        res = requests.post(url=f'{api_server}/auth/logout/', headers={'Authorization': f'Token {self.__key}'})
        print('Logged out!')
        print()
        self.__key = None
        self.__airCompany.clear()


def main(name: str):
    if name == '__main__':
        App().run()


def welcome():
    print(
        '================================================================================= ReservationFlights TUI ===============================================================================')
    print(
        '========================================================================== Because we love the \'80s so much! =========================================================================')
    print(
        '=======================================================================================================================================================================================\n')


def error_message():
    print('Unable to retrieve tickets at the moment. Please, try in a few minutes.')
    exit()


def goodbye():
    print('It was nice to have your here. Have a nice day!\n')


main(__name__)
