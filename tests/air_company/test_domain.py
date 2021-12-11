import datetime
from datetime import timedelta
import pytest
from valid8 import ValidationError

from air_company.domain import Name, Surname, Departure, Destination, Price, DepartureDateTime, Author, TimeFlight, AirCompany, Ticket


# Test author format and __str__

def test_author_str():
    assert str(Author(7)) == '7'


def test_name_format():
    wrong_values = ['', 'a#bcde', '-@#', 'ABCDE', 'A' * 51, 'Massimo pio Nicola']
    for value in wrong_values:
        with pytest.raises(ValidationError):
            Name(value)

    correct_values = ['Giovanni', 'Santino', 'Massimo Pio Nicola']
    for value in correct_values:
        assert Name(value).value == value


def test_name_str():
    for value in ['Giovanni', 'Davide', 'Massimo Pio Nicola']:
        assert str(Name(value)) == value


def test_surname_format():
    wrong_values = ['', 'a#bcde', '-@#', 'ABCDE', 'A' * 51, 'De tursi']
    for value in wrong_values:
        with pytest.raises(ValidationError):
            Surname(value)

    correct_values = ['Rotondaro', 'Locanto', 'Iorio', 'De Tursi']
    for value in correct_values:
        assert Surname(value).value == value


def test_surname_str():
    for value in ['Rotondaro', 'Locanto', 'Iorio', 'De Tursi']:
        assert str(Surname(value)) == value


def test_departure_format():
    wrong_values = ['', 'a#bcde', '-@#', 'ABCDE', 'A' * 51, 'LameziaTerme']
    for value in wrong_values:
        with pytest.raises(ValidationError):
            Departure(value)

    correct_values = ['Crotone', 'Cosenza', 'Vibo Valentia', 'Lamezia Terme']
    for value in correct_values:
        assert Departure(value).value == value


def test_departure_str():
    for value in ['Crotone', 'Cosenza', 'Vibo Valentia', 'Lamezia Terme']:
        assert str(Departure(value)) == value


def test_destination_format():
    wrong_values = ['', 'a#bcde', '-@#', 'ABCDE', 'A' * 51, 'LameziaTerme']
    for value in wrong_values:
        with pytest.raises(ValidationError):
            Departure(value)

    correct_values = ['Crotone', 'Cosenza', 'Vibo Valentia', 'Lamezia Terme']
    for value in correct_values:
        assert Departure(value).value == value


def test_destination_str():
    for value in ['Crotone', 'Cosenza', 'Vibo Valentia', 'Lamezia Terme']:
        assert str(Departure(value)) == value


def test_price_no_init():
    with pytest.raises(ValidationError):
        Price(1)


def test_price_cannot_be_negative():
    with pytest.raises(ValidationError):
        Price.create(-1, 0)


def test_price_no_cents():
    assert Price.create(1, 0) == Price.create(1)


def test_price_parse():
    assert Price.parse('10.20') == Price.create(10, 20)


def test_price_str():
    assert str(Price.create(9, 99)) == '9.99'


def test_price_euro():
    assert Price.create(14, 25).euro == 14


def test_price_cents():
    assert Price.create(14, 25).cents == 25


def test_departure_date_time_min_value():
    dateYesterday = datetime.datetime.now() - timedelta(days=1)
    with pytest.raises(ValidationError):
        DepartureDateTime(dateYesterday)

    dateTomorrow = datetime.datetime.now() + timedelta(days=1)
    assert DepartureDateTime(dateTomorrow)


def test_time_flight_min_value():
    time = datetime.time(0, 20)
    with pytest.raises(ValidationError):
        TimeFlight(time)

    time2 = datetime.time(0, 40)
    assert (TimeFlight(time2))


def test_ticket_str():
    ticket = Ticket(2, Author(2), Name("Massimo Pio"), Surname("Iorio"), Departure("Ciampino"),
                    Destination("Lamezia Terme"),
                    Price.create(15, 20), DepartureDateTime(datetime.datetime(2022, 12, 11, 17, 0)),
                    TimeFlight(datetime.time(0, 40)))

    assert str(ticket) == 'name\t surname\t departure\t destination\t price\t departureDateTime\t timeFlight\n' + str(
        ticket.name) + '\t' + str(ticket.surname) + '\t' + str(ticket.departure) + '\t' + str(ticket.destination) + '\t' + str(ticket.price) + '\t' + str(ticket.departureDateTime) + '\t' + str(ticket.timeFlight) + '\n'


