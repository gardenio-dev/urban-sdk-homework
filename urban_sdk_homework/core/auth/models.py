from frontegg.fastapi.secure_access import frontegg_security
from pydantic import ConfigDict


class Friend(frontegg_security.User):
    """
    A user.

    The ``User`` model is based on Frontegg's ``User`` model.
    """

    model_config = ConfigDict(populate_by_name=True)
