import importlib
import pkgutil
from functools import lru_cache
from typing import Pattern
from typing import Tuple
from typing import Type

from urban_sdk_homework.core.logging import logger


@lru_cache(maxsize=1)
def load_submodules(module, pattern: Pattern = None, verbose: bool = False):
    """
    Load all submodules within a module.

    :param module: the parent module
    :param pattern: a regular expression to match submodule names
    :param verbose: whether to log the loading of submodules
    """
    for loader, module_name, is_pkg in pkgutil.walk_packages(
        module.__path__,
        f"{module.__name__}.",
    ):
        if pattern and not pattern.match(module_name):
            continue
        if verbose:
            logger().debug(
                f"Loading submodule {module_name}.",
                module=module.__name__,
                submodule=module_name,
            )
        importlib.import_module(module_name)


def subclasses(t: Type) -> Tuple[Type]:
    """Get all subclasses of a type recursively."""
    subs = set(t.__subclasses__())
    for sub in tuple(subs):
        subs.update(subclasses(sub))
    return tuple(subs)
