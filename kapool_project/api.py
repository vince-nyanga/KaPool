from rest_framework import routers
from users.views import UserViewSet
from places.views import PlaceViewSet

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('places', PlaceViewSet)
