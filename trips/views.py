from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from shared.permissions import IsOwnerOrReadOnly

from .models import Trip
from .serializers import TripSerializer
from .filters import TripFilter


class TripViewSet(ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    permission_classes = [
        IsOwnerOrReadOnly,
        IsAuthenticatedOrReadOnly,
    ]
    filterset_class = TripFilter

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
