from smhi.smhi import SmhiParser
from unittest.mock import patch

def test_check_connection():
    parser = SmhiParser()
    assert 200 == parser.check_connection()


@patch('smhi.smhi.SmhiParser._make_request')
def test_list_parameters_mocked(mock_make_request):
    mock_response = {
        'resource': [
            {'key': '1', 'title': 'param1', 'summary': 'sum1'},
            {'key': '2', 'title': 'param2', 'summary': 'sum2'},
            {'key': '3', 'title': 'param3', 'summary': 'sum3'}
        ]
    }
    mock_make_request.return_value.json.return_value = mock_response
    parser = SmhiParser()
    with patch('builtins.print') as mocked_print:
        parser.list_parameters()

        mocked_print.assert_any_call("1, param1 (sum1)")
        mocked_print.assert_any_call("2, param2 (sum2)")
        mocked_print.assert_any_call("3, param3 (sum3)")

@patch('smhi.smhi.SmhiParser._make_request')
def test_temperatures_mocked(mock_make_request):
    mock_response_stations = {
        'station': [
            {'key': 'station_1', 'name': 'Station One'},
            {'key': 'station_2', 'name': 'Station Two'},
            {'key': 'station_3', 'name': 'Station Three'}
        ]
    }
    mock_make_request.return_value.json.side_effect = [mock_response_stations,
                                                    {'station': {'name': 'Station One'}, 'value': [{'value': '1.1'}]},
                                                    {'station': {'name': 'Station Two'}, 'value': [{'value': '-1.1'}]},
                                                    {'station': {'name': 'Station Three'}, 'value': [{'value': '-1.2'}]}]
    parser = SmhiParser()
    with patch('builtins.print') as mocked_print:
        parser.temperatures()

        mocked_print.assert_any_call("Highest temperature: Station One, 1.1 degrees")
        mocked_print.assert_any_call("Lowest temperature: Station Three, -1.2 degrees")

def test_temperatures(capsys):
    parser = SmhiParser()
    parser.temperatures()
    captured = capsys.readouterr()
    assert captured.out.strip()[0:21] == "Highest temperature: "