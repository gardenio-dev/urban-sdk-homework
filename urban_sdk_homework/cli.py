import importlib
import re
import sys

import click

from urban_sdk_homework.core import logging
from urban_sdk_homework.core.modules import load_submodules


@click.group(invoke_without_command=True)
@click.option(
    "-v",
    "--version",
    is_flag=True,
)
def main(version: bool):
    """Deploy and Manage IO."""
    # If the caller has requested the version, give 'em what they asked for.
    if version:
        from urban_sdk_homework.core.project.metadata import metadata

        print(f"{metadata().name} {metadata().version}")
        sys.exit(1)
    logging.configure()


def run():
    """Run the command-line interface."""
    # Resolve the current package name.
    package = __name__.split(".")[0]
    # Load all CLI submodules within the modules package.
    load_submodules(
        importlib.import_module(f"{package}.modules"),
        pattern=re.compile(rf"{package}.modules\.\w+\.cli\..*$"),
    )
    # Call the main group.
    main()