import os
import whisper
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class WhisperSTTService:
    """
    Service xử lý Speech-to-Text sử dụng OpenAI Whisper (Local).
    """

    def __init__(self, model_name: str = "base"):
        self.model_name = model_name
        self._model = None

    @property
    def model(self):
        if self._model is None:
            logger.info(f"Loading Whisper model: {self.model_name}...")
            # Load model vào CPU/GPU tùy thuộc vào phần cứng có sẵn
            self._model = whisper.load_model(self.model_name)
            logger.info("Whisper model loaded successfully.")
        return self._model

    def transcribe(self, audio_path: str) -> Optional[str]:
        """
        Chuyển đổi file âm thanh sang văn bản.
        :param audio_path: Đường dẫn đến file âm thanh (mp3, wav, m4a, ...)
        :return: Văn bản đã transcribe hoặc None nếu lỗi
        """
        if not os.path.exists(audio_path):
            logger.error(f"Audio file not found: {audio_path}")
            return None

        try:
            logger.info(f"Transcribing audio: {audio_path}...")
            result = self.model.transcribe(audio_path, language="vi")
            transcript = result.get("text", "").strip()
            logger.info(f"Transcription result: {transcript}")
            return transcript
        except Exception as e:
            logger.error(f"Error during transcription: {str(e)}")
            return None

# Singleton instance
stt_service = WhisperSTTService(model_name="base")
