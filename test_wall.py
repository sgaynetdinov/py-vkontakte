# coding=utf-8
from __future__ import unicode_literals

import unittest
from vk.wall import Wall


class WallObjectTest(unittest.TestCase):
    def setUp(self):
        self.wall_dict = {
            "id": 340393,
            "from_id": -1,
            "owner_id": -1,
            "date": 1466181337,
            "marked_as_ads": 1,
            "post_type": 'post',
            "text": '',
            "copy_history": [{
                "id": 19972,
                "owner_id": -19542789,
                "from_id": -19542789,
                "date": 1466082642,
                "post_type": 'post',
                "text": '''Упростите получение обратной связи, добавив на свой сайт виджет «Напишите нам». С его помощью ваши клиенты смогут быстро связаться с вами через сообщения ВКонтакте и задать любой интересующий вопрос.

Кроме того, при помощи ссылки вида vk.me/[короткий адрес вашей страницы или сообщества] у вас всегда есть возможность поделиться вашим контактом через продвижение записей ВКонтакте, а у пользователей — оперативно уточнить цену или проконсультироваться об услугах.

Подробнее о нововведении читайте в блоге ВКонтакте: new.vk.com/blog/vkme.''',
                "attachments": [{
                    "type": 'link',
                    "link": {
                        "url": '"http"://new.vk.com/blog/vkme',
                        "title": 'VK.me — быстрый доступ к обмену сообщениями',
                        "caption": 'new.vk.com',
                        "description": 'ВКонтакте представляет короткий адрес для сообщений — vk.me. Теперь написать сообщение другу или задать вопрос компании стало ещё проще — по прямой ссылке можно сразу попасть в диалог или поделиться ей с другими.',
                        "photo": {
                            "id": 420804501,
                            "album_id": -2,
                            "owner_id": 6291322,
                            "photo_75": '"https"://pp.vk.me/...bea/pPdnQ6-zZG8.jpg',
                            "photo_130": '"https"://pp.vk.me/...beb/vgQtNi0PVKU.jpg',
                            "photo_604": '"https"://pp.vk.me/...bec/LE_Cv5sLaC4.jpg',
                            "width": 150,
                            "height": 52,
                            "text": '',
                            "date": 1466063017
                        },
                        "is_external": 1
                    }
                }],
                "post_source": {
                    "type": 'vk'
                }
            }],
            "can_delete": 1,
            "can_pin": 1,
            "post_source": {
                "type": 'vk'
            },
            "comments": {
                "count": 0,
                "can_post": 0
            },
            "likes": {
                "count": 65,
                "user_likes": 0,
                "can_like": 1,
                "can_publish": 1
            },
            "reposts": {
                "count": 7,
                "user_reposted": 0
            }
        }

    def test_create_wall_object(self):
        wall = Wall(self.wall_dict)
        self.assertEqual(wall.id, self.wall_dict.get("id"))
        self.assertEqual(wall.owner_id, self.wall_dict.get("owner_id"))
        self.assertEqual(wall.from_id, self.wall_dict.get("from_id"))
        self.assertEqual(wall.date, self.wall_dict.get("date"))
        self.assertEqual(wall.text, self.wall_dict.get("text"))
        self.assertEqual(wall.reply_owner_id, self.wall_dict.get("reply_owner_id"))
        self.assertEqual(wall.reply_post_id, self.wall_dict.get("reply_post_id"))
        self.assertEqual(wall.friends_only, self.wall_dict.get("friends_only"))
        self.assertEqual(wall.comments_count, self.wall_dict.get("comments_count"))
        self.assertEqual(wall.likes_count, self.wall_dict.get("likes_count"))
        self.assertEqual(wall.reposts_count, self.wall_dict.get("reposts_count"))
        self.assertEqual(wall.post_type, self.wall_dict.get("post_type"))
        self.assertEqual(wall.is_pinned, self.wall_dict.get("is_pinned"))


if __name__ == "__main__":
    unittest.main()
