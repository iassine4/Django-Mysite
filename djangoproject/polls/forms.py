from django import forms


class QuestionCreateForm(forms.Form):
    """
    Formulaire simple pour créer une Question.
    - Identifiants (QuestionCreateForm, question_text).
    """

    question_text = forms.CharField(
        label="Texte de la question",
        max_length=200,  # validation automatique : <= 200
        required=True,  # validation : obligatoire
        help_text="200 caractères maximum.",
        error_messages={
            "required": "Le texte de la question est obligatoire.",
            "max_length": "Le texte est trop long (200 caractères max).",
            }
        ),
    )