import json


from django.test import TestCase
from django.urls import reverse

from character.models import Character
from character.tests.data.characters import CHARACTERS
from character.tests.data.characters import SPECTRUM_CHARACTER

APPLICATION_JSON = "application/json"


class BaseTestCase(TestCase):
    def assert_resp(self, resp, status):
        self.assertEqual(resp.status_code, status)

    def assert_json(self, resp, status):
        self.assert_resp(resp, status)
        self.assertEqual(resp["content-type"], APPLICATION_JSON)

    @staticmethod
    def create_spectrum():
        character_data = {
            "character_id": SPECTRUM_CHARACTER["id"],
            "name": SPECTRUM_CHARACTER["name"],
            "description": SPECTRUM_CHARACTER["description"],
            "picture": f"{SPECTRUM_CHARACTER['thumbnail']['path']}.{SPECTRUM_CHARACTER['thumbnail']['extension']}",
        }
        return Character.objects.create(**character_data)

    @staticmethod
    def create_characters():
        for character in CHARACTERS:
            character_data = {
                "character_id": character["id"],
                "name": character["name"],
                "description": character["description"],
                "picture": f"{character['thumbnail']['path']}.{character['thumbnail']['extension']}",
            }
            Character.objects.create(**character_data)


class TestCharacterView(BaseTestCase):
    def compare_characters(self, character_marvel, character_db):
        self.assertEqual(character_marvel["id"], character_db["character_id"])
        self.assertEqual(character_marvel["name"], character_db["name"])
        self.assertEqual(character_marvel["description"], character_db["description"])
        self.assertEqual(
            Character.get_picture_from_thumbnail(character_marvel["thumbnail"]),
            character_db["picture"],
        )

    def test_list_character(self):
        self.create_characters()
        url = reverse("character-list")
        resp = self.client.get(url)
        self.assert_json(resp, 200)
        for character in resp.data:
            character_found = [
                row for row in CHARACTERS if row["id"] == character["character_id"]
            ][0]
            self.compare_characters(character_found, character)

    def test_get_character(self):
        character = self.create_spectrum()
        url = reverse("character-detail", args=(character.id,))
        resp = self.client.get(url)
        self.assert_json(resp, 200)

        character = resp.data
        self.compare_characters(SPECTRUM_CHARACTER, character)
