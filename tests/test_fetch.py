import vk


def test_url_open(mocker):
    mocker.patch('vk.fetch.urlopen')

    mock_json = mocker.patch('json.load')
    mock_json.return_value = {'response': [{
      "id": 1,
      "first_name": "Павел",
      "last_name": "Дуров",
      "domain": "durov",
    }]}

    api = vk.Api('TOKEN')
    user = api.get_user('durov')

    assert user.domain == 'durov'
