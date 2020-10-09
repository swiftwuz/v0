from django.urls import path
from election_watch import views as users_views

urlpatterns = [
    path("register/org", users_views.register, name="register-org"),
    path("register/admin/", users_views.register, name="register-admin"),
    path("profile/", users_views.profile, name="profile"),
]
