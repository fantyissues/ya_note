from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.forms import NoteForm
from notes.models import Note

User = get_user_model()


class TestContent(TestCase):
    HOME_URL = reverse('notes:list')

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.user = User.objects.create(username='Пользователь')
        cls.note = Note.objects.create(
            title='Заголовок заметки',
            text='Текст заметки',
            slug='note-slug',
            author=cls.author,
        )

    def test_notes_list_for_author(self):
        response = self.author_client.get(self.HOME_URL)
        self.assertIn(self.note, response.context['object_list'])

    def test_notes_list_for_not_author(self):
        self.client.force_login(self.user)
        response = self.client.get(self.HOME_URL)
        self.assertNotIn(self.note, response.context['object_list'])

    def test_pages_contains_form(self):
        names_args = (
            ('notes:add', None),
            ('notes:edit', (self.note.slug,))
        )
        for name, args in names_args:
            with self.subTest(name=name):
                response = self.author_client.get(reverse(name, args=args))
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
