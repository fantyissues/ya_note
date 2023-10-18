from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestRoutes(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор заметки')
        cls.user = User.objects.create(username='Пользователь')
        cls.note = Note.objects.create(
            title='Заголовок заметки',
            text='Текст заметки',
            slug='test-note-slug',
            author=cls.author,
        )

    def test_pages_availability(self):
        view_names = (
            'notes:home',
            'users:login',
            'users:logout',
            'users:signup',            
        )
        for name in view_names:
            with self.subTest(name=name):
                response = self.client.get(reverse(name))
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_availability_for_auth_user(self):
        view_names = (
            'notes:list',
            'notes:add',
            'notes:success',
        )
        self.client.force_login(self.user)
        for name in view_names:
            with self.subTest(name=name):
                response = self.client.get(reverse(name))
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_availability_for_note_read_edit_and_delete(self):
        users_statuses = (
            (self.author, HTTPStatus.OK),
            (self.user, HTTPStatus.NOT_FOUND),
        )
        for user, status in users_statuses:
            self.client.force_login(user)
            for name in ('notes:detail', 'notes:edit', 'notes:delete'):
                with self.subTest(name=name):
                    response = self.client.get(
                        reverse(name, args=(self.note.slug,))
                    )
                    self.assertEqual(response.status_code, status)

    def test_redirect_for_anonymous_client(self):
        view_names_args = (
            ('notes:list', None),
            ('notes:add', None),
            ('notes:success', None),
            ('notes:detail', (self.note.slug,)),
            ('notes:edit', (self.note.slug,)),
            ('notes:delete', (self.note.slug,)),
        )
        login_url = reverse('users:login')
        for name, args in view_names_args:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                redirect_url = f'{login_url}?next={url}'
                self.assertRedirects(self.client.get(url), redirect_url)
