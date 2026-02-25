from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Choice, Question


def detail(request, question_id):
    """
    Page détail : affiche 1 question + ses choix.
    get_object_or_404() => renvoie une 404 si l'id n'existe pas.
    """
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})


def results(request, question_id):
    """
    Page résultats : après le vote, affiche les votes.
    """
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})


def vote(request, question_id):
    """
    Traite le POST du formulaire de vote.
    """
    question = get_object_or_404(Question, pk=question_id)

    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Si aucune option choisie => on réaffiche la page détail avec un message d'erreur
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "Tu n'as pas sélectionné de choix.",
            },
        )

    # On incrémente les votes
    selected_choice.votes += 1
    selected_choice.save()

    # Bonne pratique : Post/Redirect/Get
    return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))