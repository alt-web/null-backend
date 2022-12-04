from rest_framework import generics
from messaging.models import Board, Thread, Reply, Attachment
from messaging.serializers import BoardSerializer, BoardDetailedSerializer, ThreadSerializer, ThreadDetailedSerializer, ReplySerializer
from messaging.permissions import CreateOnly


class BoardList(generics.ListCreateAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer


class BoardDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardDetailedSerializer


class ThreadList(generics.ListCreateAPIView):
    permission_classes = [CreateOnly]
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer


class ThreadDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Thread.objects.all()
    serializer_class = ThreadDetailedSerializer


class ReplyList(generics.ListCreateAPIView):
    permission_classes = [CreateOnly]
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer


class ReplyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer
