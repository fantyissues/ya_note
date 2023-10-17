from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestRoutes(TestCase):
    SLUG = 'test-note-slug'

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор заметки')
        cls.user = User.objects.create(username='Пользователь')
        cls.note = Note.objects.create(
            title='Заголовок заметки',
            text='Текст заметки',
            slug=cls.SLUG,
            author=cls.author,
        )

    def test_reverse_view_name(self):
        urls = (
            ('/', 'notes:home', None),
            ('/add/', 'notes:add', None),
            (f'/edit/{self.SLUG}/', 'notes:edit', (self.SLUG,)),
            (f'/note/{self.SLUG}/', 'notes:detail', (self.SLUG,)),
            (f'/delete/{self.SLUG}/', 'notes:delete', (self.SLUG,)),
            ('/notes/', 'notes:list', None),
            ('/done/', 'notes:success', None),
            ('/auth/login/', 'users:login', None),
            ('/auth/logout/', 'users:logout', None),
            ('/auth/signup/', 'users:signup', None),
        )
        for path, view_name, args in urls:
            with self.subTest(path=path, view_name=view_name):
                self.assertEqual(path, reverse(view_name, args=args))

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
            ('notes:detail', (self.note.slug,)),
            ('notes:edit', (self.note.slug,)),
            ('notes:delete', (self.note.slug,)),
        )
        login_url = reverse('users:login')
        for name, args in view_names_args:
            with self.subTest(name=name, args=args):
                url = reverse(name, args=args)
                redirect_url = f'{login_url}?next={url}'
                self.assertRedirects(self.client.get(url), redirect_url)
