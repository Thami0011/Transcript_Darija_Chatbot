# Darija Transcript chatbot 🤖

This project is an intelligent chatbot designed to understand and respond to user queries in Darija (Moroccan Arabic). It combines automatic speech recognition (ASR), natural language understanding, and AI-powered classification to assist users in a banking context **_AttijariWafaBank_**.

#### The chatbot is capable of:

- Understanding different languages like French, English, Standard Arabic, Morrocan Darija Arabic ...
- Taking as an input both Text messages and Audio messades. _wav format_
- Interpreting data to respond within a banking context.
- Denying every inference not related to the banking system with a user friendly prompt.

#### The app uses :

- FastAPI to deploy the app with different endpoints.
- Ollama to send requests via its API.
- ATLASAI as an LLM model to understand and respond in Darija Dialect.
- Python-Based ASR models like Whisper and Wav2Vac2 to transcribe audio files.

As a basic understanding of how the app works, it accepts both text and voice messages via :

#### 🚀 Endpoints

> **_/chat_**
> POST method that accepts a body request JSON:
> `{"prompt":"textPrompt"}`

> **_/voice_**
> POST method that acepts as a body request a JSON:
> `{"record":MultipartFile}`

---

## 📄 Installation

###### 📍 Local Installation

Requirements :

- Python3.12
- FFMPEG
- OLLAMA

1. (OPTIONNAL) **Create a Python Virtual Environment :**

   > Start by creating a python virtual environment to separate diffenrent project dipedencies from your local Python dependencies, with the command `python -m venv path_and_name_of_your_venv`

2. **Copy the project to you local environment :**

   > Inside your working directory, run the command `git clone https://github.com/Thami0011/Transcript_Darija_Chatbot.git` to download the project locally.

3. **Install dependencies :**

   > To install them all at one, use the command:
   > `pip install -r requirements.txt` or `python3 -m pip install -r requirements.txt`

4. **Add ATLASAI model to OLLAMA**

   > The app communicates with a model named AtlasAI, to use it, you need to download it and add it to OLLAMA as it is not natively linked, nor can available in ollama model Hub.

   1. Start by installing the gguf file from **_HuggingFace_** --> [ATLASAI_9b.gguf](https://huggingface.co/RichardErkhov/MBZUAI-Paris_-_Atlas-Chat-9B-gguf/blob/main/Atlas-Chat-9B.Q5_0.gguf)
   2. Create a file without extension named **modelfile** within it : `FROM path_to_your_gguf_file.gguf`
   3. Run the command `ollama create atlasai:9b -f .` to install the model into OLLAMA.

5. **Start the app**
   To run the app, execute the command `python main.py` and the server starts automatically.

---

###### 🐳 Installation via Docker

> Install docker into your local machine, no other requirements needed apart from OLLAMA and the gguf file, everything is contained into the Docker container.

Run the command `docker pull thami0011/transcript_chatbot:latest` to download the docker image.
Then run the container linking the ports `8000` and `11434` to your local machine to allow OLLAMA and server port to communicate: `docker run -p 8000:8000 -p 11434:11434 --name your_container_name thami0011/transcript_chatbot:latest`
