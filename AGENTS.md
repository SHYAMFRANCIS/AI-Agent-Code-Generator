# AGENTS.md - Development Guidelines for AI Agent Code Generator

This file provides essential information for agentic coding agents working in this repository.

## Project Overview

This is a Python-based AI Agent Code Generator that uses LlamaIndex, Ollama models, and various AI tools to analyze code, generate new code, and answer questions about provided codebases. The application runs as a CLI tool with Docker support.

## Development Commands

### Environment Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Install Ollama models (required)
ollama pull mistral
ollama pull codellama
```

### Running the Application
```bash
# Main application (interactive CLI)
python3 main.py

# Using Docker
docker build -t ai-agent-code-generator .
docker run -it --rm ai-agent-code-generator
```

### Testing
```bash
# No formal test framework is currently set up
# To test functionality manually:
# 1. Place files in ./data directory for analysis
# 2. Run python3 main.py and interact with prompts
# 3. Check generated code in ./output directory
```

### Code Quality
```bash
# No linting/formatted tools currently configured
# Recommended additions:
pip install black flake8 mypy pytest
```

## Code Style Guidelines

### Python Formatting
- **Python Version**: Python 3.11+ (as specified in Dockerfile)
- **Indentation**: 4 spaces
- **Line Length**: Aim for under 100 characters (existing code varies)
- **Quotes**: Single quotes for strings, double quotes for docstrings

### Import Organization
```python
# Standard library imports first
import os
import ast

# Third-party imports next
from llama_index.llms.ollama import Ollama
from llama_parse import LlamaParse
from pydantic import BaseModel

# Local imports last
from prompts import context, code_parser_template
from code_reader import code_reader
```

### Naming Conventions
- **Variables**: snake_case (e.g., `file_extractor`, `query_engine`)
- **Functions**: snake_case (e.g., `code_reader_func`)
- **Classes**: PascalCase (e.g., `CodeOutput`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `API_KEY`)
- **Files**: snake_case (e.g., `code_reader.py`)

### Type Hints
- Use type hints for function parameters and return values
- Import from `typing` module when needed
- Example: `def code_reader_func(file_name: str) -> dict:`

### Error Handling
```python
# Use try-except blocks for file operations and API calls
try:
    with open(path, "r") as f:
        content = f.read()
        return {"file_content": content}
except Exception as e:
    return {"error": str(e)}
```

### Class Structure
- Use Pydantic models for data validation
- Include clear docstrings for classes and methods
- Example from codebase:
```python
class CodeOutput(BaseModel):
    code: str
    description: str
    filename: str
```

## Architecture Guidelines

### Core Components
1. **main.py**: Entry point with agent setup and main loop
2. **prompts.py**: System prompts and templates
3. **code_reader.py**: Tool for reading code files
4. **data/**: Directory for input files and documentation
5. **output/**: Directory for generated code files

### AI Model Integration
- Uses Ollama models: `mistral` for documentation queries, `codellama` for code generation
- LlamaParse for document parsing (PDF support)
- VectorStoreIndex for efficient information retrieval
- ReActAgent pattern for tool usage

### Tool Development
When creating new tools:
1. Use `FunctionTool.from_defaults()` wrapper
2. Provide clear descriptions for AI understanding
3. Return structured data (dicts or Pydantic models)
4. Handle errors gracefully and return error information

## File Structure Guidelines

### Directory Layout
```
/
├── main.py              # Application entry point
├── prompts.py           # System prompts and templates  
├── code_reader.py      # File reading tool
├── requirements.txt    # Python dependencies
├── Dockerfile         # Docker configuration
├── data/              # Input files for analysis
├── output/            # Generated code files
└── .env               # Environment variables (gitignored)
```

### Configuration
- Environment variables loaded via `python-dotenv`
- Key variables: `LLAMA_CLOUD_API_KEY` and other API keys
- Models configured in main.py (can be modified for different use cases)

## Best Practices

### Development Workflow
1. Test changes with sample data in `./data` directory
2. Verify generated code outputs to `./output` directory  
3. Use Docker for consistent environment testing
4. Check Ollama model availability before running

### Security Considerations
- Never commit API keys or sensitive data
- Use environment variables for configuration
- Validate file paths to prevent directory traversal
- Handle user input sanitization for generated code

### Performance Considerations
- Vector indexing provides efficient document retrieval
- Request timeouts configured for Ollama models (30.0 seconds)
- Retry logic implemented for resilient operation (max 3 retries)

## Adding New Features

### New Tool Integration
1. Create tool function in separate file or existing module
2. Use `FunctionTool.from_defaults()` pattern
3. Add tool to tools list in main.py
4. Update agent configuration if needed

### Model Configuration
- Models configured in main.py lines 18 and 40
- Can be swapped for different Ollama models or cloud APIs
- Adjust request timeouts based on model performance

### Prompt Engineering  
- System prompts stored in prompts.py
- Use clear, descriptive prompts for better results
- Template variables use `{variable}` syntax for QueryPipeline

## Common Issues and Solutions

### Model Connection Issues
- Ensure Ollama is running: `ollama list`
- Verify models are pulled: `ollama pull mistral`, `ollama pull codellama`
- Check network connectivity for cloud APIs

### File Path Issues
- Use `os.path.join()` for cross-platform compatibility
- Verify `data` and `output` directories exist
- Check file permissions for read/write operations

### Docker Issues
- Use `--network=host` for Ollama connectivity
- Mount volumes for persistent data: `-v $(pwd)/data:/app/data`
- Ensure proper environment variables are passed