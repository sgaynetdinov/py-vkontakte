# coding: utf-8
from .base import VKObject
from .fetch import fetch, fetch_post


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

    @classmethod
    def get_wall_upload_server(cls, group_id):
        """
        https://vk.com/dev/photos.getWallUploadServer
        """
        response = fetch("photos.getWallUploadServer", group_id=group_id)
        return response['upload_url']

    @classmethod
    def get_save_wall_photo(cls, photo, server, hash, user_id=None, group_id=None):
        """
        https://vk.com/dev/photos.saveWallPhoto
        """
        if group_id < 0:
            group_id = abs(group_id)

        response = fetch("photos.saveWallPhoto", photo=photo, server=server, hash=hash, user_id=user_id, group_id=group_id)[0]
        return response['id'], response['owner_id']

    @classmethod
    def upload_wall_photos_for_group(cls, group_id, image_files):
        upload_url = cls.get_wall_upload_server(group_id)

        attachments = []
        for image_fd in image_files:
            response = fetch_post(upload_url, files={'photo': image_fd})
            response_json = response.json()
            photo, server, _hash = response_json['photo'], response_json['server'], response_json['hash']
            photo_id, owner_id = cls.get_save_wall_photo(photo, server, _hash, group_id=group_id)
            attachments.append("photo{0}_{1}".format(owner_id, photo_id))

        return ",".join(attachments)
