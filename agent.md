# agent.md

This file provides guidance to AI assistants (GitHub Copilot, Claude, Gemini, etc.) when working with code in this repository.

## Repository Overview

This is the AI-Driven Software Engineering Program repository - a comprehensive 10-day intensive course teaching modern software development with AI assistance. The repository contains course materials, labs, solutions, and a unified AI provider interface for interacting with multiple LLM providers.

## Essential Commands

### Environment Setup
```bash
# Initial setup (run once)
python -m venv venv

# Activate environment (run every session)
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up pre-commit hooks (optional but recommended)
pip install pre-commit
pre-commit install
```

### Testing
```bash
# Run all unit tests
pytest tests/

# Run specific test files
pytest tests/test_text_generation.py
pytest tests/test_utils.py

# Run tests with coverage
pytest --cov=utils tests/

# Run integration tests (require API keys)
pytest -m integration

# Run slow tests (image generation/editing, 10-30s each)
pytest -m slow

# Skip integration tests
pytest -m "not integration"
```

### Code Quality
```bash
# Run pre-commit hooks on all files
pre-commit run --all-files

# Format code with Black
black .

# Sort imports with isort
isort .

# Lint with Ruff
ruff check .

# Type check with mypy
mypy utils/
```

### Development Workflow
```bash
# Start Jupyter for interactive development
jupyter notebook

# Run a specific notebook
jupyter nbconvert --to notebook --execute "Labs/Day_01_Planning_and_Requirements/D1_Lab1_AI_Powered_Requirements_User_Stories.ipynb"

# Start FastAPI development server (if app directory exists)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Start Streamlit app (if using Streamlit)
streamlit run app.py
```

### Docker Operations
```bash
# Build container
docker build -t ai-software-engineering .

# Run containerized application
docker run -p 8000:8000 --env-file .env ai-software-engineering
```

## Architecture Overview

### Core Components

**`utils/` - Unified AI Interface Module**
The heart of this repository is the `utils/` module, which provides a standardized interface for multiple AI providers (OpenAI, Anthropic, Hugging Face, Google Gemini). Key files include:

- `llm.py`: Core LLM functions (`get_completion()`, `async_get_completion()`, `get_vision_completion()`, `setup_llm_client()`, `async_setup_llm_client()`, `prompt_enhancer()`)
- `models.py`: Model configuration database with `RECOMMENDED_MODELS` and capabilities metadata
- `providers/`: Provider-specific implementations for each AI provider
- `image_gen.py`: Image generation and editing (`get_image_generation_completion()`, `get_image_edit_completion()`)
- `audio.py`: Speech-to-text processing (`transcribe_audio()`)
- `artifacts.py`: Artifact saving/loading with path resolution and security controls
- `helpers.py`: Shared utility functions
- `errors.py`: Custom exception classes
- `settings.py`: Environment loading and Jupyter display helpers
- `rate_limit.py`: Provider-aware throttling
- `http.py`: Shared HTTP session utilities
- `logging.py`: Structured logging for notebooks and scripts
- `plantuml.py`: PlantUML diagram rendering

### Educational Structure

**Labs Directory (`Labs/`)**
Organized by days (Day_01 through Days_9_and_10) with:
- Each day contains specific learning objectives and hands-on exercises
- Jupyter notebooks for interactive development
- README files with day-specific guidance
- `Agent_notebooks/` for advanced agent exercises
- `Day_07_MCP_and_A2A/` for Model Context Protocol and Agent-to-Agent protocol labs

**Solutions Directory (`Solutions/`)**
- `Day_01` through `Day_08` with fully worked notebooks
- Reference implementations instructors can demo or students can review

**Supporting Materials**
- `Environment_Setup_Guide.md` - Setup instructions
- `Docker_Guide.md` - Docker deployment
- `Artifacts_Guide.md` - Artifact management deep dive
- `Deployment_Guide_Onboarding_Tool.md` - Full-stack deployment
- `How_to_View_Your_React_Components_Locally.md` - React viewing guide
- `Productionizing_Utils.md` - Production configuration
- `GitHub_Copilot_Reference_Guide.md` - Copilot best practices
- `VS_Code_Copilot_Best_Practices.md` - VS Code tips
- `Starter_Utils_Demo.ipynb` - Interactive utilities demo
- `🔑 API Key Generation Guide for Labs.pdf` - API key setup

