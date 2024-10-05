from schemas.notification_schema import Notification
from database import NotificationModel
from fastapi import APIRouter, Body, HTTPException

notification_route = APIRouter()

@notification_route.post("/")
async def create_notification(notification: Notification = Body(...)):
    """Create a new notification."""
    NotificationModel.create(
        user_id=notification.user_id,
        message=notification.message,
        is_read=notification.is_read
    )
    return {"message": "Notification created successfully"}

@notification_route.get("/")
async def read_all_notifications():
    """Retrieve a list of all notifications."""
    notifications = NotificationModel.select().dicts()
    return list(notifications)

@notification_route.get("/{notification_id}")
async def read_notification(notification_id: int):
    """Retrieve a specific notification by its ID."""
    try:
        notification = NotificationModel.get(NotificationModel.id == notification_id)
        return notification
    except Exception as exc:
        raise HTTPException(status_code=404, detail="Notification not found") from exc

@notification_route.put("/{notification_id}")
async def update_notification(notification_id: int, notification: Notification = Body(...)):
    """Update an existing notification."""
    try:
        existing_notification = NotificationModel.get(NotificationModel.id == notification_id)
        existing_notification.user_id = notification.user_id
        existing_notification.message = notification.message
        existing_notification.is_read = notification.is_read
        existing_notification.save()
        return {"message": "Notification updated successfully"}
    except Exception as exc:
        raise HTTPException(status_code=404, detail="Notification not found") from exc

@notification_route.delete("/{notification_id}")
async def delete_notification(notification_id: int):
    """Delete a notification by its ID."""
    rows_deleted = NotificationModel.delete().where(NotificationModel.id == notification_id).execute()
    if rows_deleted:
        return {"message": "Notification deleted successfully"}
    raise HTTPException(status_code=404, detail="Notification not found")
