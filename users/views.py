from django.contrib.auth import get_user_model
from rest_framework import viewsets, mixins

from .serializers import UserSerializer
from .permissions import IsAuthenticatedUserOrReadOnly


User = get_user_model()


class UserViewSet(
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        viewsets.GenericViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    permission_classes = [
        IsAuthenticatedUserOrReadOnly,
    ]
