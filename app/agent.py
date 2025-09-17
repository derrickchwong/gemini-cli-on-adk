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

import google.auth
from google.adk.agents import Agent

_, project_id = google.auth.default()
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", project_id)
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "global")
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "True")

def gemini_cli(task: str, codebaseDir: str) -> str:
    """Executes the Gemini CLI.

    Args:
        task: The task to pass to Gemini CLI, eg: explain this codebase, generate a test plan, etc.
        codebaseDir: The location of the codebase in local file system.

    Returns:
        The response from the Gemini CLI.
    """
    import subprocess

    try:
        # Construct the gemini command with include-directories
        command = f'gemini -p "{task}" --include-directories "{codebaseDir}"'

        # Execute the command in the specified directory
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=60,  # Increased timeout for AI processing
            cwd=codebaseDir,
        )

        # Return the stdout directly as the response
        if result.returncode == 0:
            return result.stdout
        else:
            return f"Error executing Gemini CLI: {result.stderr}"

    except subprocess.TimeoutExpired:
        return "Gemini CLI command timed out after 60 seconds"
    except Exception as e:
        return f"Failed to execute Gemini CLI: {str(e)}"


root_agent = Agent(
    name="root_agent",
    model="gemini-2.5-pro",
    instruction="You are a world class Software Developer and you have a very powerfull tool - Gemini CLI to help analyze code, generating test plan, generating unit tests, etc. that located in local file system.",
    tools=[gemini_cli],
)
