from django.urls import path
from . import views

# Namespace (important pour {% url 'polls:detail' ... %})
app_name = "polls"

urlpatterns = [
    # Routes fixes d'abord
    path("all/", views.AllView.as_view(), name="all"),
    path("statistics/", views.statistics, name="statistics"),

    # Index
    path("", views.index, name="index"),

    # Routes dynamiques ensuite
    path("<int:question_id>/", views.detail, name="detail"),
    path("<int:question_id>/results/", views.results, name="results"),

    # Actions liées à une question
    path("<int:question_id>/vote/", views.vote, name="vote"),
    path("<int:question_id>/frequency/", views.frequency, name="frequency"),
]