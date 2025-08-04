import json
from typing import Any

import rich

from urban_sdk_homework.core.models import BaseModel
from urban_sdk_homework.core.settings.base import BaseSettings


def pprint(data: Any):
    """Pretty print the data."""
    if isinstance(data, (BaseModel, BaseSettings)):
        rich.print_json(data.model_dump_json(indent=2))
    elif isinstance(data, dict):
        rich.print(json.dumps(data, indent=2))
    elif isinstance(data, (list, tuple)):
        rich.print(
            [
                item.model_dump() if isinstance(item, BaseModel) else item
                for item in data
            ]
        )
    else:
        rich.print(data)
