from django import forms
from djangoproject.polls.models import Question


class QuestionCreateForm(forms.ModelForm):
    """
    ModelForm : Django construit le formulaire à partir du modèle.
    Moins de duplication = mieux pour SonarQube.
    """

    class Meta:
        model = Question
        fields = ["question_text"]  # on expose uniquement ce champ
        widgets = {
            "question_text": forms.Textarea(
                attrs={"rows": 3, "placeholder": "Ex : Quel est ton sport préféré ?"}
            )
        }
        labels = {"question_text": "Texte de la question"}
        help_texts = {"question_text": "200 caractères maximum."}