from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.forms import NoteForm
from notes.models import Note

User = get_user_model()


class TestNotesListPage(TestCase):
    NOTES_AMOUNT = 100
    HOME_URL = reverse('notes:list')

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='Автор')
        cls.user_client = Client()
        cls.user_client.force_login(cls.user)
        Note.objects.bulk_create(
            Note(
                title=f'Заметка {index}',
                text='Текст заметки',
                author=cls.user,
                slug=f'note-{index}',
            )
            for index in range(cls.NOTES_AMOUNT)
        )

    def test_notes_count(self):
        response = self.user_client.get(self.HOME_URL)
        object_list = response.context['object_list']
        self.assertEqual(len(object_list), self.NOTES_AMOUNT)


class TestNoteAddPage(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='Автор')
        cls.user_client = Client()
        cls.user_client.force_login(cls.user)
        cls.add_url = reverse('notes:add')
        cls.form_data = {
            'title': 'Заголовок',
            'text': 'Текст',
        }

    def test_note_add_has_form(self):
        response = self.user_client.get(self.add_url)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], NoteForm)
