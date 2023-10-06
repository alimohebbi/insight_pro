from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'analyze'
urlpatterns = [
    path("", views.index, name="index"),
    path("<company_id>/results/", views.results, name="results"),
    path("progress/", views.progress, name="progress"),
    path("leaderboad/", views.leaderboard, name="leaderboard"),
    path("get_insight/", views.get_insight, name="get_insight"),
]

