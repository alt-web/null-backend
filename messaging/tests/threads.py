from django.test import TestCase, Client
from messaging.models import Board, Thread, Reply
import json


class ThreadTestCase(TestCase):
    def setUp(self):
        # Boards
        self.b1 = Board(code='b', name='random', description='desc')
        self.b1.save()
        # Threads
        self.t1 = Thread(body='test thread', board=self.b1)
        self.t1.save()
        # Replies
        self.r1 = Reply(body='test reply', origin=self.t1)
        self.r1.save()
        # Client
        self.c = Client()

    def test_get_thread(self):
        """ Anyone can get information about thread and replies """
        response = self.c.get(f'/threads/{self.t1.id}/')
        requested_thread = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(requested_thread['body'], self.t1.body)
        self.assertEqual(len(requested_thread['replies']), 1)

    def test_unauthorized_post(self):
        """ Random visitors can create new threads """
        response = self.c.post('/threads/', {
            'body': 'new thread',
            'board': self.b1.id,
        })

        self.assertEqual(response.status_code, 201)

    def test_unauthorized_put(self):
        """ Random visitors can't modify threads """
        response = self.c.put(f'/threads/{self.t1.id}/', {
            'body': 'new body',
            'board': self.b1.id
        })

        self.assertEqual(response.status_code, 403)

    def test_unauthorized_delete(self):
        """ Random visitors can't delete threads """
        response = self.c.delete(f'/threads/{self.t1.id}/')

        self.assertEqual(response.status_code, 403)
