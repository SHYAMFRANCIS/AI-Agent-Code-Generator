# AI-Agent-Code-Generator Docker Image

This repository contains a Docker image for the AI-Agent-Code-Generator, an AI-powered tool that can analyze code, generate new code, and answer questions about code using large language models.

## Features

- AI-powered code generation and analysis
- Integration with Ollama models (mistral and codellama)
- Document parsing capabilities (supports PDF files)
- Interactive command-line interface
- File reading and analysis tools

## Prerequisites

Before using this Docker image, ensure you have:

- Docker installed on your system
- Ollama installed and running on your host system with the required models:
  - `mistral`
  - `codellama`

Install the required models:
```bash
ollama pull mistral
ollama pull codellama
```

## Quick Start

To run the AI-Agent-Code-Generator using Docker:

```bash
# Pull and run the latest image
docker run -it --rm \
  --network=host \
  yourusername/ai-agent-code-generator:latest
```

## Usage with Volume Mounts

For better integration with your local files, mount the data and output directories:

```bash
docker run -it --rm \
  --network=host \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/output:/app/output \
  yourusername/ai-agent-code-generator:latest
```

### Environment Variables

If you need to set environment variables (like API keys), use:

```bash
docker run -it --rm \
  --network=host \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/output:/app/output \
  -e LLAMA_CLOUD_API_KEY=your_api_key_here \
  yourusername/ai-agent-code-generator:latest
```

## Building from Source

To build the image from source:

```bash
git clone https://github.com/yourusername/ai-agent-code-generator.git
cd ai-agent-code-generator
docker build -t yourusername/ai-agent-code-generator .
```

## Configuration

### Data Directory
Place documentation files (PDFs, source code, etc.) in the `data` directory for the AI to reference during code generation.

### Output Directory
Generated code will be saved in the `output` directory.

## How It Works

The application uses a ReAct agent with:
- Ollama's mistral model for documentation queries
- Ollama's codellama model for code generation
- LlamaParse for document parsing
- Vector indexing for efficient information retrieval

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the terms specified in the original repository.

## Support

If you encounter issues with the Docker image, please file an issue in the GitHub repository.