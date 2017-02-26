# coding=utf-8
class VKObject(object):

    def __repr__(self):
        return u"<{0} id{1}>".format(self.__class__.__name__, self.id)
