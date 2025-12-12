from django.shortcuts import render, get_object_or_404, redirect
from .models import Note
from .forms import NoteForm

# Create your views here.


def note_list(request):
    '''View to display a list of notes

    param request: HTTP request object
    return: Rendered template with a list of notes'''

    notes = Note.objects.all()

    # creating a context dictionary to pass data

    context = {
        "notes": notes,
        "page_title": "List of Notes",
    }
    return render(request, "notes/notes_list.html", context)


def note_detail(request, pk):
    '''
    View to display details of a specific post

    param request: HTTP request object
    param pk: Primary key of the note
    return: Rendered template with details of the specified note'''

    note = get_object_or_404(Note, pk=pk)
    return render(request, "notes/notes_detail.html", {"note": note})


def note_create(request):
    '''view to create new note

    param request: HTTP request object
    return: Rendered template for creating a new note'''

    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.save()
            return redirect("note_list")
    else:
        form = NoteForm()
    return render(request, "notes/notes_form.html", {"form": form})


def note_update(request, pk):
    '''view to update and existing note

    param request: HTTP request object
    param pk: Primary key of the note to be updated
    return: Rendered template for updating the specified note'''

    note = get_object_or_404(Note, pk=pk)
    if request.method == "POST":
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            note = form.save(commit=False)
            note.save()
            return redirect("note_list")
    else:
        form = NoteForm(instance=note)
    return render(request, "notes/notes_form.html", {"form": form})


def note_delete(request, pk):
    '''view to delete an existing post

    param request: HTTP request object
    param pk: Primary key of the note to be deleted
    return: redirect to the list after deleton'''

    post = get_object_or_404(Note, pk=pk)
    post.delete()
    return redirect("note_list")
