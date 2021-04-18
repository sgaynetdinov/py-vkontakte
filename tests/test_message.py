import pytest

from vk.messages import Message

message_json = {
    "id": 18000,
    "date": 621734400,
    "out": 1,
    "user_id": -151808000,
    "read_state": 1,
    "title": "",
    "body": "Hello world",
    "random_id": 597248445,
}


def test_message(factory):
    message = Message.from_json(None, message_json)

    assert isinstance(message, Message)
    assert message.date == 621734400
    assert message.id == 18000
    assert message.out == 1
    assert message.body == "Hello world"
    assert message.random_id == 597248445
    assert message.update_time is None

@pytest.mark.parametrize('update_time, expected', [
    (None, None),
    (100500, 100500),
])
def test_is_updated(update_time, expected):
    message_json['update_time'] = update_time
    message = Message.from_json(None, message_json)

    assert message.update_time == expected 
