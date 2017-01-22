# coding=utf-8
def get_attachments(attachments_json):
    if not attachments_json:
        return None

    attachment_items = []

    for attachment_json in attachments_json:
        if attachment_json.get("type") == "photo":
            attachment_items.append(AttachmentPhoto.from_json(attachment_json.get("photo")))

    return attachment_items


class AttachmentPhoto(object):
    __slots__ = ("id", "album_id", "owner_id", "user_id", "text", "type", "unixtime", "photo_75", "photo_130", "photo_604", "photo_807", "photo_1280",
                 "photo_2560")

    @classmethod
    def from_json(cls, attachment_json):
        attachment = cls()
        attachment.id = attachment_json.get("id")
        attachment.album_id = attachment_json.get("album_id")
        attachment.owner_id = attachment_json.get("owner_id")
        attachment.user_id = attachment_json.get("user_id")
        attachment.text = attachment_json.get("text")
        attachment.type = attachment_json.get("type")
        attachment.unixtime = attachment_json.get("date")
        attachment.photo_75 = attachment_json.get("photo_75")
        attachment.photo_130 = attachment_json.get("photo_130")
        attachment.photo_604 = attachment_json.get("photo_604")
        attachment.photo_807 = attachment_json.get("photo_807")
        attachment.photo_1280 = attachment_json.get("photo_1280")
        attachment.photo_2560 = attachment_json.get("photo_2560")
        return attachment

    def __repr__(self):
        return u"<AttachmentPhoto: id{0}>".format(self.id)
