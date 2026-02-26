
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from .models import Choice, Question

def frequency(request, question_id):
    """
    Affiche les résultats du sondage :
    - votes (valeur absolue)
    - pourcentage
    Sans formulaire de vote.
    """
    question = get_object_or_404(Question, pk=question_id)

    # On essaye d'utiliser la méthode optionnelle get_choices()
    # Si elle n'existe pas, on calcule ici.
    if hasattr(question, "get_choices"):
        choices_stats = question.get_choices()
        # choices_stats attendu : liste de tuples (choice, votes, ratio)
    else:
        # Fallback (au cas où get_choices n'est pas présent)
        choices = list(question.choice_set.all())
        total_votes = sum(c.votes for c in choices)

        choices_stats = []
        for c in choices:
            ratio = (c.votes / total_votes) if total_votes > 0 else 0.0
            choices_stats.append((c, c.votes, ratio))

    context = {
        "question": question,
        "choices_stats": choices_stats,
    }
    return render(request, "polls/frequency.html", context)

class AllView(generic.ListView):
    """
    Affiche TOUS les sondages.
    """
    template_name = "polls/all.html"
    context_object_name = "question_list"

    def get_queryset(self):
        # On trie par date décroissante (plus récent en haut)
        return Question.objects.order_by("-pub_date")

def index(request):
    """
    Affiche la liste des 5 dernières questions.
    """
    latest_question_list = Question.objects.order_by("-pub_date")[:5]

    # render() = raccourci Django : charge le template + injecte le contexte
    context = {"latest_question_list": latest_question_list}
    return render(request, "polls/index.html", context)

def detail(request, question_id):
    """
    Page détail : affiche 1 question + ses choix.
    get_object_or_404() → renvoie une 404 si l'id n'existe pas.
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
        # Si aucune option choisie → on réaffiche la page détail avec un message d'erreur
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