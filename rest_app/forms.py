from django import forms
from .models import *

class RecipesForm(forms.ModelForm):  #inherits the form model to class recipesform
    class Meta:
        model = recipes     #clarifying the model and its fields
        fields = ['name', 'prep_time', 'difficulty', 'vegetarian', 'Recipe_img', 'description']

'''With this setup, Django will automatically generate a form based on the recipes model. This form will typically include:

Text fields for entering the recipe name, description, etc.
A dropdown menu for selecting difficulty level.
A checkbox for indicating vegetarian or non-vegetarian.
An option to upload a recipe image.'''