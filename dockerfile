FROM pytorch/pytorch:2.6.0-cuda12.4-cudnn9-runtime

WORKDIR /app

# Install system dependencies with cleanup
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy only necessary files
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the app (after deps are installed to leverage Docker cache)
COPY . .

# Expose ports
EXPOSE 8000 11434

# Use python -m if main.py is a module, or keep as is
CMD ["python", "main.py"]
