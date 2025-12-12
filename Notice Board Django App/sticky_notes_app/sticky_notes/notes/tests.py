from django.test import TestCase
from django.urls import reverse
from notes.models import Note, Author

# Create your tests here.


class NoteModelTest(TestCase):
    def setUp(self):
        # create author object
        author = Author.objects.create(name='Test Author')
        # create a Note object for testing
        Note.objects.create(title='Test Note', content='This is a test note.',
                            author=author)

    def test_note_has_title(self):
        # Test that the note object has the expected title
        note = Note.objects.get(id=1)
        self.assertEqual(note.title, 'Test Note')

    def test_note_has_content(self):
        # testing that the note has the expected content
        note = Note.objects.get(id=1)
        self.assertEqual(note.content, 'This is a test note.')


class NoteViewTest(TestCase):
    def setUp(self):
        # create author object
        author = Author.objects.create(name='Test Author')
        # create a Note object for testing views
        Note.objects.create(title='Test Note', content='This is a test note.',
                            author=author)

    def test_note_list_view(self):
        # test the note list view
        response = self.client.get(reverse('note_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Note')

    def test_note_detail_view(self):
        # Test the note-detail view
        note = Note.objects.get(id=1)
        response = self.client.get(reverse('note_detail', args=[str(note.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Note')
        self.assertContains(response, 'This is a test note')


class TestNoteUpdate(TestCase):
    def setUp(self):

        self.author = Author.objects.create(
            name='An Author')
        self.note = Note.objects.create(
            title="A Title", author=self.author, content='some content')

    def test_update_title(self):
        # Tests if the title is corretly updating
        new_title = "Test Title"
        self.note.title = new_title
        self.note.save()
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, new_title)

    def test_update_content(self):
        # Testing if the content is updating correctly
        new_content = "Test new content"
        self.note.content = new_content
        self.note.save()
        self.note.refresh_from_db()
        self.assertEqual(self.note.content, new_content)


class TestNoteDelete(TestCase):
    def setUp(self):
        self.author = Author.objects.create(
            name='An Author')
        self.note = Note.objects.create(
            title="A Title", author=self.author, content='some content')

    def test_note_delete(self):
        note_id = self.note.id
        self.note.delete()
        self.assertFalse(Note.objects.filter(id=note_id).exists())
