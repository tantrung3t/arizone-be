from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message, Notification


def send_notify_message(user_id, msg_title, msg_body):
    device = get_device_user(user_id)
    message = Message(
        notification=Notification(
            title=msg_title, body=msg_body
        )
    )
    device.send_message(message)


def get_device_user(user_id):
    device = FCMDevice.objects.filter(user=user_id, active=True)
    return device
