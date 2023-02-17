from django.test import TestCase
from unittest.mock import patch

from character.management.commands.load_characters import API_KEY
from character.models import Character
from character.management.commands.load_characters import (
    get_auth_params,
    fetch_character,
    save_character_data,
    save_spectrum_work_mates,
    Command,
)
from character.tests.data.characters import CHARACTERS
from character.tests.data.characters import SPECTRUM_CHARACTER


class MarvelApiTestLoadCharacters(TestCase):
    def setUp(self):
        self.spectrum_character = SPECTRUM_CHARACTER
        self.auth_params = {"ts": "123456789", "apikey": "myapikey", "hash": "myhash"}

    @patch("character.management.commands.load_characters.requests.get")
    def test_fetch_character(self, mock_get):
        mock_get.return_value.json.return_value = {
            "data": {"results": [self.spectrum_character]}
        }
        result = fetch_character(1010705, self.auth_params)
        self.assertIsNotNone(result)
        self.assertEqual(result, self.spectrum_character)

    def test_save_character_data(self):
        character_data = self.spectrum_character
        save_character_data(character_data)
        character = Character.objects.get(name="Spectrum")
        self.assertIsNotNone(character)
        self.assertEqual(character.character_id, 1010705)
        self.assertEqual(
            character.description, self.spectrum_character.get("description")
        )
        self.assertEqual(
            character.picture,
            Character.get_picture_from_thumbnail(
                self.spectrum_character.get("thumbnail")
            ),
        )

    @patch("character.management.commands.load_characters.fetch_comics_by_character")
    @patch("character.management.commands.load_characters.fetch_comic_characters")
    def test_save_spectrum_work_mates(
        self, mock_fetch_comic_characters, mock_fetch_comics_by_character
    ):

        mock_fetch_comic_characters.return_value = CHARACTERS
        mock_fetch_comics_by_character.return_value = CHARACTERS
        save_spectrum_work_mates(self.spectrum_character, self.auth_params)
        for character in CHARACTERS:
            character_found = Character.objects.get(name=character.get("name"))
            self.assertIsNotNone(character_found)
            self.assertEqual(character_found.character_id, character.get("id"))
            self.assertEqual(character_found.description, character.get("description"))
            self.assertEqual(character_found.name, character.get("name"))
            self.assertEqual(
                character_found.picture,
                Character.get_picture_from_thumbnail(character.get("thumbnail")),
            )

    @patch("character.management.commands.load_characters.time")
    @patch("character.management.commands.load_characters.os")
    @patch("character.management.commands.load_characters.hashlib")
    def test_get_auth_params(self, mock_hashlib, mock_os, mock_time):
        mock_os.getenv.return_value = "test_value"
        mock_time.time.return_value = 123456789
        mock_hashlib.md5.return_value.hexdigest.return_value = "test_hash"

        auth_params = get_auth_params()

        expected_params = {
            "ts": "123456789",
            "apikey": API_KEY,
            "hash": "test_hash",
        }
        self.assertEqual(auth_params, expected_params)

    @patch("character.management.commands.load_characters.get_auth_params")
    @patch("character.management.commands.load_characters.fetch_character")
    @patch("character.management.commands.load_characters.save_spectrum_work_mates")
    @patch("character.management.commands.load_characters.save_character_data")
    def test_handle(
        self,
        mock_save_character_data,
        mock_save_spectrum_work_mates,
        mock_fetch_character,
        mock_get_auth_params,
    ):
        mock_get_auth_params.return_value = {"test_auth": "params"}
        mock_fetch_character.return_value = self.spectrum_character

        mock_save_spectrum_work_mates.return_value = None

        command = Command()
        command.handle()

        mock_save_character_data.assert_called_once_with(self.spectrum_character)
        mock_save_spectrum_work_mates.assert_called_once_with(
            self.spectrum_character,
            {"test_auth": "params"},
        )
