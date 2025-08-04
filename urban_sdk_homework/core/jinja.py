from functools import lru_cache

import jinja2


@lru_cache(maxsize=1)
def env() -> jinja2.Environment:
    """Get the Jinja2 environment."""
    return jinja2.Environment(autoescape=True)
