import typing as t
from functools import wraps

import click
import typing_extensions as te


P = te.ParamSpec("P")
R = t.TypeVar("R")
T = t.TypeVar("T")
_AnyCallable = t.Callable[..., t.Any]


def multi_tenant(
    func: "t.Callable[te.Concatenate[str, P], R]",
) -> "t.Callable[P, R]":
    """Marks a command as requiring a tenant parameters."""

    @click.option(
        "-t",
        "--tenant",
        "--for",
        required=True,
        type=click.STRING,
        help="the tenant identifier",
    )
    @wraps(func)
    def wrapper(*args: "P.args", tenant: str, **kwargs: "P.kwargs") -> "R":
        return func(*args, tenant=tenant, **kwargs)  # type: ignore

    return wrapper  # type: ignore
