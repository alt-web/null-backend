from django.test import TestCase, Client
from messaging.models import Board, Thread, Reply
import json


class ReplyTestCase(TestCase):
    def setUp(self) -> None:
        # Boards
        self.b1 = Board(code='b', name='random', description='desc')
        self.b1.save()
        # Threads
        self.t1 = Thread(board=self.b1)
        self.t1.save()
        # Replies
        self.r1 = Reply(body='test reply', origin=self.t1)
        self.r1.save()
        # Client
        self.c = Client()

    def test_get_list_of_replies(self) -> None:
        """ Users can't request a list of all replies """
        response = self.c.get('/replies/')

        self.assertEqual(response.status_code, 405)

    def test_get_reply(self) -> None:
        """ Anyone can get information about reply """
        response = self.c.get(f'/replies/{self.r1.id}/')
        requested_thread = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(requested_thread['body'], self.r1.body)

    def test_unauthorized_post(self) -> None:
        """ Random visitors can create new replies """
        response = self.c.post('/replies/', {
            'body': 'new reply',
            'origin': self.t1.id,
        })

        self.assertEqual(response.status_code, 201)

    def test_unauthorized_put(self) -> None:
        """ Random visitors can't modify replies """
        response = self.c.put(f'/replies/{self.r1.id}/', {
            'body': 'new body',
            'origin': self.t1.id
        })

        self.assertEqual(response.status_code, 403)

    def test_unauthorized_delete(self) -> None:
        """ Random visitors can't delete replies """
        response = self.c.delete(f'/replies/{self.r1.id}/')

        self.assertEqual(response.status_code, 403)
