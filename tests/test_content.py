from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestContent(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор заметки')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        all_notes = [
            Note(
                title=f'Заметка {index}',
                text='Текст заметки',
                author=cls.author,
                slug=f'Note-{index}',
            )
            for index in range(10)
        ]
        Note.objects.bulk_create(all_notes)

    def test_notes_count(self):
        response = self.author_client.get(reverse('notes:list'))
        object_list = response.context['object_list']
        notes_count = object_list.count()
        self.assertEqual(notes_count, 10)
