from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView
)
from rest_framework import permissions
from rest_framework.parsers import (
    MultiPartParser, FormParser, FileUploadParser
)
from .serializers import IncidentSerializer
from .models import Incident
from .permissions import IsOwner


class ImageUploadParser(FileUploadParser):
    media_type = 'image/*'


class IncidentListAPIView(ListCreateAPIView):
    serializer_class = IncidentSerializer
    queryset = Incident.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    parser_class = (MultiPartParser, FormParser, ImageUploadParser,
                    FileUploadParser)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class IncidentDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = IncidentSerializer
    queryset = Incident.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwner,)
    lookup_field = "id"
    parser_class = (MultiPartParser, FormParser, FileUploadParser)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
