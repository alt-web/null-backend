import requests
import magic
import json
from rest_framework import serializers
from messaging.models import Board, Thread, Reply, Attachment


class AttachmentSerializer(serializers.ModelSerializer):
    file = serializers.FileField(write_only=True)

    class Meta:
        model = Attachment
        fields = ('id', 'file', 'cid', 'name', 'mimetype', 'size', 'width', 'height', 'length')
        read_only_fields = ['cid', 'name', 'mimetype', 'size', 'width', 'height', 'length']
    
    def save(self, **kwargs):
        # Upload file to ipfs
        file = self.validated_data.pop('file')
        res = requests.post('http://localhost:5001/api/v0/add?cid-version=1', files={'django': file})
        content = json.loads(res.content)
       
        # Save data from ipfs
        self.validated_data['cid'] = content['Hash']
        self.validated_data['name'] = content['Name']

        # Save file size
        self.validated_data['size'] = file.size

        # Get mime type
        file.seek(0)
        mime_type = magic.from_buffer(file.read(2048), mime=True)
        self.validated_data['mimetype'] = mime_type

        instance = Attachment.objects.create(**self.validated_data)
        return instance


class ReplySerializer(serializers.ModelSerializer):
    """
    Serializer for reply - any post in thread
    """
    # Attachment ids
    aid1 = serializers.IntegerField(write_only=True, required=False)
    aid2 = serializers.IntegerField(write_only=True, required=False)
    aid3 = serializers.IntegerField(write_only=True, required=False)
    aid4 = serializers.IntegerField(write_only=True, required=False)
    
    attachments = AttachmentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Reply
        fields = ('id', 'body', 'origin', 'attachments', 'aid1', 'aid2', 'aid3', 'aid4')

    def create(self, validated_data):
        # Save attachment ids
        attachments = get_attachments(validated_data)
        # Create a reply
        reply = Reply(**validated_data)
        reply.save()
        # Add attachments
        for attachment_id in attachments:
            reply.attachments.add(attachment_id)
        return reply


class ThreadSerializer(serializers.ModelSerializer):
    # Attachment ids
    aid1 = serializers.IntegerField(write_only=True, required=False)
    aid2 = serializers.IntegerField(write_only=True, required=False)
    aid3 = serializers.IntegerField(write_only=True, required=False)
    aid4 = serializers.IntegerField(write_only=True, required=False)
    
    attachments = AttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = Thread
        fields = ('id', 'body', 'board', 'aid1', 'aid2', 'aid3', 'aid4', 'attachments')

    def create(self, validated_data):
        # Save attachments
        attachments = get_attachments(validated_data)
        # Create a thread
        thread = Thread(**validated_data)
        thread.save()
        # Add attachments
        for attachment_id in attachments:
            thread.attachments.add(attachment_id)
        return thread


def get_attachments(validated_data):
    attachment_ids = []
    for i in range(1, 5):
        key = f'aid{i}'
        try:
            aid = validated_data.pop(key)
            attachment_ids.append(aid)
        except KeyError:
            pass
    return attachment_ids


class ThreadDetailedSerializer(serializers.ModelSerializer):
    replies = ReplySerializer(many=True, read_only=True)
    attachments = AttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = Thread
        fields = ('id', 'body', 'board', 'replies', 'attachments')


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ('id', 'code', 'name', 'description')


class BoardDetailedSerializer(serializers.ModelSerializer):
    threads = ThreadSerializer(many=True, read_only=True)

    class Meta:
        model = Board
        fields = ('id', 'code', 'name', 'description', 'threads')
