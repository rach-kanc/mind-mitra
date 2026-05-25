from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
import uuid

from app.models.sos import SOSAlert, SOSAlertCreate, AlertStatus, AlertSeverity
from app.models.user import User, EmergencyContact
from app.core.database import get_collection
from app.core.config import settings
from app.core.logging import get_logger
from app.services.notifications import NotificationService

logger = get_logger("sos")


class SOSService:
    """SOS alert service for emergency notifications"""
    
    def __init__(self):
        self.alerts_collection = get_collection("sos_alerts")
        self.users_collection = get_collection("users")
        self.notification_service = NotificationService()
    
    async def create_alert(self, user_id: str, alert_data: SOSAlertCreate) -> Optional[SOSAlert]:
        """Create a new SOS alert"""
        try:
            # Check if user has recent alerts (cooldown)
            if await self._has_recent_alert(user_id):
                logger.warning(f"User {user_id} has recent alert, cooldown active")
                return None
            
            # Create alert document
            alert_id = str(uuid.uuid4())
            now = datetime.utcnow()
            
            alert_doc = {
                "id": alert_id,
                "user_id": user_id,
                "trigger_type": alert_data.trigger_type,
                "severity": alert_data.severity,
                "reason": alert_data.reason,
                "emotion_data": alert_data.emotion_data,
                "status": AlertStatus.PENDING,
                "created_at": now,
                "updated_at": now,
                "sent_at": None,
                "acknowledged_at": None
            }
            
            result = await self.alerts_collection.insert_one(alert_doc)
            if result.inserted_id:
                alert = SOSAlert(**alert_doc)
                
                # Send notifications
                await self._send_notifications(alert)
                
                return alert
            
            return None
            
        except Exception as e:
            logger.error(f"Error creating SOS alert: {e}")
            return None
    
    async def get_user_alerts(self, user_id: str, page: int = 1, size: int = 20) -> List[SOSAlert]:
        """Get SOS alerts for a user"""
        try:
            skip = (page - 1) * size
            cursor = self.alerts_collection.find(
                {"user_id": user_id}
            ).sort("created_at", -1).skip(skip).limit(size)
            
            alerts = []
            async for doc in cursor:
                alerts.append(SOSAlert(**doc))
            
            return alerts
            
        except Exception as e:
            logger.error(f"Error getting user alerts: {e}")
            return []
    
    async def cancel_alert(self, alert_id: str, user_id: str) -> bool:
        """Cancel an SOS alert"""
        try:
            result = await self.alerts_collection.update_one(
                {"id": alert_id, "user_id": user_id, "status": AlertStatus.PENDING},
                {
                    "$set": {
                        "status": AlertStatus.CANCELLED,
                        "updated_at": datetime.utcnow()
                    }
                }
            )
            
            return result.modified_count > 0
            
        except Exception as e:
            logger.error(f"Error cancelling alert: {e}")
            return False
    
    async def acknowledge_alert(self, alert_id: str) -> bool:
        """Acknowledge an SOS alert (for emergency contacts)"""
        try:
            result = await self.alerts_collection.update_one(
                {"id": alert_id, "status": AlertStatus.SENT},
                {
                    "$set": {
                        "status": AlertStatus.ACKNOWLEDGED,
                        "acknowledged_at": datetime.utcnow(),
                        "updated_at": datetime.utcnow()
                    }
                }
            )
            
            return result.modified_count > 0
            
        except Exception as e:
            logger.error(f"Error acknowledging alert: {e}")
            return False
    
    async def check_emotional_distress(self, user_id: str, emotion_data: Dict[str, Any]) -> bool:
        """Check if user is in emotional distress and should trigger SOS"""
        try:
            # Get recent journal entries and emotion data
            recent_entries = await self._get_recent_emotion_data(user_id)
            
            # Check for critical emotions
            critical_emotions = ["depressed", "suicidal", "hopeless", "desperate"]
            negative_emotions = ["sad", "angry", "anxious", "fearful"]
            
            # Count negative emotions in recent data
            negative_count = 0
            for entry in recent_entries:
                if entry.get("dominant_emotion") in negative_emotions:
                    negative_count += 1
                
                # Check current emotion data
                if emotion_data.get("dominant_emotion") in critical_emotions:
                    return True
            
            # Check if multiple negative emotions detected recently
            if negative_count >= settings.DEPRESSION_FLAG_THRESHOLD:
                return True
            
            # Check current emotion confidence
            if emotion_data.get("confidence", 0) > settings.CRITICAL_EMOTION_THRESHOLD:
                if emotion_data.get("dominant_emotion") in negative_emotions:
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error checking emotional distress: {e}")
            return False
    
    async def _has_recent_alert(self, user_id: str) -> bool:
        """Check if user has recent SOS alert (cooldown)"""
        try:
            cooldown_time = datetime.utcnow() - timedelta(minutes=settings.SOS_COOLDOWN_MINUTES)
            
            recent_alert = await self.alerts_collection.find_one({
                "user_id": user_id,
                "created_at": {"$gte": cooldown_time},
                "status": {"$in": [AlertStatus.PENDING, AlertStatus.SENT]}
            })
            
            return recent_alert is not None
            
        except Exception as e:
            logger.error(f"Error checking recent alerts: {e}")
            return False
    
    async def _send_notifications(self, alert: SOSAlert):
        """Send notifications for SOS alert"""
        try:
            # Get user and emergency contacts
            user_doc = await self.users_collection.find_one({"id": alert.user_id})
            if not user_doc:
                logger.error(f"User not found for alert: {alert.user_id}")
                return
            
            user = User(**user_doc)
            
            # Update alert status to sent
            await self.alerts_collection.update_one(
                {"id": alert.id},
                {
                    "$set": {
                        "status": AlertStatus.SENT,
                        "sent_at": datetime.utcnow(),
                        "updated_at": datetime.utcnow()
                    }
                }
            )
            
            # Send notifications to emergency contacts
            for contact in user.emergency_contacts:
                await self._send_contact_notification(alert, user, contact)
            
            # Send notification to user
            await self._send_user_notification(alert, user)
            
            logger.info(f"SOS notifications sent for alert {alert.id}")
            
        except Exception as e:
            logger.error(f"Error sending SOS notifications: {e}")
    
    async def _send_contact_notification(self, alert: SOSAlert, user: User, contact: EmergencyContact):
        """Send notification to emergency contact"""
        try:
            message = f"URGENT: {user.name} has triggered an SOS alert. "
            message += f"Severity: {alert.severity.value}. "
            if alert.reason:
                message += f"Reason: {alert.reason}. "
            message += "Please check on them immediately."
            
            # Send SMS
            if contact.phone:
                await self.notification_service.send_sms(
                    to=contact.phone,
                    message=message
                )
            
            # Send email
            if contact.email:
                await self.notification_service.send_email(
                    to=contact.email,
                    subject=f"URGENT: {user.name} SOS Alert",
                    message=message
                )
                
        except Exception as e:
            logger.error(f"Error sending contact notification: {e}")
    
    async def _send_user_notification(self, alert: SOSAlert, user: User):
        """Send notification to user"""
        try:
            message = f"Your SOS alert has been sent to your emergency contacts. "
            message += "Help is on the way. Please stay safe."
            
            # Send push notification (placeholder)
            await self.notification_service.send_push_notification(
                user_id=user.id,
                title="SOS Alert Sent",
                message=message
            )
            
        except Exception as e:
            logger.error(f"Error sending user notification: {e}")
    
    async def _get_recent_emotion_data(self, user_id: str) -> List[Dict[str, Any]]:
        """Get recent emotion data from journal entries"""
        try:
            # Get journal entries from last 24 hours
            yesterday = datetime.utcnow() - timedelta(days=1)
            
            journal_collection = get_collection("journal_entries")
            cursor = journal_collection.find({
                "user_id": user_id,
                "created_at": {"$gte": yesterday}
            }).sort("created_at", -1)
            
            entries = []
            async for doc in cursor:
                entries.append({
                    "dominant_emotion": doc.get("emotion_labels", [{}])[0].get("label", "neutral") if doc.get("emotion_labels") else "neutral",
                    "mood_score": doc.get("mood_score", 0.5)
                })
            
            return entries
            
        except Exception as e:
            logger.error(f"Error getting recent emotion data: {e}")
            return []


# Global SOS service instance
sos_service = SOSService() 