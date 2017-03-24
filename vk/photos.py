# coding: utf-8
from .base import VKObject
from .fetch import fetch


class Photo(VKObject):

    @classmethod
    def get_owner_cover_photo_upload_server(cls, group_id, crop_x=0, crop_y=0, crop_x2=795, crop_y2=200):
        """
        https://vk.com/dev/photos.getOwnerCoverPhotoUploadServer
        """
        group_id = abs(group_id)
        response = fetch("photos.getOwnerCoverPhotoUploadServer", group_id=group_id, crop_x=crop_x, crop_y=crop_y, crop_x2=crop_x2, crop_y2=crop_y2)
        return response['upload_url']

    @classmethod
    def save_owner_cover_photo(cls, hash, photo):
        """
        https://vk.com/dev/photos.saveOwnerCoverPhoto
        """
        response = fetch('photos.saveOwnerCoverPhoto', hash=hash, photo=photo)
        return response
