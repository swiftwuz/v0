from django.db import models
from users.models import User


class Incident(models.Model):

    INCIDENT_TYPE = [
        ("NON-COMPLIANCE", "NON-COMPLIANCE"),
        ("LOGSITICS", "LOGSITICS"),
        ("HARRSASEMENT", "HARRSASEMENT"),
        ("INTERFERENCE", "INTERFERENCE"),
        ("VIOLENCE", "VIOLENCE"),
        ("DELAYS", "DELAYS"),
        ("CONFUSION", "CONFUSION"),
        ("CHAOS", "CHAOS"),
        ("POWER FAILURE", "POWER FAILURE"),
    ]

    category = models.CharField(choices=INCIDENT_TYPE, max_length=255)
    description = models.TextField()
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)

    image = models.ImageField(upload_to="pictures/",
                              blank=True, null=True)

    video = models.FileField(upload_to="videos/", blank=True, null=True)
    audio = models.FileField(upload_to="audio_files/", blank=True, null=True)

    lat = models.FloatField('lat', blank=True, null=True)
    lng = models.FloatField('lng', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering: ["-created_at"]

    def __str__(self):
        return f"{self.user}'s {self.description}.'"
