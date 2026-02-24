from django.contrib import admin
from .models import Question, Choice

class QuestionAdmin(admin.ModelAdmin):
    # Affiche plusieurs colonnes dans la liste
    list_display = ("id", "question_text", "pub_date")

    # Ajoute une barre de filtres à droite
    list_filter = ("pub_date",)

    # Tri par défaut (plus récent d’abord)
    ordering = ("-pub_date",)

    # Barre de recherche
    search_fields = ("question_text",)


class ChoiceAdmin(admin.ModelAdmin):
    # Affiche les champs utiles + la question liée
    list_display = ("id", "choice_text", "votes", "question")

    # Filtrer par question (et éventuellement votes !)
    list_filter = ("question",)

    # Tri par défaut (+ les plus de votes d’abord)
    ordering = ("-votes",)

    # Recherche sur le texte du choix + question liée (relation)
    search_fields = ("choice_text", "question__question_text")


# Enregistrement avec leurs classes d'admin
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
