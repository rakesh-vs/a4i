#!/usr/bin/env python3
"""
Script for deploying first_responder_agent on vertex agent_engine
"""

import os
import subprocess
import sys
from dotenv import load_dotenv

load_dotenv()

def deploy():
    """Deploy agent_engine and first_responder_agent to Google Cloud."""
    project = os.getenv("GCP_PROJECT")
    region = os.getenv("GCP_REGION")
    staging_bucket = os.getenv("STAGING_BUCKET")

    cmd = [
        "adk",
        "deploy",
        "agent_engine",
        "first_responder_agent",
        f"--project={project}",
        f"--region={region}",
        f"--staging_bucket={staging_bucket}",
    ]

    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    sys.exit(result.returncode)


if __name__ == "__main__":
    deploy()
