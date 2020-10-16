from django.urls import path
from election_watch import views

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("feedback/", views.feedback, name="feedback"),
    path("incidents/", views.incidents, name="incidents"),
    path("login/", views.sign_in, name="login"),
    path("reports/", views.reports, name="reports"),
    path("results/", views.results, name="results"),
    path("profile/", views.profile, name="profile"),

    path("register/", views.register_admin, name="register"),

    # path("register/inst/", views.register_institution,
         # name="register-inst"),

    path("register/location/", views.register_location,
         name="register-location"),

    path("register/agents/", views.register_agents,
         name="register-agents"),

    path("profile/", views.profile, name="profile"),
]
