import pytest

from notes.models import Note


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def author_client(author, client):
    client.force_login(author)
    return client


@pytest.fixture
def note(author):
    return Note.objects.create(
        title='Заголовок',
        text='Текст заметки',
        slug='note-slug',
        author=author,
    )


@pytest.fixture
def slug_for_args(note):
    return note.slug,
