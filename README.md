# gemini-cli-on-adk

## Gemini CLI Integration

This project demonstrates how Gemini CLI's non-interactive mode can significantly enhance ADK development workflows. The integration in `app/agent.py` provides a powerful `gemini_cli` tool that enables automated development tasks.

### Key Benefits

- **Automated Code Analysis**: The agent can analyze codebases without manual file selection using Gemini CLI's intelligent file discovery
- **Streamlined Development**: Eliminates the need to manually specify which files to send to the agent
- **Command Execution**: Automated execution of development commands based on analysis results
- **File Editing**: Intelligent file modifications based on code analysis recommendations
- **Error Handling**: Built-in timeout and robust error handling for reliable execution

### Development Efficiency Gains

The non-interactive mode saves significant development time by:

1. **Intelligent File Selection**: Automatically determines relevant files for specific tasks
2. **Automated Code Generation**: Generates boilerplate code, tests, and documentation
3. **Command Automation**: Executes development commands without manual intervention
4. **Contextual Analysis**: Provides codebase insights with full project context

### Usage Example

The integrated `gemini_cli` function accepts tasks like:
- "Explain this codebase"
- "Generate a test plan"
- "Create unit tests for the agent module"
- "Analyze code quality and suggest improvements"

This integration demonstrates how Gemini CLI can serve as a powerful development accelerator within ADK agents.

## Project Structure

This project is organized as follows:

```
gemini-cli-on-adk/
├── app/                 # Core application code
│   ├── agent.py         # Main agent logic
│   ├── server.py        # FastAPI Backend server
│   └── utils/           # Utility functions and helpers
├── deployment/          # Infrastructure and deployment scripts
├── notebooks/           # Jupyter notebooks for prototyping and evaluation
├── tests/               # Unit, integration, and load tests
├── Makefile             # Makefile for common commands
├── GEMINI.md            # AI-assisted development guide
└── pyproject.toml       # Project dependencies and configuration
```

## Deployment

The ADK agent is designed to run on Google Cloud Run. It includes a Dockerfile and Cloud Build YAML configuration for seamless deployment using Google Cloud Build.

### Prerequisites

- Vertex AI API must be enabled in your Google Cloud project
- Cloud Run service account must have access to Vertex AI services

### Cloud Run Deployment

Build the container image using Cloud Build:

```bash
gcloud builds submit --config cloudbuild.yaml
```

You can also override the default substitution variables:

```bash
gcloud builds submit --config cloudbuild.yaml --substitutions=_REGION=us-east1,_REPO_NAME=my-repo,_SERVICE_NAME=my-service,_IMAGE_TAG=v1.0.0
```

Available substitution variables:
- `_REGION`: Deployment region (default: us-central1)
- `_REPO_NAME`: Artifact Registry repository name (default: container)
- `_SERVICE_NAME`: Cloud Run service name (default: gemini-cli-adk)
- `_IMAGE_TAG`: Docker image tag (default: latest)

