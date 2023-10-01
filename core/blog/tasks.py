from celery import shared_task

from .models import Comment


@shared_task
def delete_rejected_comments():
    return Comment.objects.filter(approved=False).delete()
