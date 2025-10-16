# A4I - ADK Agent Framework

A starter project for building and deploying AI agents using Google's Agent Development Kit (ADK).

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- `uv` package manager
- Google Cloud credentials (for using Gemini models)

### Installation

1. **Clone and setup the project:**
```bash
cd a4i
uv sync
```

2. **Set up environment variables:**
```bash
cp .env.example .env
# Edit .env with your Google Cloud credentials
```

3. **Run the starter agent:**
```bash
uv run python main.py
```

## 📁 Project Structure

```
a4i/
├── agents/                 # Agent implementations
│   ├── __init__.py
│   ├── base_agent.py      # Base agent configuration
│   └── search_agent.py    # Search agent example
├── tests/                  # Test suite
│   ├── __init__.py
│   └── test_agents.py
├── main.py                # Entry point
├── pyproject.toml         # Project configuration
├── .env.example           # Environment variables template
└── README.md              # This file
```

## 🤖 Creating Your First Agent

### Simple Search Agent

```python
from agents.search_agent import create_search_agent

async def main():
    agent = create_search_agent()
    response = await agent.run("What is AI?")
    print(response)
```

### Custom Agent

```python
from agents.base_agent import BaseAgentConfig
from google.adk.tools import google_search

agent = BaseAgentConfig.create_agent(
    name="my_agent",
    instruction="You are a helpful assistant.",
    description="My custom agent",
    tools=[google_search]
)
```

## 🧪 Testing

Run tests with pytest:

```bash
uv run pytest tests/
```

Run with coverage:

```bash
uv run pytest tests/ --cov=agents
```

## 📦 Dependencies

### Core
- **google-adk** - Agent Development Kit
- **anthropic** - Anthropic SDK
- **pydantic** - Data validation
- **python-dotenv** - Environment management

### Development
- **pytest** - Testing framework
- **pytest-asyncio** - Async test support
- **black** - Code formatter
- **ruff** - Linter
- **mypy** - Type checker

## 🚢 Deployment

### Local Development
```bash
uv run python main.py
```

### Docker Deployment
```bash
docker build -t a4i-agent .
docker run a4i-agent
```

### Google Cloud Run
```bash
gcloud run deploy a4i-agent --source .
```

## 📚 Resources

- [ADK Documentation](https://google.github.io/adk-docs/)
- [ADK GitHub](https://github.com/google/adk-python)
- [Gemini API Docs](https://ai.google.dev/)

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## 📝 License

This project is licensed under the Apache 2.0 License.
