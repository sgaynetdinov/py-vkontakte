class VKBase:

    def __repr__(self):
        if hasattr(self, 'screen_name'):
            object_title = self.screen_name
        elif hasattr(self, 'id'):
            object_title = "id{0}".format(self.id)
        else:
            object_title = ''

        return u"<{0}: {1}>".format(self.__class__.__name__, object_title)

    def __hash__(self):
        class_name = type(self).__name__
        return hash(class_name) ^ hash(self.id)

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return hash(self) == hash(other)
        raise NotImplementedError
