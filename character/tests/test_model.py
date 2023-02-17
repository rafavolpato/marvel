from django.test import TestCase

from character.models import Character


class CharacterModelTests(TestCase):
    def setUp(self):
        self.character_test = Character.objects.create(
            character_id=1,
            name="test",
            description="test description",
            picture="test.jpg"
        )

    def test_character_str_method(self):
        self.assertEqual(str(self.character_test), "test")

    def test_get_picture_from_thumbnail_method(self):
        thumbnail = {
            "path": "path/to/image",
            "extension": "jpg"
        }
        self.assertEqual(Character.get_picture_from_thumbnail(thumbnail), "path/to/image.jpg")
