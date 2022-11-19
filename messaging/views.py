from django.http import JsonResponse
from messaging.models import Board, Thread, Reply, Attachment

def home(request):
    boards = []
    for i in Board.objects.all():
        boards.append({'code': i.code, 'name': i.name})
    return JsonResponse({'boards': boards})


def board_view(request, board_id):
    # Find board
    selected_board = Board.objects.get(pk=board_id)

    # Fint all threads
    threads = []
    for i in Thread.objects.filter(board=selected_board):
        threads.append({
            'id': i.id,
            'body': i.body,
        })

    return JsonResponse({
        'board': {
            'id': selected_board.id,
            'code': selected_board.code,
            'threads': threads,
        }
    })

def thread_view(request, thread_id):
    requested_thread = Thread.objects.get(pk=thread_id)

    # Find all replies
    replies = []
    for i in Reply.objects.filter(origin=requested_thread):
        # Find attachments
        attachments = []
        for j in Attachment.objects.filter(post=i):
            attachments.append(j.file.name)

        replies.append({
            'id': i.id,
            'body': i.body,
            'attachments': attachments,
        })

    return JsonResponse({
        'thread': {
            'id': requested_thread.id,
            'replies': replies,
        }
    })
