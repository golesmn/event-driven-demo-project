from flask import request

def send_notification(message):
    print(f"Sending notification, {message}")

def message_queue_entrypoint():
    info = request.get_json()
    send_notification(info)
    return {"msg" : "notification sent"}