@pytest.fixture
def tickets():
    return [
        Ticket(1, Author(1), Name("Santino"), Surname("Locanto"), Departure("Crotone"), Destination("Lamezia Terme"),
               Price.create(15, 20), DepartureDateTime(datetime.datetime(2022, 12, 11, 17, 0)),
               TimeFlight(datetime.time(0, 40))),
        Ticket(2, Author(2), Name("Massimo Pio"), Surname("Iorio"), Departure("Ciampino"), Destination("Lamezia Terme"),
               Price.create(15, 20), DepartureDateTime(datetime.datetime(2022, 12, 11, 17, 0)),
               TimeFlight(datetime.time(0, 40))),
        Ticket(3, Author(3), Name("Giovanni"), Surname("Rotondaro"), Departure("Scalea"), Destination("Cosenza"),
               Price.create(15, 20), DepartureDateTime(datetime.datetime(2022, 12, 11, 17, 0)),
               TimeFlight(datetime.time(0, 40)))
    ]


def test_airCompany_clear_len_add_tickets(tickets):
    airCompany = AirCompany()
    size = 0
    for ticket in tickets:
        airCompany.add_ticket(ticket)
        size += 1
        assert airCompany.tickets() == size
        assert airCompany.ticket((size - 1)) == ticket
    airCompany.clear()
    assert airCompany.tickets() == 0


def test_airCompany_remove_ticket(tickets):
    airCompany = AirCompany()
    for ticket in tickets:
        airCompany.add_ticket(ticket)

    airCompany.remove_ticket(0)
    assert airCompany.ticket(0) == tickets[1]

    with pytest.raises(ValidationError):
        airCompany.remove_ticket(-1)

    with pytest.raises(ValidationError):
        airCompany.remove_ticket(airCompany.tickets())

    while airCompany.tickets():
        airCompany.remove_ticket(0)
    assert airCompany.tickets() == 0


def test_sort_departure_date():
    airCompany = AirCompany()
    ticket = Ticket(1, Author(1), Name("Santino"), Surname("Locanto"), Departure("Crotone"),
                    Destination("Lamezia Terme"),
                    Price.create(15, 20), DepartureDateTime(datetime.datetime(2022, 12, 12, 17, 0)),
                    TimeFlight(datetime.time(0, 40)))

    airCompany.add_ticket(ticket)

    ticket2 = Ticket(2, Author(2), Name("Massimo Pio"), Surname("Iorio"), Departure("Ciampino"),
                     Destination("Lamezia Terme"),
                     Price.create(15, 20), DepartureDateTime(datetime.datetime(2022, 12, 11, 17, 0)),
                     TimeFlight(datetime.time(0, 40)))
    airCompany.add_ticket(ticket2)
    airCompany.sort_by_departure_date()

    assert airCompany.ticket(0) == ticket2


def test_sort_time_flight():
    airCompany = AirCompany()
    ticket = Ticket(1, Author(1), Name("Santino"), Surname("Locanto"), Departure("Crotone"),
                    Destination("Lamezia Terme"),
                    Price.create(15, 20), DepartureDateTime(datetime.datetime(2022, 12, 12, 17, 0)),
                    TimeFlight(datetime.time(0, 49)))
    airCompany.add_ticket(ticket)
    ticket2 = Ticket(2, Author(2), Name("Massimo Pio"), Surname("Iorio"), Departure("Ciampino"),
                     Destination("Lamezia Terme"),
                     Price.create(15, 20), DepartureDateTime(datetime.datetime(2022, 12, 11, 17, 0)),
                     TimeFlight(datetime.time(0, 50)))
    airCompany.add_ticket(ticket2)
    airCompany.sort_by_time_flight()
    assert airCompany.ticket(0) == ticket2