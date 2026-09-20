# 1. Start with a reliable, lightweight Linux computer (3.10 is safest for PyTorch wheels)
FROM python:3.10-slim

# 2. Prevent Python from writing .pyc files and buffering stdout
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 3. Create a folder called /app inside this new computer and move into it
WORKDIR /app

# 4. Install essential build tools (required for compiling certain Python packages on ARM64)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 5. Copy just the requirements file first
COPY requirements.txt .

# 6. Upgrade pip and install PyTorch (ARM64 default wheels are already CPU-only and lightweight)
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir torch torchvision torchaudio

# 7. Install all the other Python libraries (Langchain, Streamlit, etc.)
RUN pip install --no-cache-dir -r requirements.txt

# 8. Now, copy all of your project code from your laptop into the /app folder
COPY . .

# 9. Tell Python to look in the /app folder for your custom files
ENV PYTHONPATH=/app

# 10. Open port 8501 so the outside world can see the Streamlit website
EXPOSE 8501

# 11. The exact command to start the Web App when the container boots up
CMD ["streamlit", "run", "app/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
