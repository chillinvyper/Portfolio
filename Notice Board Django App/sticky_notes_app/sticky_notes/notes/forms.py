from django import forms
from .models import Note


class NoteForm(forms.ModelForm):
    '''Form for creating a nd updating Note objects

    Fields:
    title: charfield for note title
    content: textfield for the note's content

    Meta class:
    defines the model to use (Note) and the fields to include in the form

    param forms.Modelform: Djangos ModelForm class'''
    class Meta:
        model = Note
        fields = ['title', 'content', 'author']
