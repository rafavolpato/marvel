from rest_framework.serializers import ModelSerializer

from character.models import Character


class CharacterModelSerializer(ModelSerializer):
    class Meta:
        model = Character
        fields = "__all__"
