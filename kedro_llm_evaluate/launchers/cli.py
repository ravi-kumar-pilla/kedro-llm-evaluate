import subprocess
import sys
from pathlib import Path
import click

PROJECT_ROOT = Path.cwd()

@click.group(name="llm-evaluate")
def llm_evaluate_cli():
    """Commands for initializing and running local Opik server."""
    pass

@llm_evaluate_cli.command("init")
def init():
    """Scaffold docker-compose.yml and llm_evaluation.yml."""
    # 1. Docker compose file
    compose = PROJECT_ROOT / "docker-compose.opik.yml"
    if not compose.exists():
        compose.write_text(f"""
version: '3'
services:
  opik:
    image: cometml/opik:latest
    ports:
      - "5173:5173"
    restart: unless-stopped
""".strip())
        click.echo(f"• Created {compose.name}")
    # 2. Default llm_evaluation.yml
    cfg = PROJECT_ROOT / "conf" / "base" / "llm_evaluation.yml"
    cfg.parent.mkdir(parents=True, exist_ok=True)
    if not cfg.exists():
        cfg.write_text(f"""
enabled: true
evaluator: opik
opik:
  project_name: {{your_project_name}}
  server_url: http://localhost:5173/api
trace_dir: data/99_traces
""".strip())
        click.echo(f"• Created conf/base/llm_evaluation.yml")
    click.echo("Run `kedro llm-evaluate up` to start Opik locally.")

@llm_evaluate_cli.command("up")
def up():
    """Bring up the Opik server via Docker Compose."""
    compose = "docker-compose.opik.yml"
    click.echo("Starting Opik server…")
    ret = subprocess.call(["docker-compose", "-f", compose, "up", "-d"])
    sys.exit(ret)

@llm_evaluate_cli.command("down")
def down():
    """Tear down the Opik server."""
    compose = "docker-compose.opik.yml"
    click.echo("Stopping Opik server…")
    ret = subprocess.call(["docker-compose", "-f", compose, "down"])
    sys.exit(ret)
