from rest_framework import serializers
from .models import Incident


class IncidentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Incident
        fields = ["id", "image", "category", "description", "created_at",
                  "video", "audio", "lat", "lng"]
