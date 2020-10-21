from django.contrib import admin
from election_watch.models import Institution
from .models import User

admin.site.register(User)
admin.site.register(Institution)
