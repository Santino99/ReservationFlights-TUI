from unittest.mock import patch, Mock

from air_company.app import App


def mock_response_dict(status_code, data={}):
    res = Mock()
    res.status_code = status_code
    res.json.return_value = data
    return res


def mock_response(status_code, data={}):
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


@patch('requests.post', side_effect=[mock_response_dict(200, {'key': '12e1abb2447d2b994bc8d7350645e1df7624c32'}),
                                     mock_response_dict(200),
                                     mock_response_dict(200),])
@patch('builtins.input', side_effect=['1', 'Iorio', 'massimo99', '1', 'Pietro', 'Cofone',
                                      'Lamezia Terme', 'Torino', '50', '03/02/22 19:30', '01:00'])
@patch('builtins.print')
def test_add_ticket(mocked_print, mocked_input, mocked_requests_post):
    with patch('builtins.open'):
        App().run()
    mocked_input.assert_called()
    mocked_requests_post.assert_called()
    mocked_print.assert_any_call('Ticket added!')

