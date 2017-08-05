# coding=utf-8
class VKObject(object):

    def __repr__(self):
        if hasattr(self, 'screen_name'):
            vkobject_title = self.screen_name
        elif hasattr(self, 'id'):
            vkobject_title = "id{0}".format(self.id)
        else:
            vkobject_title = ''

        return u"<{0}: {1}>".format(self.__class__.__name__, vkobject_title)

    def __hash__(self):
        class_name = type(self).__name__
        return hash(class_name) ^ hash(self.id)

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return hash(self) == hash(other)
        raise NotImplementedError
