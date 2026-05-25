from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum


class AlertSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AlertStatus(str, Enum):
    PENDING = "pending"
    SENT = "sent"
    CANCELLED = "cancelled"
    ACKNOWLEDGED = "acknowledged"


class TriggerType(str, Enum):
    AUTOMATIC = "automatic"
    MANUAL = "manual"


class SOSAlertBase(BaseModel):
    trigger_type: TriggerType
    severity: AlertSeverity
    reason: Optional[str] = Field(None, max_length=500)
    emotion_data: Optional[Dict[str, Any]] = {}


class SOSAlertCreate(SOSAlertBase):
    pass


class SOSAlert(SOSAlertBase):
    id: str
    user_id: str
    status: AlertStatus
    created_at: datetime
    updated_at: datetime
    sent_at: Optional[datetime] = None
    acknowledged_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class SOSAlertList(BaseModel):
    alerts: list[SOSAlert]
    total: int
    page: int
    size: int


class SOSAlertResponse(BaseModel):
    alert_id: str
    status: AlertStatus
    message: str 