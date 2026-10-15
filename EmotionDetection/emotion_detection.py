"""Detect emotions using the IBM Skills Network Watson NLP service."""

import json

import requests

URL = (
    "https://sn-watson-emotion.labs.skills.network/v1/"
    "watson.runtime.nlp.v1/NlpService/EmotionPredict"
)
HEADERS = {
    "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
}
EMOTIONS = ("anger", "disgust", "fear", "joy", "sadness")


def emotion_detector(text_to_analyze):
    """Return five emotion scores and the highest-scoring emotion.

    Blank input and HTTP 400 return None for every field. Other service
    failures propagate to the caller instead of becoming invented scores.
    """
    empty_result = dict.fromkeys((*EMOTIONS, "dominant_emotion"))
    if not text_to_analyze or not text_to_analyze.strip():
        return empty_result
    response = requests.post(
        URL,
        headers=HEADERS,
        json={"raw_document": {"text": text_to_analyze}},
        timeout=30,
    )
    if response.status_code == 400:
        return empty_result
    response.raise_for_status()
    payload = json.loads(response.text)
    scores = payload["emotionPredictions"][0]["emotion"]
    result = {emotion: scores[emotion] for emotion in EMOTIONS}
    result["dominant_emotion"] = max(result, key=result.get)
    return result
