import frappe


class AIService:
    def __init__(self):
        self.api_key = frappe.conf.get("OPENAI_API_KEY")
        if not self.api_key:
            frappe.log_error("OPENAI_API_KEY not found — AIService running in mock mode")

    def analyze_audio(self, audio_url, context="general"):
        """
        Transcribes and analyzes audio for feedback.
        NOTE: Currently returns mock response — real Whisper/GPT-4 implementation pending.
        """
        if not self.api_key:
            return {
                "is_mock": True,
                "transcription": "[Mock] Transcription not available — OPENAI_API_KEY not configured.",
                "feedback": "[Mock] Configure OPENAI_API_KEY to enable real audio analysis.",
                "score": 0,
            }

        # A-07 fix: lazy import to avoid ImportError if openai is not installed
        try:
            import openai  # noqa: F401
        except ImportError:
            frappe.log_error("openai package not installed — run: pip install openai>=1.0")
            return {"is_mock": True, "error": "openai package not installed"}

        # Real implementation: download audio_url -> send to Whisper -> analyze with GPT-4
        # TODO: Implement real Whisper + GPT-4 audio analysis
        return {
            "is_mock": True,
            "transcription": "Real transcription coming soon.",
            "feedback": "Real phonetic feedback coming soon.",
            "score": 0,
        }

    def get_phonetic_feedback(self, text_expected, audio_url):
        """
        Detailed phonetic analysis between expected text and audio.
        NOTE: Currently returns mock response — real implementation pending.
        """
        if not self.api_key:
            return {"is_mock": True, "error": "AI Service not configured"}

        # TODO: Implement using a specialized speech-to-phoneme API or GPT-4o-audio
        return {
            "is_mock": True,
            "expected_phonetic": "/hɛˈloʊ ˈwɜrld/",
            "actual_phonetic": "[not analyzed yet]",
            "mistakes": [],
            "score": 0,
            "improvement_tip": "Real phonetic analysis coming soon.",
        }
