import os
import time
import logging
import requests
import hashlib

from django.core.management import BaseCommand

from character.models import Character
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

load_dotenv()
API_KEY = os.getenv("API_KEY")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")

BASE_URL = "http://gateway.marvel.com/v1/public"
total_characters_saved = 0
total_characters_updated = 0


def get_character_data(character):
    character_id = character.get("id")
    name = character.get("name")
    description = character.get("description")
    picture = Character.get_picture_from_thumbnail(character.get("thumbnail"))
    return character_id, name, description, picture


def save_character_data(data):
    character_id, name, description, picture = get_character_data(data)
    obj, created = Character.objects.get_or_create(
        name=name,
        description=description,
        picture=picture,
        defaults={"character_id": character_id},
    )
    global total_characters_saved
    global total_characters_updated
    if created:
        total_characters_saved += 1
        logger.info(f"{name} saved.")
    else:
        total_characters_updated += 1
        logger.info(f"{name} updated.")


def http_get_json(endpoint, auth_params):
    try:
        response = requests.get(endpoint, params=auth_params)
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(
            f"Error calling endpoint: {endpoint}",
        )
        logger.error(e)
        raise SystemExit("Command terminated due to the previous errors.")


def fetch_character(name, auth_params):
    endpoint = f"{BASE_URL}/characters?name={name}"
    data = http_get_json(endpoint, auth_params)
    if data.get("data", {}).get("results"):
        return data["data"]["results"][0]
    return {}


def fetch_comic_characters(auth_params, comic_id, limit):
    endpoint = f"{BASE_URL}/comics/{comic_id}/characters?limit={limit}"
    data = http_get_json(endpoint, auth_params)
    if data.get("data", {}).get("results"):
        return data["data"]["results"]
    return {}


def fetch_comics_by_character(character_id, auth_params, limit):
    endpoint = f"{BASE_URL}/characters/{character_id}/comics?limit={limit}"
    data = http_get_json(endpoint, auth_params)
    if data.get("data", {}).get("results"):
        return data["data"]["results"]
    return {}


def save_spectrum_work_mates(character_data, auth_params):
    character_id = character_data.get("id")
    if not character_id:
        return
    available_comics = character_data.get("comics", {}).get("available", [])
    comics = fetch_comics_by_character(character_id, auth_params, available_comics)
    for comic in comics:
        if not comic.get("resourceURI"):
            continue
        comic_id = comic["resourceURI"].split("/")[-1]
        available_characters = comic.get("characters", {}).get("available", [])
        comic_characters = fetch_comic_characters(
            auth_params, comic_id, available_characters
        )
        for character in comic_characters:
            save_character_data(character)


def get_auth_params():
    ts = str(int(time.time()))
    hash_input = ts + PRIVATE_KEY + API_KEY
    hash_value = hashlib.md5(hash_input.encode("utf-8")).hexdigest()
    return {"ts": ts, "apikey": API_KEY, "hash": hash_value}


class Command(BaseCommand):
    def handle(self, *args, **options):
        auth_params = get_auth_params()
        character = fetch_character("spectrum", auth_params)
        if not character:
            logger.error(f"Spectrum not found.")
            raise SystemExit("Command terminated due to Spectrum not found.")
        save_character_data(character)
        save_spectrum_work_mates(character, auth_params)
        logger.info(f"Total characters saved: {total_characters_saved}")
        logger.info(f"Total characters updated: {total_characters_updated}")
