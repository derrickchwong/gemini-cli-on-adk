# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import requests

import google.auth
from google.adk.agents import Agent

def get_project_id():
    """Get project ID from Cloud Run metadata service or fallback to auth."""
    try:
        # Try Cloud Run metadata service first
        metadata_url = "http://metadata.google.internal/computeMetadata/v1/project/project-id"
        headers = {"Metadata-Flavor": "Google"}
        response = requests.get(metadata_url, headers=headers, timeout=5)
        if response.status_code == 200:
            return response.text
    except Exception:
        pass

    # Fallback to google.auth
    _, project_id = google.auth.default()
    return project_id

project_id = get_project_id()
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", project_id)
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "global")
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "true")

def gemini_cli(task: str, github_url: str) -> str:
    """Executes the Gemini CLI.

    Args:
        task: The task to pass to Gemini CLI, eg: explain this codebase, generate a test plan, etc.
        github_url: GitHub URL to clone and analyze.

    Returns:
        The response from the Gemini CLI.
    """
    import subprocess

    try:
        # Extract repository name from GitHub URL to create local directory
        repo_name = github_url.rstrip('/').split('/')[-1]
        if repo_name.endswith('.git'):
            repo_name = repo_name[:-4]

        codebaseDir = f"/tmp/{repo_name}"

        # Clone the repo if directory doesn't exist
        if not os.path.exists(codebaseDir):
            print(f"Directory {codebaseDir} doesn't exist. Cloning from {github_url}...")
            clone_command = f'git clone "{github_url}" "{codebaseDir}"'
            clone_result = subprocess.run(
                clone_command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=300,  # 5 minutes timeout for git clone
            )

            if clone_result.returncode != 0:
                return f"Error cloning repository: {clone_result.stderr}"

            print(f"Successfully cloned repository to {codebaseDir}")

        # Construct the gemini command with include-directories
        command = f'gemini -p "{task}"'

        # Execute the command in the specified directory with required environment variable
        env = os.environ.copy()

        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=600,  # Increased timeout for AI processing
            cwd=codebaseDir,
            env=env,
        )

        # Return the stdout directly as the response
        if result.returncode == 0:
            return result.stdout
        else:
            return f"Error executing Gemini CLI: {result.stderr}"

    except subprocess.TimeoutExpired:
        return "Gemini CLI command timed out after 600 seconds"
    except Exception as e:
        return f"Failed to execute Gemini CLI: {str(e)}"


root_agent = Agent(
    name="root_agent",
    model="gemini-2.5-pro",
    instruction="""    
You are a world class Software Developer and you have a very powerful tool - Gemini CLI to help analyze code, generating test plan, generating unit tests, etc. 
The codebase is cloned from a GitHub repository and stored on /tmp directory.
Always use the Gemini CLI tool to analyze the codebase and complete the user's request.
""",
    tools=[gemini_cli],
)