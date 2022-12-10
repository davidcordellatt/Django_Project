from django.urls import path

from . import views

app_name = "polls"

urlpatterns = [

    #ex: /polls/
    path("", views.IndexView.as_view(), name="index"),

    #ex: /polls/details
    path("<int:pk>/details", views.DetailsView.as_view(), name="details"),

    #ex: /polls/results
    path("<int:pk>/results", views.ResultsView.as_view(), name="results"),

    #ex: /polls/vote
    path("<int:question_id>/vote", views.vote, name="vote"),
]
