from django.contrib import admin
from messaging.models import Board, Thread, Reply, Attachment

# Register your models here.
admin.site.register(Board)
admin.site.register(Thread)
admin.site.register(Reply)
admin.site.register(Attachment)
