from django import forms


class QuestionCreateForm(forms.Form):
    """
    Formulaire simple pour créer une Question.
    - Identifiants (QuestionCreateForm, question_text).
    """

    question_text = forms.CharField(
        label="Texte de la question",
        max_length=200,
        help_text="Écris la question (200 caractères max).",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Ex: Quel est ton framework préféré ?",
            }
        ),
    )