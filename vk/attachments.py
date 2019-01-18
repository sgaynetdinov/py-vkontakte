from .photos import Photo
from .polls import Poll


def get_attachments(session, attachments_json):
    if not attachments_json:
        return None

    attachment_items = []

    for attachment_json in attachments_json:
        _attachments_type = attachment_json.get("type")

        if _attachments_type == "photo":
            attachment_items.append(Photo.from_json(session, attachment_json.get("photo")))

        elif _attachments_type == "poll":
            attachment_items.append(Poll.from_json(session, attachment_json.get("poll")))

    return attachment_items
