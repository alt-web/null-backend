import requests
import magic
import json
from typing import Any
from django.db.models import Max
from rest_framework import serializers
from messaging.models import (
        Board,
        Thread,
        Reply,
        Attachment,
        Preview,
)
from messaging.utils import (
        get_ipfs_url,
        is_audio_file,
        is_video_file,
        get_audio_preview,
        get_audio_duration,
        get_video_preview,
        get_video_info,
)


class PreviewSerializer(serializers.ModelSerializer):
    """
    Simple version of attachment serializer
    """

    class Meta:
        model = Preview
        fields = ('id', 'cid', 'width', 'height', 'mimetype')


class AttachmentSerializer(serializers.ModelSerializer):
    file = serializers.FileField(write_only=True)
    preview = PreviewSerializer(read_only=True)

    class Meta:
        model = Attachment
        fields = ('id', 'file', 'cid', 'name', 'mimetype', 'size',
                  'width', 'height', 'duration', 'preview')
        read_only_fields = ['cid', 'name', 'mimetype', 'size',
                            'width', 'height', 'duration', 'preview']

    def create(self, validated_data: dict[str, Any]) -> Attachment:
        # Upload file to ipfs
        file = validated_data.pop('file')
        res = requests.post(
                get_ipfs_url('/api/v0/add?cid-version=1'),
                files={'django': file}
        )
        content = json.loads(res.content)

        # Save data from ipfs
        validated_data['cid'] = content['Hash']
        validated_data['name'] = content['Name']

        # Save file size
        validated_data['size'] = file.size

        # Get mime type
        file.seek(0)
        mime_type = magic.from_buffer(file.read(2048), mime=True)
        validated_data['mimetype'] = mime_type

        # Try to extract cover image from audio files
        if is_audio_file(mime_type):
            file.seek(0)
            validated_data['preview'] = get_audio_preview(file)
            file.seek(0)
            validated_data['duration'] = get_audio_duration(file)

        # Extract single frame from video
        elif is_video_file(mime_type):
            file_path = file.temporary_file_path()
            validated_data['preview'] = get_video_preview(file_path)
            video_info = get_video_info(file_path)
            validated_data['duration'] = video_info.duration
            validated_data['width'] = video_info.width
            validated_data['height'] = video_info.height

        instance = Attachment(**validated_data)
        instance.save()
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
        fields = ('id', 'body', 'created_at', 'origin', 'target', 'attachments',
                  'aid1', 'aid2', 'aid3', 'aid4')

    def create(self, validated_data: dict[str, Any]) -> Reply:
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
    # Body of the first reply
    body = serializers.CharField(write_only=True, required=True)
    # Attachment ids
    aid1 = serializers.IntegerField(write_only=True, required=False)
    aid2 = serializers.IntegerField(write_only=True, required=False)
    aid3 = serializers.IntegerField(write_only=True, required=False)
    aid4 = serializers.IntegerField(write_only=True, required=False)

    first_reply = serializers.SerializerMethodField()
    last_replies = serializers.SerializerMethodField()

    def get_first_reply(self, instance):
        """
        Returns the first reply
        """
        reply = instance.replies.earliest('id')
        return ReplySerializer(reply).data

    def get_last_replies(self, instance):
        """
        Returns only the last 3 replies
        """
        replies = list(instance.replies.all()[1:])
        last_replies = replies[-3:]
        
        return ReplySerializer(last_replies, many=True).data

    class Meta:
        model = Thread
        fields = ('id', 'body', 'first_reply', 'last_replies', 'board',
                  'aid1', 'aid2', 'aid3', 'aid4')

    def create(self, validated_data: dict[str, Any]) -> Thread:
        """
        Extract everything that belongs to the reply model,
        create the tread and thren create the first reply.
        """
        body = validated_data.pop('body')
        attachments = get_attachments(validated_data)
        # Create a thread
        thread = Thread(**validated_data)
        thread.save()
        # Create the first reply
        reply = Reply(body=body, origin=thread)
        reply.save()
        # Add attachments
        for attachment_id in attachments:
            reply.attachments.add(attachment_id)
        return thread


def get_attachments(validated_data: dict[str, Any]) -> list[int]:
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

    class Meta:
        model = Thread
        fields = ('id', 'board', 'replies')
    

class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ('id', 'code', 'name', 'description')


class BoardDetailedSerializer(serializers.ModelSerializer):
    threads = serializers.SerializerMethodField()

    def get_threads(self, instance):
        """ Sort threads by the date of last reply """
        threads = Thread.objects.filter(board=instance)
        threads_with_dates = threads.annotate(last_reply_date=Max('replies__created_at'))
        ordered_threads = threads_with_dates.order_by('-last_reply_date')
        return ThreadSerializer(ordered_threads, many=True).data

    class Meta:
        model = Board
        fields = ('id', 'code', 'name', 'description', 'threads')
