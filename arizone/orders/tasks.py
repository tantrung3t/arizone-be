import logging
from django.conf import settings
from arizone.celery import app

from bases.services.firebase import notification
from accounts.models import BusinessUser

@app.task()
def SendNotify(business):
    queryset = BusinessUser.objects.get(id=business)
    notification.send_notify_message(
        user_id=queryset.user.id, msg_title=queryset.user.full_name, msg_body="Bạn có đơn hàng mới!")