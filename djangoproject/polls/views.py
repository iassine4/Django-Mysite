# polls/views.py
from django.shortcuts import render
from .models import Question

def index(request):
    """
    Affiche la liste des 5 dernières questions.
    """
    latest_question_list = Question.objects.order_by("-pub_date")[:5]

    # render() = raccourci Django : charge le template + injecte le contexte
    context = {"latest_question_list": latest_question_list}
    return render(request, "polls/index.html", context)