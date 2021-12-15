from unittest.mock import patch, Mock

from air_company.app import App


def mock_response_dict(status_code, data={}):
    res = Mock()
    res.status_code = status_code
    res.json.return_value = data
    return res


@patch('builtins.input', side_effect=['0'])
@patch('builtins.print')
def test_exit(mocked_print, mocked_input):
    with patch('builtins.open'):
        App().run()
    mocked_print.assert_any_call('Bye!')
    mocked_print.assert_any_call('It was nice to have your here. Have a nice day!\n')
    mocked_input.assert_called()


@patch('requests.post', side_effect=[mock_response_dict(400)])
@patch('builtins.input', side_effect=['1', 'Santino', 'Locanto'])
@patch('builtins.print')
def test_wrong_credentials(mocked_print, mocked_input, mocked_requests_post):
    with patch('builtins.open'):
        App().run()
    mocked_requests_post.assert_called()
    mocked_print.assert_any_call('Wrong Credentials!')
    mocked_input.assert_called()


@patch('requests.post', side_effect=[mock_response_dict(400)])
@patch('builtins.input', side_effect=['2', 'Iorio', 'pio@example.com', 'massimo99', 'massimo99'])
@patch('builtins.print')
def test_user_already_registered(mocked_print, mocked_input, mocked_requests_post):
    with patch('builtins.open'):
        App().run()
    mocked_requests_post.assert_called()
    mocked_print.assert_any_call('Something went wrong')
    mocked_input.assert_called()


@patch('requests.post', side_effect=[mock_response_dict(200, {'key': 'dd72faf5a81fea7e7304a3de632aa1a9eb1ec250'}),
                                     mock_response_dict(200)])
@patch('builtins.input', side_effect=['1', 'Iorio', 'massimo99', '1', 'Pietro', 'Cofone',
                                      'Lamezia Terme', 'Torino', '50', '03/02/22 19:30', '01:00'])
@patch('builtins.print')
def test_add_ticket(mocked_print, mocked_input, mocked_requests_post):
    with patch('builtins.open'):
        App().run()
    mocked_input.assert_called()
    mocked_requests_post.assert_called()
    mocked_print.assert_any_call('Ticket added!')


@patch('requests.post', side_effect=[mock_response_dict(200, {'key': 'dd72faf5a81fea7e7304a3de632aa1a9eb1ec250'})])
@patch('requests.delete', side_effect=[mock_response_dict(204)])
@patch('builtins.input', side_effect=['1', 'Iorio', 'massimo99', '2', '1'])
@patch('builtins.print')
def test_remove_ticket(mocked_print, mocked_input, mocked_requests_delete, mocked_requests_post):
    with patch('builtins.open'):
        App().run()
    mocked_input.assert_called()
    mocked_requests_delete.assert_called()
    mocked_requests_post.assert_called()
    mocked_print.assert_any_call('Ticket removed!')


@patch('requests.post', side_effect=[mock_response_dict(200, {'key': 'dd72faf5a81fea7e7304a3de632aa1a9eb1ec250'})])
@patch('builtins.input', side_effect=['1', 'Iorio', 'massimo99', '2', '0'])
@patch('builtins.print')
def test_remove_ticket_cancelled(mocked_print, mocked_input, mocked_requests_post):
    with patch('builtins.open'):
        App().run()
    mocked_input.assert_called()
    mocked_requests_post.assert_called()
    mocked_print.assert_any_call('Cancelled!')


@patch('requests.post', side_effect=[mock_response_dict(200, {'key': 'dd72faf5a81fea7e7304a3de632aa1a9eb1ec250'})])
@patch('builtins.input', side_effect=['1', 'Iorio', 'massimo99', '3', '1', 'Santino', 'Locanto',
                                      'Genova', 'Verona', '50', '03/02/22 19:30', '01:00'])
@patch('requests.put', side_effect=[mock_response_dict(200)])
@patch('builtins.print')
def test_update_ticket(mocked_print, mocked_input, mocked_requests_post, mocked_requests_put):
    with patch('builtins.open'):
        App().run()
    mocked_requests_post.assert_called()
    mocked_input.assert_called()
    mocked_requests_put.assert_called()
    mocked_print.assert_any_call('Ticket updated!')


@patch('requests.post', side_effect=[mock_response_dict(200, {'key': 'dd72faf5a81fea7e7304a3de632aa1a9eb1ec250'})])
@patch('builtins.input', side_effect=['1', 'Iorio', 'massimo99', '3', '0'])
@patch('builtins.print')
def test_update_ticket_cancelled(mocked_print, mocked_input, mocked_requests_post):
    with patch('builtins.open'):
        App().run()
    mocked_requests_post.assert_called()
    mocked_input.assert_called()
    mocked_print.assert_any_call('Cancelled!')


@patch('requests.post', side_effect=[mock_response_dict(200, {'key': 'dd72faf5a81fea7e7304a3de632aa1a9eb1ec250'})])
@patch('builtins.input', side_effect=['1', 'Iorio', 'massimo99', '4'])
def test_sort_by_departure_date(mocked_input, mocked_requests_post):
    with patch('builtins.open'):
        App().run()
    mocked_requests_post.assert_called()
    mocked_input.assert_called()


@patch('requests.post', side_effect=[mock_response_dict(200, {'key': 'dd72faf5a81fea7e7304a3de632aa1a9eb1ec250'})])
@patch('builtins.input', side_effect=['1', 'Iorio', 'massimo99', '5'])
def test_sort_by_price(mocked_input, mocked_requests_post):
    with patch('builtins.open'):
        App().run()
    mocked_requests_post.assert_called()
    mocked_input.assert_called()


@patch('requests.post', side_effect=[mock_response_dict(200, {'key': 'dd72faf5a81fea7e7304a3de632aa1a9eb1ec250'}),
                                     mock_response_dict(200)])
@patch('requests.get', side_effect=[mock_response_dict(200, {'id': 2}),
                                    mock_response_dict(200, [{'id': 1,
                                                         'author': 2,
                                                         'name': 'Marco',
                                                         'surname': 'Bianchi',
                                                         'departure': 'Torino',
                                                         'destination': 'Ancona',
                                                         'price': '46.78',
                                                         'departureDateTime': '"23-12-26T12:12:12Z',
                                                         'timeFlight': "01:00:00"}])])
@patch('builtins.input', side_effect=['1', 'Iorio', 'massimo99'])
def test_fetch(mocked_input, mocked_requests_get, mocked_requests_post):
    with patch('builtins.open'):
        App().run()
    mocked_input.assert_called()
    mocked_requests_post.assert_called()
    mocked_requests_get.assert_called_with(url='http://localhost:8000/api/v1/tickets/', headers={'Authorization': 'Token dd72faf5a81fea7e7304a3de632aa1a9eb1ec250'})


@patch('requests.post', side_effect=[mock_response_dict(200, {'key': 'dd72faf5a81fea7e7304a3de632aa1a9eb1ec250'}),
                                     mock_response_dict(200)])
@patch('builtins.input', side_effect=['1', 'Iorio', 'massimo99', '0'])
@patch('builtins.print')
def test_logout(mocked_print, mocked_input, mocked_requests_post):
    with patch('builtins.open'):
        App().run()
    mocked_requests_post.assert_called()
    mocked_input.assert_called()
    mocked_print.assert_any_call("Logged out!")
