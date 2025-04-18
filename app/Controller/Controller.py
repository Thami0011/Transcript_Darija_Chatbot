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



 
# # Utils
# def generate_response(request:str) -> str:

#     context_history.append({"role": "user", "content": request.prompt})

#     data = {
#         "model": "atlasai:9b",
#         "messages": context_history,
#     }

#     try:
#         # Send the request to the OLLAMA API
#         response = requests.post(OLLAMA_URL, json=data, stream=True)
#         response.raise_for_status()

#         full_response = ""
#         for line in response.iter_lines():
#             if line:
#                 fragment = json.loads(line)
#                 full_response += fragment.get("message", "content")
#                 if fragment.get("done", False):
#                     break
#         return full_response

#     except requests.exceptions.RequestException as e:
#         logger.error(f"Request failed: {e}")
#         raise HTTPException(status_code=500, detail=f"Erreur modèle : {str(e)}")


# def detect_and_translate(message: str) -> str:
#     translation = generate_response("Traduis cette phrase en francais : " + message, TRANSLATION_PROMPT)
#     # translation = message
#     # # Si la langue détectée est l’arabe, on applique une traduction personnalisée
#     # if langdetect.detect(translation) == "ar":
#     #     logger.info("Detected Arabic language, applying custom translation.")
#     #     translation = darija_english_translation(translation)
#     logger.info(f"Translation result: {translation}")
#     return translation


# Endpoints

@app.get("/")
async def ping_test():
    return {"message": "API is running"}


@app.post("/chat")
async def communicate_with_llama(request: RequestMessage):
    try:
        response_text = generate_response(request.prompt, keep_context=True)
        translated_text = generate_response(request.prompt)
        logger.info(f"Response generated: {response_text}")
        logger.info(f"Translation generated: {translated_text}")
        return {"response": response_text, "translation": translated_text}

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
        response_text = generate_response(user_input, keep_context=True)
        logger.info(f"Response generated: {response_text}")
        translated_text = generate_response(user_input)
        logger.info(f"Translation generated: {translated_text}")

        return {"response": response_text, "translation": translated_text, "transcription": user_input}

    except Exception as e:
        logger.error(f"Error processing voice message: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur traitement vocal : {str(e)}")
