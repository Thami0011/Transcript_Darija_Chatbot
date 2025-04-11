from model.transcribe import speech_to_text
from model.darija_audio_transcript import darija_transcript
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")


def calculate_perplexity(text):
    """
    Compute the perplexity score of a text using GPT-2.
    """    
    encodings = tokenizer(text, return_tensors="pt")
    input_ids = encodings.input_ids
    with torch.no_grad():
        outputs = model(input_ids, labels=input_ids)
        loss = outputs.loss
    return torch.exp(loss).item()  # Convert log-loss to perplexity


def transcription_decision(path_to_file):
    """
    Returns the transcript of an audio file based on its perplexity.
    If the perplexity is higher than a certain threshold (100), it returns the transcript of the audio using the Darija model.
    """
    
    whisper_text, whisper_conf = speech_to_text(path_to_file)
    whisper_perplexity = calculate_perplexity(whisper_text)
    
    logger.info(f"Whisper Perplexity: {whisper_perplexity}")

    if whisper_perplexity < 150:
        logger.info("Transcription using Whisper")
        return whisper_text 
    else:
        logger.info("Transcription using Wav2Vec2")
        return darija_transcript(path_to_file)[0]

