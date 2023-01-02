from django.conf import settings
import os
import io
import urllib.parse
import requests
import json
from PIL import Image
from mutagen.id3 import ID3
from messaging.models import Attachment


def get_ipfs_url(path: str) -> str:
    if settings.DEBUG:
        return urllib.parse.urljoin('http://localhost:5001', path)

    host = os.environ.get('IPFS_HOST', 'http://ipfs:5001')
    return urllib.parse.urljoin(host, path)


def is_audio_file(mime_type: str) -> bool:
    """
    Checks the mime type and tells if the file is audio or not
    """
    if mime_type.startswith('audio'):
        return True

    # MP3 files sometimes recognised as octet-stream
    if mime_type == 'application/octet-stream':
        return True
    
    return False


def encode_webp(image_data):
    """
    Converts image to webp format
    """
    img = Image.open(image_data).convert("RGB")
    buffer = io.BytesIO()
    img.save(buffer, format="WebP")
    return buffer


def get_audio_preview(file) -> Attachment:
    """
    Tries to extract the cover from audio file.
    Returns None if any exception was raised.
    """
    try:
        tags = ID3(file)
        image_data = tags['APIC:'].data
        image_buffer = io.BytesIO(image_data)

        # Convert to webp
        image_data = encode_webp(image_buffer)
        image_data.seek(0)

        # Upload to ipfs
        res = requests.post(
                get_ipfs_url('/api/v0/add?cid-version=1'),
                files={'django': image_data}
        )
        content = json.loads(res.content)

        # Save attachment
        record = Attachment(cid=content['Hash'], name='cover.webp', size=image_data.getbuffer().nbytes, mimetype='image/webp')
        record.save()
        return record

    except:
        return None
