# coding=utf-8
from .base import VKObject
from .fetch import fetch


class Poll(VKObject):
    """
    https://vk.com/dev/objects/poll
    """
    __slots__ = ('id', 'type', 'owner_id', 'unixtime', 'question', 'count_votes', 'answers', 'is_anonymous')

    @classmethod
    def from_json(cls, poll_json):
        poll = cls()
        poll.id = poll_json.get("id")
        poll.type = "poll"
        poll.owner_id = poll_json.get("owner_id")
        poll.unixtime = poll_json.get("created")
        poll.question = poll_json.get("question")
        poll.count_votes = poll_json.get("votes")
        poll.answers = PollAnswer.get_answers(poll_json.get("answers"), poll.owner_id, poll.id)
        poll.is_anonymous = bool(poll_json.get("anonymous"))
        return poll


class PollAnswer(VKObject):
    __slots__ = ('id', 'text', 'count_votes', 'rate', 'users')

    @classmethod
    def from_json(cls, answer_json):
        answer = cls()
        answer.id = answer_json.get('id')
        answer.text = answer_json.get('text')
        answer.count_votes = answer_json.get('votes')
        answer.rate = answer_json.get('rate')
        answer.users = cls._get_voters(answer_json.get('owner_id'), answer_json.get('poll_id'), answer.id)
        return answer

    @classmethod
    def get_answers(cls, answer_json_items, owner_id, poll_id):
        _answer_items = []
        for answer_json in answer_json_items:
            answer_json.update({
                'owner_id': owner_id,
                'poll_id': poll_id
            })
            _answer_items.append(cls.from_json(answer_json))
        return _answer_items

    @classmethod
    def _get_voters(cls, owner_id, poll_id, answer_id):
        """
        https://vk.com/dev/polls.getVoters
        """
        response = fetch("polls.getVoters", owner_id=owner_id, poll_id=poll_id, answer_ids=answer_id)
        user_items = response[0].get("users").get("items")
        for user in user_items:
            yield user
