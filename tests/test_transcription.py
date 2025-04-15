
import unittest
from unittest.mock import patch
from app.model.transcript_decision import calculate_perplexity, transcription_decision

class TestTranscription(unittest.TestCase):

    @patch("app.model.transcript_decision.tokenizer")
    @patch("app.model.transcript_decision.model")
    def test_calculate_perplexity(self, mock_model, mock_tokenizer):
        mock_tokenizer.return_value = {"input_ids": "dummy_tensor"}
        mock_model.return_value.__call__.return_value.loss = 2.0

        with patch("torch.no_grad"):
            result = calculate_perplexity("test")
            self.assertIsInstance(result, float)

    @patch("app.model.transcript_decision.calculate_perplexity", return_value=50)
    @patch("app.model.transcript_decision.speech_to_text", return_value="normal transcript")
    def test_transcription_decision(self, mock_speech, mock_perplex):
        transcript = transcription_decision("some_audio.wav")
        self.assertEqual(transcript, "normal transcript")
