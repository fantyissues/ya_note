import pytest
from django.urls import reverse


@pytest.mark.parametrize(
    'parametrized_client, note_in_list',
    (
        (pytest.lazy_fixture('author_client'), True),
        (pytest.lazy_fixture('admin_client'), False),
    ),
)
def test_notes_list_for_different_users(
        note, parametrized_client, note_in_list,
):
    response = parametrized_client.get(reverse('notes:list'))
    object_list = response.context['object_list']
    assert (note in object_list) is note_in_list


@pytest.mark.parametrize(
    'name, args',
    (
        ('notes:add', None),
        ('notes:edit', pytest.lazy_fixture('slug_for_args')),
    ),
)
def test_pages_contains_form(author_client, name, args):
    response = author_client.get(reverse(name, args=args))
    assert 'form' in response.context
