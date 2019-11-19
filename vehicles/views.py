from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from shared.permissions import IsOwnerOrReadOnly
from .models import Vehicle
from .serializers import VehicleSerializer


class VehicleViewSet(ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

    permission_classes = [
        IsOwnerOrReadOnly,
        permissions.IsAuthenticatedOrReadOnly,
    ]

    def perform_create(self, serializer):
        # set user to the logged in user
        serializer.save(user=self.request.user)
