THUMBNAILS = [
    {
        "path": "http://i.annihil.us/u/prod/marvel/i/mg/c/e0/535fecbbb9784",
        "extension": "jpg",
    },
    {
        "path": "http://i.annihil.us/u/prod/marvel/i/mg/9/50/4ce18691cbf04",
        "extension": "jpg",
    },
]
CHARACTERS = [
    {
        "id": 1011333,
        "name": "3-D Man",
        "description": "description",
        "thumbnail": THUMBNAILS[0],
        "resourceURI": "http://gateway.marvel.com/v1/public/comics/1011333",
        "characters": {"available": 2},
    },
    {
        "id": 1010745,
        "name": "Abomination (Emil Blonsky)",
        "description": "description",
        "thumbnail": THUMBNAILS[1],
        "resourceURI": "http://gateway.marvel.com/v1/public/comics/1011333",
        "characters": {"available": 2},
    },
]
SPECTRUM_CHARACTER = {
    "id": 1010705,
    "name": "Spectrum",
    "description": "Monica Rambeau is a force to be reckoned with",
    "thumbnail": {
        "path": "http://i.annihil.us/u/prod/marvel/i/mg/c/50/4bc69f4b7f4fe",
        "extension": "jpg",
    },
    "comics": {
        "items": [
            {"resourceURI": "http://gateway.marvel.com/v1/public/comics/12345"},
            {"resourceURI": "http://gateway.marvel.com/v1/public/comics/67890"},
        ],
        "available": 2,
    },
}
