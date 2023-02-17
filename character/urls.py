from rest_framework import routers
from character import views

router = routers.SimpleRouter()
router.register(r"character", views.CharacterModelViewSet, basename="character")
urlpatterns = router.urls
