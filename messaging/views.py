from django.http import JsonResponse
from messaging.models import Board, Thread, Reply, Attachment


def home(request):
    boards = [i.as_dict() for i in Board.objects.all()]
    return JsonResponse({ 'boards': boards })


def board_view(request, board_id):
    # Find board
    selected_board = Board.objects.get(pk=board_id)

    # Fint all threads
    threads = [i.as_dict() for i in Thread.objects.filter(board=selected_board)]

    return JsonResponse({
        'board': selected_board.as_dict(),
        'threads': threads,
    })


def thread_view(request, thread_id):
    requested_thread = Thread.objects.get(pk=thread_id)

    # Find all replies
    replies = []
    for i in Reply.objects.filter(origin=requested_thread):
        # Find attachments
        attachments = [a.as_dict() for a in Attachment.objects.filter(post=i)]

        replies.append({
            **i.as_dict(),
            'attachments': attachments,
        })

    return JsonResponse({
        'thread': requested_thread.as_dict(),
        'replies': replies,
    })
