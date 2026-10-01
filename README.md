# AI Agent Code Generator

[![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)](https://www.python.org/)
[![LlamaIndex](https://img.shields.io/badge/LlamaIndex-0.10-purple)](https://www.llamaindex.ai/)
[![Ollama](https://img.shields.io/badge/Ollama-mistral%20%2B%20codellama-black)](https://ollama.com/)
[![Docker](https://img.shields.io/badge/Docker-ready-2496ED?logo=docker)](DOCKER_README.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A **CLI-based AI agent** that analyses code, answers questions about a codebase, and generates new code. It combines a **LlamaIndex ReAct agent** (running **Ollama `mistral`**) with a **retrieval tool over PDF API docs** (LlamaParse + local **BGE-M3** embeddings) and a **`code_reader` file tool**, then formats the result through a structured parser into `{code, description, filename}` via **Ollama `codellama`**. Ships with a **Dockerfile** for containerized runs.

> Docker-specific instructions live in [`DOCKER_README.md`](DOCKER_README.md) — this file documents the project itself. `DOCKER_README.md` is intentionally preserved as-is.

## Features

- **ReAct agent loop** — `ReActAgent` with `mistral` reasons over tools and a `context` system prompt (`main.py`, `prompts.py`).
- **API-docs retrieval tool** — PDFs in `./data` parsed by `LlamaParse`, embedded locally with `BAAI/bge-m3`, queried as `api_documentation` (`main.py`).
- **Code reading tool** — `code_reader` `FunctionTool` returns the contents of any file under `./data` (`code_reader.py`).
- **Structured code output** — Agent response parsed by `PydanticOutputParser(CodeOutput)` into `code`, `description`, `filename` (`prompts.py: code_parser_template`).
- **Interactive CLI** — Prompt loop (`q` to quit) with up to 3 retries per request; generated code lands in `./output` (`main.py`).
- **Diagnostics** — Import/debug helpers (`debug_imports.py`, `check_async.py`) and agent-method tests (`test_agent_methods.py`).
- **Docker support** — Python 3.11-slim image with Ollama install, volume mounts for `./data` and `./output` (`Dockerfile`, `DOCKER_README.md`).
- **Agent contributor guide** — `AGENTS.md` documents setup and commands for agentic coding assistants.

## Tech Stack

| Layer      | Technology |
|------------|------------|
| Agent      | LlamaIndex 0.10 (`ReActAgent`, `QueryEngineTool`, `FunctionTool`, `VectorStoreIndex`) |
| LLMs       | Ollama `mistral` (reasoning) + `codellama` (code), via `llama-index-llms-ollama` |
| Parsing    | LlamaParse (PDF → Markdown), `PydanticOutputParser` |
| Embeddings | Local `BAAI/bge-m3` (`llama-index-embeddings-huggingface`, `sentence-transformers`) |
| App        | Python CLI (`main.py`), `nest-asyncio`, `python-dotenv` |
| Python     | 3.13 (`.python-version`); Docker image uses 3.11-slim |
| Deploy     | Docker (`Dockerfile`, `DOCKER_README.md`, `DOCKER_REPO_README.md`) |

## Project Structure

```text
AI-Agent-Code-Generator/
├── main.py                 # Agent wiring, retrieval index, CLI loop, output parsing
├── prompts.py              # context system prompt + code_parser_template
├── code_reader.py           # code_reader FunctionTool (reads ./data/<file>)
├── requirements.txt        # Full dependency set (llama-index, torch stack, …)
├── core_requirements.txt   # Core subset
├── pyproject.toml          # Project metadata (name: ai-agent, requires-python >=3.13)
├── Dockerfile              # Container build (Ollama install, ./output, CMD main.py)
├── DOCKER_README.md        # Docker usage (preserved)
├── DOCKER_REPO_README.md   # Docker Hub repo readme
├── AGENTS.md               # Contributor guide for AI coding agents
├── QWEN.md                 # Architecture notes
├── data/                   # Input: PDFs + code files the agent reads
├── output/                 # Generated code lands here
├── check_async.py / debug_imports.py   # Diagnostics
└── test_agent_methods.py   # Agent-method tests
```

## Installation

**Prerequisites:** Python 3.13, [Ollama](https://ollama.com/) with the required models.

```bash
git clone https://github.com/SHYAMFRANCIS/AI-Agent-Code-Generator.git
cd AI-Agent-Code-Generator

ollama pull mistral
ollama pull codellama

pip install -r requirements.txt
```

Set any needed keys (e.g. `LLAMA_CLOUD_API_KEY` for LlamaParse) in a `.env` file — a `.env` is already expected via `python-dotenv`:

```env
LLAMA_CLOUD_API_KEY=your_api_key_here
```

Place the PDFs/code you want the agent to reference in `./data/`.

## Usage

```bash
python main.py
```

Then type a request at the prompt (`q` to quit):

```text
Enter a prompt (q to quit): Write a FastAPI endpoint that paginates users from Postgres
```

The agent consults the `api_documentation` index and `code_reader`, and the parsed `{code, description, filename}` result is produced (saved under `./output`).

### Docker

```bash
docker build -t ai-agent-code-generator .
docker run -it --rm \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/output:/app/output \
  -e LLAMA_CLOUD_API_KEY=your_api_key_here \
  ai-agent-code-generator
```

See [`DOCKER_README.md`](DOCKER_README.md) for full details.

### Examples

- *“Explain what the authentication module in `./data` does.”* → agent reads files via `code_reader` and summarises.
- *“Generate a retry decorator with exponential backoff; save suggestion as1595062364.py.”* → structured `CodeOutput` with filename suggestion.

## Configuration / Environment

| Variable              | Description                                   |
|-----------------------|-----------------------------------------------|
| `LLAMA_CLOUD_API_KEY` | API key for LlamaParse PDF parsing (optional for local-only use) |

Models are fixed in `main.py`: `mistral` for reasoning, `codellama` for code, `local:BAAI/bge-m3` for embeddings — edit there to swap models.

## Contributing

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/my-change`).
3. Run `python test_agent_methods.py` and verify `python main.py` still completes a prompt.
4. Open a pull request describing the change.

## License

No `LICENSE` file is present in this repository. The code is shared publicly by the author; if you intend to reuse it, please confirm licensing with the repository owner. (This README defaults to referencing MIT — a `LICENSE` file should be added to make that explicit.)
