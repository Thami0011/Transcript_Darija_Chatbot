from whisper import load_model, transcribe
from whisper.audio import load_audio

def speech_to_text(audio_file_path: str):
    # Load the audio file
    audio_array = load_audio(audio_file_path)
    
    # Load the Whisper model (you can specify a model size like "base", "small", "medium", etc.)
    model = load_model("base")

    # Transcribe the audio
    result = transcribe(model, audio=audio_array,language="fr", task="transcribe")
    avg_confidence = sum([x["avg_logprob"] for x in result["segments"]]) / len(result["segments"])
    
    # Convert log probability to confidence (0 to 1)
    whisper_conf = (1 + avg_confidence) / 2  # Normalize logprob (-1 to 0) to (0 to 1)
    
    # Return the transcribed text and confidence score
    return result["text"], whisper_conf


