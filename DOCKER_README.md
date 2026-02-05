# Docker Setup for AI-Agent-Code-Generator

## Building the Docker Image

To build the Docker image for this project, run:

```bash
cd AI-Agent-Code-Generator
docker build -t ai-agent-code-generator .
```

## Running the Docker Container

To run the application in a container:

```bash
docker run -it --rm ai-agent-code-generator
```

## Mounting Volumes for Data and Output

To provide data files and access generated outputs:

```bash
docker run -it --rm \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/output:/app/output \
  ai-agent-code-generator
```

## Passing Environment Variables

If you need to set environment variables (like API keys):

```bash
docker run -it --rm \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/output:/app/output \
  -e LLAMA_CLOUD_API_KEY=your_api_key_here \
  ai-agent-code-generator
```

## Notes

- The application is a CLI application, so it will prompt for input interactively
- Place your data files in the ./data directory before running
- Generated code will be saved to the ./output directory
- The application uses Ollama models (mistral and codellama), which may need to be available in your environment