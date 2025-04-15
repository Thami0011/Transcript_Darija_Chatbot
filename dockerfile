FROM pytorch/pytorch:2.6.0-cuda12.4-cudnn9-runtime

WORKDIR /app

RUN apt-get update && apt-get install -y \
    ffmpeg

COPY . .

EXPOSE 8000

EXPOSE 11434

RUN pip install --no-cache-dir -r /app/requirements.txt

CMD ["python", "main.py"]