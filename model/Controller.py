from fastapi import FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import requests
import langdetect
import json
import os
import logging

from translate import translate_darija_to_french
from transcript_decision import transcription_decision

# Logging Configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Configuration
OLLAMA_URL = "http://localhost:11434/api/generate"
TEMP_DIR = Path("temp")
TEMP_DIR.mkdir(exist_ok=True)

# FastAPI app initialization
app = FastAPI(logger.info("FastAPI app initialized"))

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

# Prompts système
MAIN_SYSTEM_PROMPT = (
    """"
You are a chatbot assistant in AttijariWafaBank, a leading bank in Morocco. Your role is to assist the user with banking-related issues, answer questions about services, and handle any problems or suggestions the user might have in the context of banking. You should always maintain a professional and helpful tone while providing relevant information.

User Instruction:

If the user’s request relates to banking services, financial inquiries, or any relevant issue within the scope of the bank, respond appropriately and assist them.

If the request does not relate to banking or financial services, respond with the following message: "Désolé, je ne peux pas vous assister en ceci !"

Behavior Guidelines:

Always stay within the scope of banking and financial services.

Handle user queries related to accounts, loans, transactions, banking products, etc.

Offer guidance on the usage of mobile banking apps, online services, and any updates related to the bank’s offerings.

If the query is outside the scope, politely redirect the user with the specified phrase: "Désolé, je ne peux pas vous assister en ceci !"

Examples:

User Request: "Comment puis-je ouvrir un compte courant chez AttijariWafaBank ?" Response: "Pour ouvrir un compte courant chez AttijariWafaBank, vous pouvez vous rendre dans l'une de nos agences ou vous inscrire directement via notre application mobile. Avez-vous besoin d’aide pour cela ?"

User Request: "Quels sont les taux d'intérêt pour les prêts immobiliers ?" Response: "Les taux d'intérêt pour les prêts immobiliers chez AttijariWafaBank varient en fonction du montant et de la durée du prêt. Je peux vous fournir plus de détails ou vous orienter vers notre équipe spécialisée si vous le souhaitez."

User Request: "J'ai des questions sur les crypto-monnaies." Response: "Désolé, je ne peux pas vous assister en ceci !"""""

)

TRANSLATION_PROMPT = "Traduis le texte en francais, quelque soit la langue source."

# Utils
def generate_response(prompt: str, system_prompt: str) -> str:
    data = {
        "model": "atlasai:9b",
        "prompt": prompt,
        "system": system_prompt
    }

    try:
        response = requests.post(OLLAMA_URL, json=data, stream=True)
        response.raise_for_status()

        full_response = ""
        for line in response.iter_lines():
            if line:
                fragment = json.loads(line)
                full_response += fragment.get("response", "")
                if fragment.get("done", False):
                    break
        logger.info(f"Response generated: {full_response}")
        return full_response

    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur modèle : {str(e)}")


def detect_and_translate(message: str) -> str:
    translation = generate_response(message, TRANSLATION_PROMPT)

    # Si la langue détectée est l’arabe, on applique une traduction personnalisée
    if langdetect.detect(translation) == "ar":
        logger.info("Detected Arabic language, applying custom translation.")
        translation = translate_darija_to_french(translation)
    logger.info(f"Translation result: {translation}")
    return translation


# Endpoints
@app.post("/chat")
async def communicate_with_llama(request: RequestMessage):
    try:
        response_text = generate_response(request.prompt, MAIN_SYSTEM_PROMPT)
        translated_text = detect_and_translate(request.prompt)

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

        # Transcription
        user_input = str(transcription_decision(file_path))

        # Nettoyage du fichier
        os.remove(file_path)
        logger.info(f"Temporary file {file_path} deleted and removed.")

        # Génération de réponse et traduction
        response_text = generate_response(user_input, MAIN_SYSTEM_PROMPT)
        translated_text = detect_and_translate(user_input)

        return {"response": response_text, "translation": translated_text}

    except Exception as e:
        logger.error(f"Error processing voice message: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur traitement vocal : {str(e)}")
