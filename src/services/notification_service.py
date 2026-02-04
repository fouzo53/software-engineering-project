from typing import List, Dict
from src.infrastructure.databases.database import db
from src.infrastructure.models.notification_model import Notification

class NotificationService:
    def create_notification(self, title: str, message: str, user_id: int = None, type: str = 'info') -> Dict:
        try:
            notification = Notification(
                title=title,
                message=message,
                user_id=user_id,
                type=type
            )
            db.session.add(notification)
            db.session.commit()
            return {"success": True, "notification": notification.to_dict()}
        except Exception as e:
            db.session.rollback()
            return {"success": False, "message": str(e)}

    def get_notifications(self, user_id: int, unread_only: bool = False) -> List[Dict]:
        from sqlalchemy import or_
        query = Notification.query.filter(or_(Notification.user_id == user_id, Notification.user_id == None))
        
        if unread_only:
            query = query.filter_by(is_read=False)
            
        notifications = query.order_by(Notification.created_at.desc()).all()
        return [n.to_dict() for n in notifications]

    def mark_read(self, notification_id: int, user_id: int) -> Dict:
        from sqlalchemy import or_
        notification = Notification.query.filter(
            Notification.id == notification_id,
            or_(Notification.user_id == user_id, Notification.user_id == None)
        ).first()
        
        if not notification:
            return {"success": False, "message": "Notification not found"}
            
        notification.is_read = True
        db.session.commit()
        return {"success": True}
        
    def mark_all_read(self, user_id: int) -> Dict:
        from sqlalchemy import or_
        notifications = Notification.query.filter(
            or_(Notification.user_id == user_id, Notification.user_id == None),
            Notification.is_read == False
        ).all()
        for n in notifications:
            n.is_read = True
        db.session.commit()
        return {"success": True, "count": len(notifications)}
