from django.db import models


class Board(models.Model):
    code = models.CharField(max_length=6)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=256)

    def __str__(self):
        return f'/{self.code}/ - {self.name}'


class Preview(models.Model):
    """
    The model is a simplified version of the attachment.
    - For an audio this is the album cover.
    - For a video it is a frame from the video.
    - For a picture it is a smaller version of the picture.
    """
    # Ipfs CID
    cid = models.CharField(max_length=59)

    # Mime type
    mimetype = models.CharField(max_length=36)

    # Width and height
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()


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

    # Optional preview for video or audio files.
    # Under the hood it's just another attachment.
    preview = models.ForeignKey(
            Preview,
            on_delete=models.SET_NULL,
            default=None, null=True, blank=True,
    )

    def __str__(self):
        return self.name


class Thread(models.Model):
    board = models.ForeignKey(
            Board,
            related_name='threads',
            on_delete=models.CASCADE
    )


class Reply(models.Model):
    body = models.CharField(max_length=1024)
    created_at = models.DateTimeField(auto_now_add=True)
    origin = models.ForeignKey(
            Thread,
            related_name='replies',
            on_delete=models.CASCADE
    )
    target = models.ForeignKey(
            'self',
            related_name='replies',
            on_delete=models.SET_NULL,
            default=None, null=True, blank=True,
    )
    attachments = models.ManyToManyField(Attachment)