**Artifacts Directory (`artifacts/`)**
Generated course outputs including:
- `app/` - Sample FastAPI application
- `a2a_requester.py`, `a2a_responder.py` - A2A protocol examples
- `schema.sql`, `seed_data.sql` - Database schemas
- `Dockerfile` - Container configuration
- `chat_ui.py` - Chat interface example
- `day1_prd.md`, `day1_user_stories.json` - Sample planning artifacts

**Testing Framework**
- `tests/` - Unit tests for utilities (offline-safe)
- Test markers: `integration` (API calls), `slow` (image generation)
- Database model validation tests with in-memory SQLite

### Key Patterns

**Environment Management**
- Uses `python-dotenv` for secure API key management
- `.env` file pattern for local configuration
- Project root detection via markers (`.git`, `artifacts`, `README.md`)

**Artifact Management**
- All generated content saved to `artifacts/` directory
- Path resolution with security controls to prevent directory traversal
- Automatic directory creation for nested structures

**Error Handling**
- Graceful degradation when optional dependencies are missing
- Provider-specific error handling with informative messages
- Fallback mechanisms for different API endpoint variations

**Code Style**
- Black for formatting (line-length 88)
- isort for import sorting (Black-compatible profile)
- Ruff for linting
- mypy for type checking (Python 3.11)
- Pre-commit hooks enforce style on commits

## Development Guidelines

### Working with AI Providers

When adding new AI provider integrations, follow the established pattern in `utils/`:

1. Add model configuration to `RECOMMENDED_MODELS` in `utils/models.py` with capability flags
2. Create a new provider file in `utils/providers/`
3. Implement provider-specific client setup in `setup_llm_client()` in `utils/llm.py`
4. Add provider handling to relevant completion functions
5. Update model filtering in `recommended_models_table()`

### Testing Considerations

- Use `pytest.mark.integration` for tests that call external APIs
- Use `pytest.mark.slow` for tests involving image generation (10-30 seconds)
- Test database models use in-memory SQLite with proper fixture isolation
- Mock external API calls in unit tests to avoid rate limits
- Run `pytest tests/` (fast, offline) before committing

### Jupyter Notebook Development

- Notebooks expect activated virtual environment with installed dependencies
- Use `utils` module functions for consistent AI provider interactions
- Save artifacts using `utils.artifacts.save_artifact()` for proper path management
- Display generated content using provided display helpers from `utils.settings`

### Docker Considerations

- Multi-stage build optimizes for production deployment
- FastAPI application expects to run at `/app` with `PYTHONPATH=/app`
- Environment variables passed via `--env-file .env`
- Exposes port 8000 for web services

## Course-Specific Context

This repository teaches AI-assisted development across the full SDLC:

**Week 1:**
- Day 1: AI-powered planning and requirements
- Day 2: Design and architecture with AI
- Day 3: Development and coding with AI assistants
- Day 4: Testing and quality assurance
- Day 5: Introduction to agents and RAG

**Week 2:**
- Day 6: Building RAG systems
- Day 7: Advanced agent workflows, MCP, and A2A protocols
- Day 8: Vision capabilities and evaluation
- Days 9-10: Capstone projects

The `utils/` module serves as the foundation for all AI interactions throughout the course, providing students with a consistent interface regardless of which provider or model they choose to use.

## API Key Requirements

Essential for full functionality:
- `OPENAI_API_KEY`: Required for most course exercises
- `HUGGINGFACE_API_KEY`: Optional for open-source model experiments
- `GOOGLE_API_KEY`: Optional for Gemini model usage
- `ANTHROPIC_API_KEY`: Optional for Claude model usage
- `TAVILY_API_KEY`: Optional for web search in agent labs

Store these in a `.env` file in the repository root (never commit this file).

## Key Dependencies

The repository uses these major frameworks and libraries:

**Web Frameworks:** FastAPI, Flask, Streamlit, uvicorn
**Agent Frameworks:** AutoGen, CrewAI, LangChain, LangGraph, smolagents, MCP, A2A Protocol
**RAG Components:** FAISS, sentence-transformers, pypdf
**Model Providers:** OpenAI, Anthropic, Google GenAI, Hugging Face
**ML Infrastructure:** PyTorch, Transformers, Accelerate
**Testing:** pytest, pytest-asyncio
**Data:** pandas, numpy, matplotlib, seaborn, scikit-learn

See `requirements.txt` for the complete dependency list with pinned versions.
