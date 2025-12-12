'''placeholder'''
from django.db import models

# Create your models here.


class Note(models.Model):

    '''the model representing each note

    fields:
    title: a charfield for the title with a max length of 255
    content: a textfield for the content of the note
    created_at: datetimefield set to the current time and date'''

    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # Define the foreign key for the author's relationship
    author = models.ForeignKey(
        "Author", on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return str(self.title)


class Author(models.Model):
    '''model representing the author

    fields:
    name: charfield for the authors name

    methods:
    __str__ a string representation of the authors name
    param models.model: Djangos base model class'''

    name = models.CharField(max_length=255)

    def __str__(self):
        return str(self.name)
