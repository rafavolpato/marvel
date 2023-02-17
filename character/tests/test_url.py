from django.urls import resolve
from django.test import TestCase
from django.urls import reverse

from character.views import CharacterModelViewSet


class TestURLs(TestCase):
    def test_url_resolve(self):
        self.assertEqual(resolve(reverse("character-list")).func.cls, CharacterModelViewSet)
