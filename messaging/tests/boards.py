from django.test import TestCase, Client
from messaging.models import Board, Thread
import json


class BoardTestCase(TestCase):
    def setUp(self):
        # Boards
        self.b1 = Board(code='b', name='random', description='desc')
        self.b1.save()
        # Threads
        self.t1 = Thread(body='test thread', board=self.b1)
        self.t1.save()
        # Client
        self.c = Client()

    def test_get_list_of_boards(self):
        """ Anyone can get a list of boards """
        response = self.c.get('/boards/')
        boards = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(boards), 1)
        self.assertEqual(boards[0]['code'], self.b1.code)

    def test_get_board(self):
        """ Anyone can get information about board and related threads """
        response = self.c.get(f'/boards/{self.b1.id}/')
        requested_board = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(requested_board['code'], self.b1.code)
        self.assertEqual(len(requested_board['threads']), 1)

    def test_unauthorized_post(self):
        """ Random visitors can't create new boards """
        response = self.c.post('/boards/', {
            'code': 't',
            'name': 'tests',
            'description': 'board for tests',
        })

        self.assertEqual(response.status_code, 403)

    def test_unauthorized_put(self):
        """ Random visitors can't modify boards """
        response = self.c.put(f'/boards/{self.b1.id}/', {
            'code': 'a',
            'name': self.b1.name,
            'description': self.b1.description
        })

        self.assertEqual(response.status_code, 403)

    def test_unauthorized_delete(self):
        """ Random visitors can't delete boards """
        response = self.c.delete(f'/boards/{self.b1.id}/')

        self.assertEqual(response.status_code, 403)