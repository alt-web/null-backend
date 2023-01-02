from django.test import TestCase, Client
from messaging.models import Board, Thread, Reply
import json


class ThreadTestCase(TestCase):
    def setUp(self) -> None:
        # Boards
        self.b1 = Board(code='b', name='random', description='desc')
        self.b1.save()
        # Threads
        self.t1 = Thread(board=self.b1)
        self.t1.save()
        # Replies
        self.r1 = Reply(origin=self.t1)
        self.r1.save()
        # Client
        self.c = Client()

    def test_get_list_of_threads(self) -> None:
        """ Users can't request a list of all threads """
        response = self.c.get('/threads/')

        self.assertEqual(response.status_code, 405)

    def test_get_thread(self) -> None:
        """ Anyone can get information about thread and replies """
        response = self.c.get(f'/threads/{self.t1.id}/')
        requested_thread = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(requested_thread['board'], self.b1.id)
        self.assertEqual(len(requested_thread['replies']), 1)

    def test_unauthorized_post(self) -> None:
        """ Random visitors can create new threads """
        response = self.c.post('/threads/', {
            'body': 'Test thread',
            'board': self.b1.id,
        })

        self.assertEqual(response.status_code, 201)

    def test_unauthorized_put(self) -> None:
        """ Random visitors can't modify threads """
        response = self.c.put(f'/threads/{self.t1.id}/', {
            'board': self.b1.id
        })

        self.assertEqual(response.status_code, 403)

    def test_unauthorized_delete(self) -> None:
        """ Random visitors can't delete threads """
        response = self.c.delete(f'/threads/{self.t1.id}/')

        self.assertEqual(response.status_code, 403)
