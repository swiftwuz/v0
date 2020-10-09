from rest_framework import serializers
from .models import Incident


class IncidentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Incident
        fields = ["image", "category", "description", "created_at",
                  "video", "audio", "lat", "lng"]
