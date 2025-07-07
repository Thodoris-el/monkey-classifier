FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Copy your code before downloading model
COPY . .

# Download the model from Hugging Face
RUN wget https://huggingface.co/theoEL/monkey-model/resolve/main/all_labels.h5 -O all_labels.h5

# Install Python packages
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Expose port (used by Render/Railway)
ENV PORT=5000

# Run your app with increased timeout
CMD gunicorn --bind 0.0.0.0:$PORT app:app --timeout 120