from rest_framework.viewsets import ModelViewSet

from character.models import Character
from character.serializers import CharacterModelSerializer


class CharacterModelViewSet(ModelViewSet):
    http_method_names = [
        "get",
    ]
    queryset = Character.objects.all()
    serializer_class = CharacterModelSerializer
