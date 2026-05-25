from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class EmotionResult(BaseModel):
    label: str = Field(..., min_length=1, max_length=50)
    confidence: float = Field(..., ge=0.0, le=1.0)
    score: Optional[float] = Field(None, ge=-1.0, le=1.0)


class TextAnalysisRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=2000)


class TextAnalysisResponse(BaseModel):
    emotions: List[EmotionResult]
    sentiment: str  # positive, negative, neutral
    sentiment_score: float
    dominant_emotion: str
    confidence: float


class AudioAnalysisRequest(BaseModel):
    audio_data: str  # Base64 encoded audio
    audio_format: str = "wav"


class AudioAnalysisResponse(BaseModel):
    emotions: List[EmotionResult]
    dominant_emotion: str
    confidence: float
    audio_features: Optional[Dict[str, Any]] = {}


class ImageAnalysisRequest(BaseModel):
    image_data: str  # Base64 encoded image
    image_format: str = "jpeg"


class ImageAnalysisResponse(BaseModel):
    emotions: List[EmotionResult]
    dominant_emotion: str
    confidence: float
    face_detected: bool
    face_features: Optional[Dict[str, Any]] = {}


class MultiModalAnalysisRequest(BaseModel):
    text: Optional[str] = None
    audio_data: Optional[str] = None
    image_data: Optional[str] = None


class MultiModalAnalysisResponse(BaseModel):
    text_analysis: Optional[TextAnalysisResponse] = None
    audio_analysis: Optional[AudioAnalysisResponse] = None
    image_analysis: Optional[ImageAnalysisResponse] = None
    combined_emotion: str
    combined_confidence: float
    risk_level: str  # low, medium, high, critical 