from django.conf import settings
import os
import io
import urllib.parse
import requests
import json
import uuid
import subprocess
from typing import Union, Tuple, BinaryIO, Any
from PIL import Image
from mutagen.id3 import ID3
from messaging.models import Preview


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


def is_video_file(mime_type: str) -> bool:
    """
    Check the mime type and tells if the file is video or not
    """
    if mime_type.startswith('video'):
        return True

    return False


def compress_image(image_data: BinaryIO) -> Tuple[io.BytesIO, int, int]:
    """
    Resizes an image and saves it in a webp format.
    Returns image buffer, width and height.
    """
    buffer = io.BytesIO()

    # Load image
    with Image.open(image_data) as img:
        rgb_img = img.convert("RGB")

        # Resize image
        width, height = rgb_img.size
        max_size = 200
        ratio = max_size / width if width > height else max_size / height
        width = int(width * ratio)
        height = int(height * ratio)
        final_img = rgb_img.resize((width, height))

        # Save image
        final_img.save(buffer, format="WebP")

    return (buffer, width, height)


def get_audio_preview(file: BinaryIO) -> Union[Preview, None]:
    """
    Tries to extract the cover from audio file.
    Returns None if any exception was raised.
    """
    try:
        tags = ID3(file)
        image_data = tags['APIC:'].data
        image_buffer = io.BytesIO(image_data)

        # Convert to webp
        image_data, width, height = compress_image(image_buffer)
        image_data.seek(0)

        # Upload to ipfs
        res = requests.post(
                get_ipfs_url('/api/v0/add?cid-version=1'),
                files={'django': image_data}
        )
        content = json.loads(res.content)

        # Save attachment
        record = Preview(
                cid=content['Hash'],
                mimetype='image/webp',
                width=width,
                height=height,
        )
        record.save()
        return record

    except:
        return None


def get_image_size(file_path: str) -> Tuple[int, int]:
    """
    Returns width and height of the image
    """
    with Image.open(file_path) as img:
        return img.size


def get_video_preview(file_path: str) -> Union[Preview, None]:
    try:
        # Generate preview with ffmpeg
        preview_path = f'/tmp/{uuid.uuid4()}.webp'
        cmd = ['ffmpeg', '-i', file_path,
               '-vf', 'thumbnail,scale=200:200:force_original_aspect_ratio=decrease',
               '-frames:v', '1',
               preview_path
        ]
        subprocess.run(cmd, check=True)

        # Upload preview to ipfs
        with open(preview_path, 'rb') as image:
            res = requests.post(
                    get_ipfs_url('/api/v0/add?cid-version=1'),
                    files={'django': image}
            )
        content = json.loads(res.content)

        width, height = get_image_size(preview_path)

        # Save attachment
        record = Preview(
                cid=content['Hash'],
                mimetype='image/webp',
                width=width,
                height=height,
        )
        record.save()

        # Delete preview from local storage
        os.remove(preview_path)

        return record

    except:
        return None


class VideoInfo:
    def __init__(self, duration: Union[float, None], width: Union[int, None], height: Union[int, None]):
        self.duration = duration
        self.width = width
        self.height = height


def get_video_info(video_path: str) -> VideoInfo:
    """
    Runs ffprobe and 
    """

    def get_video_stream(streams: dict[str, Any]) -> dict[str, Any]:
        """
        Selects a video stream from all streams
        """
        for stream in streams:
            if stream['codec_type'] == 'video':
                return stream

    try:
        # Run ffprobe
        cmd = ['ffprobe', video_path,
               '-v', 'quiet',
               '-print_format', 'json',
               '-show_format', '-show_streams'
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)

        # Parse result
        info = json.loads(result.stdout)
        video_stream = get_video_stream(info['streams'])

        # Save info
        duration = info['format']['duration']
        width = video_stream['width']
        height = video_stream['height']
        return VideoInfo(duration, width, height)

    except:
        return VideoInfo(None, None, None)
