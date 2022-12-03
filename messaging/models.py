from django.db import models


class Board(models.Model):
    code = models.CharField(max_length=6)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=256)

    def __str__(self):
        return f'/{self.code}/ - {self.name}'


class Post(models.Model):
    """
    Base class for threads and replies
    """
    body = models.CharField(max_length=1024)

    def __str__(self):
        return self.body[:20]


class Thread(Post):
    board = models.ForeignKey(Board, related_name='threads', on_delete=models.CASCADE)


class Reply(Post):
    origin = models.ForeignKey(Thread, related_name='replies', on_delete=models.CASCADE)


class Attachment(models.Model):
    file = models.FileField()
    post = models.ForeignKey(Post, related_name='attachments', on_delete=models.CASCADE)

    def __str__(self):
        return self.file.name
