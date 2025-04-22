from fastapi import FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import os
import logging

from utils import *
from app.model.transcript_decision import transcription_decision


# Logging Configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Configuration
OLLAMA_URL = "http://localhost:11434/api/chat"
OLLAMA_URL_GENNERATION = "http://localhost:11434/api/generate"
TEMP_DIR = Path("app\\model\\temp")
TEMP_DIR.mkdir(exist_ok=True)



# FastAPI app initialization
app = FastAPI()
logger.info("FastAPI app initialized")
# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class VoiceMessage(BaseModel):
    record: UploadFile = File(...)

class RequestMessage(BaseModel):
    prompt: str



# Endpoints

@app.get("/")
async def ping_test():
    return {"message": "API is running"}


@app.post("/chat")
async def communicate_with_llama(request: RequestMessage):
    try:
        # response_text = generate_response(request.prompt, keep_context=True)
        translated_text = generate_response(request.prompt)
        # logger.info(f"Response generated: {response_text}")
        logger.info(f"Translation generated: {translated_text}")
        # return {"response": response_text, "translation": translated_text}
        return {"translation": translated_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/voice")
async def communicate_with_voice(record: UploadFile = File(...)):
    try:
        # Lire et sauvegarder temporairement le fichier
        file_content = await record.read()
        file_path = TEMP_DIR / record.filename

        with open(file_path, "wb") as f:
            f.write(file_content)
            logger.info(f"File saved to {file_path}")
            logger.warning("File should be deleted after processing.")

        logger.info("Starting transcription...")

        # Transcription
        user_input = str(transcription_decision(file_path))

        if user_input:
            os.remove(file_path)
            logger.info(f"Temporary file {file_path} deleted.")

        # Génération de réponse et traduction
        # response_text = generate_response(user_input, keep_context=True)
        # logger.info(f"Response generated: {response_text}")
        translated_text = generate_response(user_input)
        logger.info(f"Translation generated: {translated_text}")

        # return {"response": response_text, "translation": translated_text, "transcription": user_input}
        return {"translation": translated_text, "transcription": user_input}
    except Exception as e:
        logger.error(f"Error processing voice message: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur traitement vocal : {str(e)}")
