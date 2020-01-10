from rest_framework import routers
from users.views import UserViewSet
from places.views import PlaceViewSet
from vehicles.views import VehicleViewSet
from trips.views import TripViewSet

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('places', PlaceViewSet)
router.register('vehicles', VehicleViewSet)
router.register('trips', TripViewSet)

