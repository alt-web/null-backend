from rest_framework import serializers
from messaging.models import Board, Thread, Reply, Attachment


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ('file',)


class ReplySerializer(serializers.ModelSerializer):
    attachments = AttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = Reply
        fields = ('id', 'body', 'origin', 'attachments')


class ThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = ('id', 'body', 'board')


class ThreadDetailedSerializer(serializers.ModelSerializer):
    replies = ReplySerializer(many=True, read_only=True)

    class Meta:
        model = Thread
        fields = ('id', 'body', 'board', 'replies')


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ('id', 'code', 'name', 'description')


class BoardDetailedSerializer(serializers.ModelSerializer):
    threads = ThreadSerializer(many=True, read_only=True)

    class Meta:
        model = Board
        fields = ('id', 'code', 'name', 'description', 'threads')



