from django.urls import path

from . import views

app_name = 'analyze'
urlpatterns = [
    path("", views.index, name="index"),
    path("<website_id>/results/", views.results, name="results"),
    path("progress/", views.progress, name="progress"),
    path("get_insight/", views.get_insight, name="get_insight"),
]
