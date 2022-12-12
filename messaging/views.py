from rest_framework import generics
from rest_framework.permissions import AllowAny
from messaging.models import Board, Thread, Reply, Attachment
from messaging.serializers import BoardSerializer, BoardDetailedSerializer, ThreadSerializer, ThreadDetailedSerializer, ReplySerializer, AttachmentSerializer


## Boards
##

class BoardList(generics.ListAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer


class BoardDetail(generics.RetrieveAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardDetailedSerializer


## Threads
##

class ThreadList(generics.CreateAPIView):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer
    permission_classes = [AllowAny]


class ThreadDetail(generics.RetrieveAPIView):
    queryset = Thread.objects.all()
    serializer_class = ThreadDetailedSerializer


## Replies
##

class ReplyList(generics.CreateAPIView):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer
    permission_classes = [AllowAny]


class ReplyDetail(generics.RetrieveAPIView):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer


## Attachments
##

class AttachmentUploader(generics.CreateAPIView):
    serializer_class = AttachmentSerializer
    queryset = Attachment.objects.all()
