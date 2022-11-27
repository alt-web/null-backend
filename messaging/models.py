from django.db import models


class Board(models.Model):
    code = models.CharField(max_length=6)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=256)

    def __str__(self):
        return f'/{self.code}/ - {self.name}'

    def as_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'description': self.description,
        }


class Post(models.Model):
    """
    Base class for threads and replies
    """
    body = models.CharField(max_length=1024)

    def __str__(self):
        return self.body[:20]

    def as_dict(self):
        return {
            'id': self.id,
            'body': self.body,
        }


class Thread(Post):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)


class Reply(Post):
    origin = models.ForeignKey(Thread, on_delete=models.CASCADE)


class Attachment(models.Model):
    file = models.FileField(upload_to='attachments/')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.file.name
    
    def as_dict(self):
        return {
            'filename': self.file.name,
        }
