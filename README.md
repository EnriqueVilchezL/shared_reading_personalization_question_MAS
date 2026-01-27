# Shared Reading Personalization and Question Generation System

A multi-agent system (MAS) built with LangGraph and LangChain that personalizes children's stories based on user preferences and generates educational questions for shared reading activities.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Components](#components)
- [License](#license)

## Overview

This system provides two main capabilities:

1. **Story Personalization**: Adapts children's stories to match individual reading preferences (e.g., reading level, interests, cultural context)
2. **Question Generation**: Creates various types of educational questions to enhance reading comprehension and engagement

The system uses a multi-agent architecture where specialized agents collaborate to achieve these goals, with built-in quality control through critic agents.

## Features

### Personalization Pipeline

- **Adaptive Story Modification**: Personalizes stories based on user preferences
- **Multi-Criteria Evaluation**: Uses specialized critic agents to evaluate personalization quality:
  - Triage Critic: Determines if personalization meets acceptable standards
  - Coherence Critic: Ensures narrative consistency
  - Emotion Critic: Evaluates emotional appropriateness
  - Moral Critic: Assesses moral and ethical alignment
  - Naturalness Critic: Checks for natural language flow
  - Style Critic: Assesses appropriate writing style
  - Value Critic: Ensures educational value
- **Iterative Refinement**: Automatically retries personalization if quality standards aren't met

### Question Generation Pipeline

- **Multiple Question Types**: Generates diverse question categories:
  - Completion Questions
  - Recall Questions
  - Open-Ended Questions
  - WH-Questions (Who, What, When, Where, Why, How)
  - Distancing Questions
- **Question Aggregation**: Combines questions from multiple questioner agents into a cohesive set

### Technical Features

- **Role-Based Agent Architecture**: Agents are configured through composable roles
- **LangGraph Orchestration**: Uses LangGraph for complex agent workflows
- **LangFuse Integration**: Built-in observability and tracing
- **Domain-Driven Design**: Clean separation of domain models and services
- **Markdown I/O**: Stories and preferences are read/written in Markdown format

### Core Concepts

- **Agents**: Specialized AI agents that perform specific tasks
- **Roles**: Composable behaviors that define agent capabilities
- **Organizations**: Coordinate multiple agents in workflows
- **Information Schemas**: Define the data structures agents work with
- **Domain Aggregates**: Core business entities (Book, Preference, Evaluation)

## Installation

### Prerequisites

- Python 3.12 or higher
- [uv](https://github.com/astral-sh/uv) package manager (recommended) or pip

### Setup

1. Clone the repository:

```bash
git clone <repository-url>
cd shared_reading_personalization_question_MAS
```

2. Install dependencies using uv:

```bash
uv sync
```

Or using pip:

```bash
pip install -e .
```

3. Set up environment variables:

Create a `.env` file in the project root with your configuration:

```env
# LangFuse Configuration (optional, for observability)
LANGFUSE_PUBLIC_KEY=your_public_key
LANGFUSE_SECRET_KEY=your_secret_key
LANGFUSE_HOST=https://cloud.langfuse.com
```

## Usage

### Command Line Interface

The main entry point provides a command-line interface for running the pipelines:

```bash
python -m src.main \
    --story_path path/to/story.md \
    --preferences_path path/to/profile.md \
    --output_path output.md \
    --pipelines ALL \
    --verbose
```

### Arguments

- `--story_path` (required): Path to the Markdown file containing the story
- `--preferences_path` (required): Path to the Markdown file containing user preferences
- `--output_path` (optional): Output file path (default: `output.md`)
- `--pipelines` (optional): Which pipeline(s) to run:
  - `ALL`: Run both personalization and question generation
  - `PERSONALIZATION`: Run only the personalization pipeline
  - `QUESTIONS`: Run only the question generation pipeline
- `--verbose` (optional): Enable verbose output showing agent messages

### Example Story Format

Stories should be in Markdown format with pages separated by `---`:

```markdown
# Story Title
---
First page content here.
---
Second page content here.
---
```

### Example Preferences Format

Preferences should be in Markdown format:

```markdown
- type: value, value, ..., value
- type_2: value, value, ..., value
```

### Programmatic Usage

You can also use the system programmatically:

```python
from src.main import run_pipelines
from src.domain.services.book_parser import BookParser
from src.domain.services.preference_parser import PreferenceParser
from src.utils import load_md_file

# Load and parse inputs
story_str = load_md_file("data/fox.md")
preferences_str = load_md_file("data/profile.md")

story = BookParser().parse(story_str)
preferences = PreferenceParser().parse(preferences_str)

# Run pipelines
modified_story = run_pipelines(
    story=story,
    preferences=preferences,
    pipeline="ALL",
    verbose=True
)

# Render output
from src.domain.services.book_renderer import BookMarkdownRenderer
output = BookMarkdownRenderer().render(modified_story)
print(output)
```

## Project Structure

```bash
.
├── src/
│   ├── agents/              # Agent implementations
│   │   ├── core/           # Base agent classes and utilities
│   │   ├── personalization/ # Personalization agents
│   │   └── questions/      # Question generation agents
│   ├── domain/             # Domain models and services
│   │   ├── book_aggregate/ # Book domain model
│   │   ├── evaluation_aggregate/ # Evaluation domain model
│   │   ├── preference_aggregate/ # Preference domain model
│   │   └── services/       # Domain services (parsers, renderers)
│   ├── roles/              # Role definitions
│   │   ├── core/          # Base role classes
│   │   ├── personalization/ # Personalization roles
│   │   └── questions/     # Question generation roles
│   ├── main.py            # Main entry point
│   └── utils.py           # Utility functions
├── data/                  # Sample data files
├── pyproject.toml         # Project configuration
└── README.md             # This file
```

## Components

### Agents

#### Personalization Agents

- **PersonalizerAgent**: Main agent that modifies stories based on preferences
- **TriageCriticAgent**: Evaluates if personalization meets minimum quality standards
- **CoherenceCriticAgent**: Ensures narrative coherence
- **EmotionCriticAgent**: Evaluates emotional appropriateness
- **MoralCriticAgent**: Assesses moral alignment
- **NaturalnessCriticAgent**: Checks language naturalness
- **StyleCriticAgent**: Maintains writing style consistency
- **ValueCriticAgent**: Ensures educational value

#### Question Generation Agents

- **CompletionQuestionerAgent**: Generates fill-in-the-blank questions
- **RecallQuestionerAgent**: Creates memory recall questions
- **OpenEndedQuestionerAgent**: Generates open-ended discussion questions
- **WhQuestionerAgent**: Creates WH-questions (who, what, when, where, why, how)
- **DistancingQuestionerAgent**: Generates questions that connect story to reader's experience
- **AggregatorAgent**: Combines questions from all questioner agents

### Domain Models

- **Book**: Represents a story with title, pages, and optional cover image
- **Preference**: User preferences for personalization (type and value)
- **Evaluation**: Critic evaluations with label and requested changes
- **Page**: Individual pages within a book
- **Image**: Cover artwork or illustrations

### Services

- **BookParser/BookRenderer**: Parse and render books from/to Markdown
- **PreferenceParser/PreferenceRenderer**: Parse and render preferences from/to Markdown
- **EvaluationParser/EvaluationRenderer**: Parse and render evaluations from/to Markdown

## ⚙️ Configuration

### Language Model Configuration

Agents use configurable language models. Default configuration can be found in `src/agents/core/base_lm_config.py`. You can customize:

- Model provider (Ollama, OpenAI, Anthropic, etc.)
- Model name
- Temperature
- Reasoning mode (for models that support it)

## License

See [LICENSE](LICENSE) file for details.

## Contributing

This is a research project for a Master's thesis. For questions or contributions, please contact the project maintainer.

## References

- **LangGraph**: Multi-agent workflow orchestration
- **LangChain**: LLM application framework
- **LangFuse**: LLM observability and monitoring
- **Ollama**: Local LLMs server.

---

**Note**: This system is designed for research purposes in the context of shared reading personalization and educational question generation.
