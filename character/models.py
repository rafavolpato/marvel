from django.db import models


class Character(models.Model):
    character_id = models.IntegerField(blank=False, null=False)
    name = models.TextField(blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    picture = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    @staticmethod
    def get_picture_from_thumbnail(thumbnail):
        if thumbnail:
            return f"{thumbnail['path']}.{thumbnail['extension']}"
        return ""
