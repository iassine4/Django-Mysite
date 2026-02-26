from django.db.models import Sum, Max
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .forms import QuestionCreateForm
from .models import Choice, Question

def create_question(request):
    """
    Vue pour créer une Question.
    - GET  → affiche le formulaire vide
    - POST → valide, enregistre en base, puis redirige
    """

    # 1) Cas GET : on veut juste afficher le formulaire
    if request.method == "GET":
        form = QuestionCreateForm()
        return render(request, "polls/create_question.html", {"form": form})

    # 2) Cas POST : on récupère ce que l'utilisateur a soumis
    form = QuestionCreateForm(request.POST)

    # 3) Validation Django (vérifie max_length, champ requis, etc.)
    if not form.is_valid():
        # Si invalide, on réaffiche la page avec les erreurs
        return render(request, "polls/create_question.html", {"form": form})

    # 4) Si valide : on crée l'objet en base
    question_text = form.cleaned_data["question_text"]

    # pub_date est maintenant (timezone-aware)
    Question.objects.create(
        question_text=question_text,
        pub_date=timezone.now(),
    )

    # 5) Post/Redirect/Get : après création, on redirige (éviter double-submit)
    return HttpResponseRedirect(reverse("polls:index"))

def statistics(request):
    """
    Page de stats sur les sondages.
    On utilise les agrégations Django (Sum, Max) comme demandé.
    """
    total_questions = Question.objects.count()
    total_choices = Choice.objects.count()

    # Somme de tous les votes (Choice.votes)
    agg_votes = Choice.objects.aggregate(total_votes=Sum("votes"))
    total_votes = agg_votes["total_votes"] or 0  # si None -> 0

    # Moyenne de votes par sondage (simple : total_votes / total_questions)
    avg_votes_per_question = (total_votes / total_questions) if total_questions > 0 else 0

    # Dernière date de publication (Max)
    agg_last = Question.objects.aggregate(last_pub_date=Max("pub_date"))
    last_pub_date = agg_last["last_pub_date"]

    # Dernière question enregistrée (si on a une date)
    last_question = None
    if last_pub_date is not None:
        last_question = Question.objects.filter(pub_date=last_pub_date).first()

    context = {
        "total_questions": total_questions,
        "total_choices": total_choices,
        "total_votes": total_votes,
        "avg_votes_per_question": avg_votes_per_question,
        "last_question": last_question,
        "last_pub_date": last_pub_date,
    }
    return render(request, "polls/statistics.html", context)

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