from flask import request

from sqlalchemy import Column, Integer, String

from shared.infrastructure.db.db import Base, SessionLocal

class Notification(Base):
    __tablename__ = "notifications"  # Matches Django’s table name
    __table_args__ = {"extend_existing": True}  # Avoid redefinition errors
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    type = Column(String, nullable=False)



def create_notification(title, type):
    notification = Notification(
        title=title,
        type=type,
    )
    db = SessionLocal()
    try:
        db.add(notification)
        db.commit()
        db.refresh(notification)

    finally:
        db.close()
    return {"title": title, "type": type}

def send_notification(message):
    print(f"Sending notification, {message}")

def message_queue_entrypoint():
    info = request.get_json()
    send_notification(info)
    create_notification(title=info, type="push")
    return {"msg" : "notification sent"}

