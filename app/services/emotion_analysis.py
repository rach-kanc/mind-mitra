import base64
import io
import numpy as np
from typing import List, Dict, Any, Optional
from PIL import Image
import cv2
import librosa
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import pipeline
import torch

from app.models.analysis import (
    EmotionResult, TextAnalysisResponse, AudioAnalysisResponse, 
    ImageAnalysisResponse, MultiModalAnalysisResponse
)
from app.core.logging import get_logger

logger = get_logger("emotion_analysis")


class EmotionAnalysisService:
    """Service for emotion analysis using AI models"""
    
    def __init__(self):
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        self.text_classifier = None
        self.audio_classifier = None
        self.image_classifier = None
        
        # Initialize models
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize AI models"""
        try:
            # Text classification model (emotion detection)
            self.text_classifier = pipeline(
                "text-classification",
                model="j-hartmann/emotion-english-distilroberta-base",
                return_all_scores=True
            )
            logger.info("Text emotion model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load text emotion model: {e}")
        
        try:
            # Audio emotion classification (placeholder - would need specific audio model)
            logger.info("Audio emotion model placeholder initialized")
        except Exception as e:
            logger.error(f"Failed to load audio emotion model: {e}")
    
    def analyze_text(self, text: str) -> TextAnalysisResponse:
        """Analyze text for emotions and sentiment"""
        try:
            # VADER sentiment analysis
            vader_scores = self.sentiment_analyzer.polarity_scores(text)
            sentiment_score = vader_scores['compound']
            
            # Determine sentiment label
            if sentiment_score >= 0.05:
                sentiment = "positive"
            elif sentiment_score <= -0.05:
                sentiment = "negative"
            else:
                sentiment = "neutral"
            
            # Emotion classification using transformer model
            emotions = []
            if self.text_classifier:
                try:
                    emotion_results = self.text_classifier(text)[0]
                    for result in emotion_results:
                        emotions.append(EmotionResult(
                            label=result['label'],
                            confidence=result['score'],
                            score=sentiment_score
                        ))
                except Exception as e:
                    logger.error(f"Text emotion classification failed: {e}")
            
            # Fallback emotions based on sentiment
            if not emotions:
                if sentiment == "positive":
                    emotions = [EmotionResult(label="happy", confidence=0.7, score=sentiment_score)]
                elif sentiment == "negative":
                    emotions = [EmotionResult(label="sad", confidence=0.7, score=sentiment_score)]
                else:
                    emotions = [EmotionResult(label="neutral", confidence=0.7, score=sentiment_score)]
            
            # Find dominant emotion
            dominant_emotion = max(emotions, key=lambda x: x.confidence)
            
            return TextAnalysisResponse(
                emotions=emotions,
                sentiment=sentiment,
                sentiment_score=sentiment_score,
                dominant_emotion=dominant_emotion.label,
                confidence=dominant_emotion.confidence
            )
            
        except Exception as e:
            logger.error(f"Text analysis error: {e}")
            # Return default response
            return TextAnalysisResponse(
                emotions=[EmotionResult(label="neutral", confidence=0.5, score=0.0)],
                sentiment="neutral",
                sentiment_score=0.0,
                dominant_emotion="neutral",
                confidence=0.5
            )
    
    def analyze_audio(self, audio_data: str, audio_format: str = "wav") -> AudioAnalysisResponse:
        """Analyze audio for emotion detection"""
        try:
            # Decode base64 audio
            audio_bytes = base64.b64decode(audio_data)
            audio_array, sample_rate = librosa.load(io.BytesIO(audio_bytes), sr=None)
            
            # Extract audio features
            features = self._extract_audio_features(audio_array, sample_rate)
            
            # Simple emotion classification based on features
            emotions = self._classify_audio_emotion(features)
            
            # Find dominant emotion
            dominant_emotion = max(emotions, key=lambda x: x.confidence)
            
            return AudioAnalysisResponse(
                emotions=emotions,
                dominant_emotion=dominant_emotion.label,
                confidence=dominant_emotion.confidence,
                audio_features=features
            )
            
        except Exception as e:
            logger.error(f"Audio analysis error: {e}")
            return AudioAnalysisResponse(
                emotions=[EmotionResult(label="neutral", confidence=0.5)],
                dominant_emotion="neutral",
                confidence=0.5,
                audio_features={}
            )
    
    def analyze_image(self, image_data: str, image_format: str = "jpeg") -> ImageAnalysisResponse:
        """Analyze image for facial emotion detection"""
        try:
            # Decode base64 image
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))
            
            # Convert to OpenCV format
            cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            # Detect faces and emotions
            emotions, face_detected = self._detect_facial_emotions(cv_image)
            
            if not emotions:
                emotions = [EmotionResult(label="neutral", confidence=0.5)]
            
            # Find dominant emotion
            dominant_emotion = max(emotions, key=lambda x: x.confidence)
            
            return ImageAnalysisResponse(
                emotions=emotions,
                dominant_emotion=dominant_emotion.label,
                confidence=dominant_emotion.confidence,
                face_detected=face_detected,
                face_features={}
            )
            
        except Exception as e:
            logger.error(f"Image analysis error: {e}")
            return ImageAnalysisResponse(
                emotions=[EmotionResult(label="neutral", confidence=0.5)],
                dominant_emotion="neutral",
                confidence=0.5,
                face_detected=False,
                face_features={}
            )
    
    def analyze_multimodal(self, text: Optional[str] = None, 
                          audio_data: Optional[str] = None,
                          image_data: Optional[str] = None) -> MultiModalAnalysisResponse:
        """Analyze multiple modalities and combine results"""
        text_analysis = None
        audio_analysis = None
        image_analysis = None
        
        # Analyze each modality
        if text:
            text_analysis = self.analyze_text(text)
        
        if audio_data:
            audio_analysis = self.analyze_audio(audio_data)
        
        if image_data:
            image_analysis = self.analyze_image(image_data)
        
        # Combine results
        combined_emotion, combined_confidence, risk_level = self._combine_emotions(
            text_analysis, audio_analysis, image_analysis
        )
        
        return MultiModalAnalysisResponse(
            text_analysis=text_analysis,
            audio_analysis=audio_analysis,
            image_analysis=image_analysis,
            combined_emotion=combined_emotion,
            combined_confidence=combined_confidence,
            risk_level=risk_level
        )
    
    def _extract_audio_features(self, audio_array: np.ndarray, sample_rate: int) -> Dict[str, float]:
        """Extract audio features for emotion classification"""
        features = {}
        
        try:
            # Spectral features
            spectral_centroids = librosa.feature.spectral_centroid(y=audio_array, sr=sample_rate)[0]
            spectral_rolloff = librosa.feature.spectral_rolloff(y=audio_array, sr=sample_rate)[0]
            
            # MFCC features
            mfccs = librosa.feature.mfcc(y=audio_array, sr=sample_rate, n_mfcc=13)
            
            # Pitch features
            pitches, magnitudes = librosa.piptrack(y=audio_array, sr=sample_rate)
            
            features = {
                "spectral_centroid_mean": float(np.mean(spectral_centroids)),
                "spectral_rolloff_mean": float(np.mean(spectral_rolloff)),
                "mfcc_mean": float(np.mean(mfccs)),
                "pitch_mean": float(np.mean(pitches[magnitudes > 0.1])),
                "energy": float(np.mean(librosa.feature.rms(y=audio_array)[0]))
            }
        except Exception as e:
            logger.error(f"Audio feature extraction error: {e}")
        
        return features
    
    def _classify_audio_emotion(self, features: Dict[str, float]) -> List[EmotionResult]:
        """Classify emotions based on audio features"""
        emotions = []
        
        try:
            # Simple rule-based classification
            energy = features.get("energy", 0)
            pitch = features.get("pitch_mean", 0)
            
            if energy > 0.1 and pitch > 200:
                emotions.append(EmotionResult(label="excited", confidence=0.7))
            elif energy < 0.05:
                emotions.append(EmotionResult(label="sad", confidence=0.6))
            elif pitch > 300:
                emotions.append(EmotionResult(label="anxious", confidence=0.6))
            else:
                emotions.append(EmotionResult(label="neutral", confidence=0.5))
                
        except Exception as e:
            logger.error(f"Audio emotion classification error: {e}")
            emotions.append(EmotionResult(label="neutral", confidence=0.5))
        
        return emotions
    
    def _detect_facial_emotions(self, image: np.ndarray) -> tuple[List[EmotionResult], bool]:
        """Detect facial emotions using OpenCV and basic image processing"""
        emotions = []
        face_detected = False
        
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Load face cascade
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            
            # Detect faces
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            
            if len(faces) > 0:
                face_detected = True
                
                # Simple emotion classification based on face region
                for (x, y, w, h) in faces:
                    face_roi = gray[y:y+h, x:x+w]
                    
                    # Basic features (placeholder for more sophisticated analysis)
                    brightness = np.mean(face_roi)
                    
                    if brightness > 150:
                        emotions.append(EmotionResult(label="happy", confidence=0.6))
                    elif brightness < 100:
                        emotions.append(EmotionResult(label="sad", confidence=0.6))
                    else:
                        emotions.append(EmotionResult(label="neutral", confidence=0.5))
            
            if not emotions:
                emotions.append(EmotionResult(label="neutral", confidence=0.5))
                
        except Exception as e:
            logger.error(f"Facial emotion detection error: {e}")
            emotions.append(EmotionResult(label="neutral", confidence=0.5))
        
        return emotions, face_detected
    
    def _combine_emotions(self, text_analysis: Optional[TextAnalysisResponse],
                         audio_analysis: Optional[AudioAnalysisResponse],
                         image_analysis: Optional[ImageAnalysisResponse]) -> tuple[str, float, str]:
        """Combine emotions from multiple modalities"""
        
        emotions = []
        confidences = []
        
        # Collect emotions from each modality
        if text_analysis:
            emotions.append(text_analysis.dominant_emotion)
            confidences.append(text_analysis.confidence)
        
        if audio_analysis:
            emotions.append(audio_analysis.dominant_emotion)
            confidences.append(audio_analysis.confidence)
        
        if image_analysis:
            emotions.append(image_analysis.dominant_emotion)
            confidences.append(image_analysis.confidence)
        
        if not emotions:
            return "neutral", 0.5, "low"
        
        # Find most common emotion
        emotion_counts = {}
        for emotion in emotions:
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        combined_emotion = max(emotion_counts, key=emotion_counts.get)
        combined_confidence = np.mean(confidences) if confidences else 0.5
        
        # Determine risk level
        negative_emotions = ["sad", "angry", "anxious", "depressed"]
        if combined_emotion in negative_emotions and combined_confidence > 0.7:
            risk_level = "high"
        elif combined_emotion in negative_emotions and combined_confidence > 0.5:
            risk_level = "medium"
        else:
            risk_level = "low"
        
        return combined_emotion, combined_confidence, risk_level


# Global emotion analysis service instance
emotion_service = EmotionAnalysisService() 