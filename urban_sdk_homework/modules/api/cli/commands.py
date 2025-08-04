from pathlib import Path

import click
from click import pass_context
from click import pass_obj

from urban_sdk_homework.cli import main
from urban_sdk_homework.modules.api.services import ApiService


@main.group(name="api")
@pass_context
def api_(ctx):
    """Web API subcommands."""
    ctx.obj = ApiService.connect()


@api_.command()
@click.option(
    "-R",
    "--reload",
    is_flag=True,
    help="Reload the service after code changes. (This is for development.)",
)
@click.option(
    "-E",
    "--envfile",
    type=click.Path(dir_okay=False, resolve_path=True, readable=True),
)
@pass_obj
def start(service: ApiService, envfile: str, reload: bool):
    """Create a tenant database."""
    service.start(envfile=Path(envfile) if envfile else None, reload=reload)
