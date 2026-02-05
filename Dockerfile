FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies that might be needed for the Python packages
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    git \
    curl \
    zstd \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama if needed (the models will need to be pulled separately)
RUN curl -fsSL https://ollama.ai/install.sh | sh

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Create output directory if it doesn't exist
RUN mkdir -p output

# Expose port if running a web service (though this is a CLI app)
EXPOSE 8000

# Set up environment
ENV PYTHONPATH=/app

# Default command to run the application
CMD ["python", "main.py"]
