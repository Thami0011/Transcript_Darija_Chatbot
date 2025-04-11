import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
OLLAMA_URL_GENERATION = "http://localhost:11434/api/generate"

# Variable globale pour l'historique du contexte
context_history = []

def read_file(path: str) -> str:
    """
    Lit le contenu d’un fichier texte.
    Args:
        path (str): Chemin du fichier.
    Returns:
        str: Contenu du fichier.
    """
    with open(path, "r", encoding="utf-8") as file:
        return file.read()

def generate_response(prompt: str, keep_context: bool = False) -> str:
    """
    Génère une réponse du modèle en fonction du prompt donné.
    Args:
        prompt (str): Le prompt à envoyer au modèle.
        keep_context (bool, optional): Si True, le contexte est conservé dans le chat. Par défaut False.
    Returns:
        str: Réponse du modèle ou message d'erreur.
    """
    if keep_context:
        try:
            # Ajoute le message système une seule fois
            if not context_history or context_history[0]["role"] != "system":
                system_prompt = read_file("app\\Prompts\\MAIN_REQUEST_PROMPT.txt")
                context_history.insert(0, {"role": "system", "content": system_prompt})
            
            context_history.append({"role": "user", "content": prompt})
            
            data = {
                "model": "atlasai:9b",
                "messages": context_history,
                "stream": False
            }

            response = requests.post(OLLAMA_URL, json=data)
            response.raise_for_status()
            return response.json().get("message", {}).get("content", "No content received.")

        except requests.exceptions.RequestException as e:
            return f"[Error - Context]: {e}"

    else:
        try:
            system_prompt = read_file("app\\Prompts\\TRANSLATION_PROMPT.txt")

            data = {
                "model": "atlasai:9b",
                "system": system_prompt,
                "prompt": prompt,
                "stream": False
            }

            response = requests.post(OLLAMA_URL_GENERATION, json=data)
            response.raise_for_status()
            return response.json().get("response", "No response content.")

        except requests.exceptions.RequestException as e:
            return f"[Error - No Context]: {e}"
