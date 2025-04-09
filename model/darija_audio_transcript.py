import librosa
import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor

def darija_transcript(audio_file_path):
    
    """
    Transcribe Moroccan Darija audio to text using Wav2Vec2 model from HuggingFace.
    Accepts only .wav files.
    Args:
        audio_file_path (str): Path to the audio file.
    Returns:
        tuple: (Transcribed text, Confidence score of the transcription)
    """
    
    # Load tokenizer and processor
    # tokenizer = Wav2Vec2CTCTokenizer.from_pretrained("darija_transcript", unk_token="[UNK]", pad_token="[PAD]", word_delimiter_token="|")
    processor = Wav2Vec2Processor.from_pretrained("boumehdi/wav2vec2-large-xlsr-moroccan-darija")
    model = Wav2Vec2ForCTC.from_pretrained("boumehdi/wav2vec2-large-xlsr-moroccan-darija")

    # Load audio file
    input_audio, _ = librosa.load(audio_file_path, sr=16000)

    # Tokenize input
    input_values = processor(input_audio, return_tensors="pt", padding=True).input_values

    with torch.no_grad():
        logits = model(input_values).logits  # Raw predictions

    # Compute softmax probabilities
    probabilities = torch.nn.functional.softmax(logits, dim=-1)
    max_probs, _ = torch.max(probabilities, dim=-1)  # Confidence per token
    avg_confidence = torch.mean(max_probs).item()  # Overall confidence score

    # Decode predicted tokens
    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = processor.batch_decode(predicted_ids)
     
    return transcription[0], avg_confidence