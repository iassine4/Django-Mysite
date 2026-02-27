import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        """
        Affiche un résumé : 20 premiers caractères + date de publication.
        """
        # On évite un texte trop long
        text_preview = self.question_text[:20]
        # On met la date en format simple
        date_str = self.pub_date.strftime("%Y-%m-%d %H:%M")
        return f"{text_preview} ({date_str})"

    def was_published_recently(self):
        """
        True uniquement si la publication est entre
        (now - 1 jour) et now.
        → interdit le futur + interdit trop ancien.
        """
        now = timezone.now()  # maintenant (avec timezone Django)
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def age(self):
        """
        Retourne l'âge de la question sous forme de timedelta.
        Exemple : 3 days, 2:10:00
        """
        # On récupère l'heure actuelle (timezone-aware)
        now = timezone.now()
        # On retourne la différence (timedelta)
        return now - self.pub_date

    def get_choices(self):
        """
        Retourne une liste de tuples:
        (choice, votes, ratio)

        - choice: objet Choice
        - votes: int
        - ratio: float entre 0 et 1 (proportion des votes)
        """
        choices = list(self.choice_set.all())

        total_votes = sum(choice.votes for choice in choices)

        results = []
        for choice in choices:
            # Évite division par zéro si aucun vote
            ratio = (choice.votes / total_votes) if total_votes > 0 else 0.0
            results.append((choice, choice.votes, ratio))

        return results

    def get_max_choice(self):
        """
        Retourne un tuple:
        (max_choice, max_votes, ratio)

        - max_choice: Choice ou None
        - max_votes: int
        - ratio: float entre 0 et 1
        """
        choices = list(self.choice_set.all())
        if not choices:
            return None, 0, 0.0

        total_votes = sum(choice.votes for choice in choices)

        max_choice = max(choices, key=lambda c: c.votes)
        ratio = (max_choice.votes / total_votes) if total_votes > 0 else 0.0

        return max_choice, max_choice.votes, ratio

    def __repr__(self):
        """
        Représentation technique (utile pour les tests et le shell).
        On garde le texte complet, même si __str__ est tronqué.
        """
        return "<Question: {}>".format(self.question_text)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        """
        Affiche seulement les 20 premiers caractères du texte.
        """
        return self.choice_text[:20]
