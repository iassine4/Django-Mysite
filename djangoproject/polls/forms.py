from django import forms
from .models import Question


class QuestionWithChoicesForm(forms.Form):
    """
    Formulaire de création d'une Question + jusqu'à 5 Choices.

    - Identifiants en anglais (classe/champs).
    - Commentaires et messages en français.
    - Validation :
        * question_text obligatoire
        * au moins 2 choix non vides
        * max 5 (via les 5 champs)
    """

    # --- Bloc 1 : champ principal (la question) ---
    question_text = forms.CharField(
        label="Texte de la question",
        max_length=200,
        required=True,
        help_text="200 caractères maximum.",
        widget=forms.Textarea(
            attrs={
                "rows": 3,
                "placeholder": "Ex : Quelle est ta pizza préférée ?",
            }
        ),
        error_messages={
            "required": "Le texte de la question est obligatoire.",
            "max_length": "Le texte est trop long (200 caractères max).",
        },
    )

    # --- Bloc 2 : 5 champs de choix (optionnels individuellement) ---
    choice_1 = forms.CharField(
        label="Choix 1",
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Ex : Margherita"}),
    )
    choice_2 = forms.CharField(
        label="Choix 2",
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Ex : Reine"}),
    )
    choice_3 = forms.CharField(
        label="Choix 3",
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Ex : 4 fromages"}),
    )
    choice_4 = forms.CharField(
        label="Choix 4",
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Optionnel"}),
    )
    choice_5 = forms.CharField(
        label="Choix 5",
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Optionnel"}),
    )

    # --- Bloc 3 : validation globale (cross-field validation) ---
    def clean(self):
        """
        clean() sert à valider des règles qui concernent plusieurs champs.
        Ici : au moins 2 choices non vides.
        """
        cleaned_data = super().clean()

        # On récupère les 5 choix, on strip() pour éviter "   " (espaces)
        raw_choices = [
            cleaned_data.get("choice_1", "").strip(),
            cleaned_data.get("choice_2", "").strip(),
            cleaned_data.get("choice_3", "").strip(),
            cleaned_data.get("choice_4", "").strip(),
            cleaned_data.get("choice_5", "").strip(),
        ]

        # On garde seulement ceux qui ne sont pas vides
        non_empty_choices = [c for c in raw_choices if c]

        if len(non_empty_choices) < 2:
            # Erreur "générale" du formulaire (pas d'un champ en particulier)
            raise forms.ValidationError(
                "Tu dois saisir au moins 2 choix pour créer un sondage."
            )

        # On stocke la liste filtrée dans cleaned_data pour la vue
        cleaned_data["non_empty_choices"] = non_empty_choices

        return cleaned_data