"""Keep the original task-two import available after packaging."""

from EmotionDetection.emotion_detection import emotion_detector

__all__ = ["emotion_detector"]
