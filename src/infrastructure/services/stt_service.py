import os
import whisper
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class WhisperSTTService:
    """
    Service xử lý Speech-to-Text sử dụng OpenAI Whisper (Local).
    """

    def __init__(self, model_name: str = "turbo"):
        # gợi ý: "small" cho chất lượng tốt hơn "base";
        # nếu máy yếu có thể để lại "base"
        self.model_name = model_name
        self._model = None

    @property
    def model(self):
        if self._model is None:
            logger.info(f"Loading Whisper model: {self.model_name}...")
            self._model = whisper.load_model(self.model_name)
            logger.info("Whisper model loaded successfully.")
        return self._model

    def transcribe(self, audio_path: str) -> Optional[str]:
        """
        Chuyển đổi file âm thanh sang văn bản tiếng Việt.
        """
        if not os.path.exists(audio_path):
            logger.error(f"Audio file not found: {audio_path}")
            return None

        try:
            logger.info(f"Transcribing audio: {audio_path}...")
            result = self.model.transcribe(
                audio_path,
                language="vi",
                task="transcribe",
                beam_size=5,
                temperature=0.0,
                condition_on_previous_text=False,
            )
            transcript = (result.get("text") or "").strip()
            logger.info(f"Transcription result: {transcript}")
            return transcript if transcript else None
        except Exception as e:
            logger.error(f"Error during transcription: {str(e)}")
            return None

# Singleton instance
stt_service = WhisperSTTService()