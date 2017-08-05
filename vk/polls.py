# coding=utf-8
from .base import VKBase


class Poll(VKBase):
    """
    https://vk.com/dev/objects/poll
    """
    __slots__ = ('id', 'type', 'owner_id', 'unixtime', 'question', 'count_votes', 'answers', 'is_anonymous', '_session')

    @classmethod
    def from_json(cls, session, poll_json):
        poll = cls()
        poll.id = poll_json.get("id")
        poll.type = "poll"
        poll.owner_id = poll_json.get("owner_id")
        poll.unixtime = poll_json.get("created")
        poll.question = poll_json.get("question")
        poll.count_votes = poll_json.get("votes")
        poll.answers = PollAnswer.get_answers(session, poll_json.get("answers"), poll.owner_id, poll.id)
        poll.is_anonymous = bool(poll_json.get("anonymous"))
        poll._session = session
        return poll


class PollAnswer(VKBase):
    __slots__ = ('id', 'text', 'count_votes', 'rate', 'users', '_session')

    @classmethod
    def from_json(cls, session, answer_json):
        answer = cls()
        answer.id = answer_json.get('id')
        answer.text = answer_json.get('text')
        answer.count_votes = answer_json.get('votes')
        answer.rate = answer_json.get('rate')
        answer.users = cls._get_voters(session, answer_json.get('owner_id'), answer_json.get('poll_id'), answer.id)
        answer._session = session
        return answer

    @classmethod
    def get_answers(cls, session, answer_json_items, owner_id, poll_id):
        _answer_items = []
        for answer_json in answer_json_items:
            answer_json.update({
                'owner_id': owner_id,
                'poll_id': poll_id
            })
            _answer_items.append(cls.from_json(session, answer_json))
        return _answer_items

    @classmethod
    def _get_voters(cls, session, owner_id, poll_id, answer_id):
        """
        https://vk.com/dev/polls.getVoters
        """
        from .users import User

        return session.fetch_items("polls.getVoters", User._get_users, count=100, owner_id=owner_id, poll_id=poll_id, answer_ids=answer_id)
