# coding=utf-8
class VKObject(object):

    def __repr__(self):
        if hasattr(self, 'screen_name'):
            vkobject_title = self.screen_name
        else:
            vkobject_title = "id{0}".format(self.id)
        return u"<{0}: {1}>".format(self.__class__.__name__, vkobject_title)
