import io

import vk
from vk.fetch import Session


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


def test_upload_photo():
    file_obj = io.BytesIO(b'Python developer and blogger.')
    data, boundary = Session()._file_upload(file_obj)

    assert b'Content-Disposition: file; name="photo"; filename="photo.jpg"' in data
    assert b'Content-Type: application/octet-stream' in data
    assert b'Python developer and blogger.' in data
    assert boundary.encode() in data
