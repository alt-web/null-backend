from django.db import models


class Board(models.Model):
    code = models.CharField(max_length=6)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=256)

    def __str__(self):
        return f'/{self.code}/ - {self.name}'

class Attachment(models.Model):
    # Ipfs CID
    cid = models.CharField(max_length=59)

    # Original file name
    name = models.CharField(max_length=256)

    # Mime type guessed using the standard library
    mimetype = models.CharField(max_length=36)

    # File size in bytes
    size = models.PositiveIntegerField()

    # Optional width and height in pixels (image/video only)
    width = models.PositiveIntegerField(null=True, blank=True, default=None)
    height = models.PositiveIntegerField(null=True, blank=True, default=None)

    # Optional length in seconds (video/audio only)
    length = models.PositiveIntegerField(null=True, blank=True, default=None)

    def __str__(self):
        return self.name


class Post(models.Model):
    """
    Base class for threads and replies
    """
    body = models.CharField(max_length=1024)
    attachments = models.ManyToManyField(Attachment)

    def __str__(self):
        return self.body[:20]


class Thread(Post):
    board = models.ForeignKey(Board, related_name='threads', on_delete=models.CASCADE)


class Reply(Post):
    origin = models.ForeignKey(Thread, related_name='replies', on_delete=models.CASCADE)
