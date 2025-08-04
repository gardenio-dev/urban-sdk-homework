from typing import List

from fastapi import Depends

from urban_sdk_homework.core.auth.models import Friend
from urban_sdk_homework.core.auth.providers import AuthProvider
from urban_sdk_homework.core.fastapi import APIRouter

router = APIRouter(
    tags=["Auth"],
    dependencies=[],
    prefix="",
)

# TODO: Errors coming later.
# errors = {
#     403: {"model": ErrorMessage},
#     500: {"model": ErrorMessage},
#     503: {"model": ErrorMessage},
# }


def auth(
    permissions: List[str] = None,
    auto_error: bool = True,
    roles: List[str] = None,
    super_user: bool = False,
    multi_tenant: bool = True,
):
    """
    Secure endpoints.

    :param permissions: required permissions
    :param auto_error: raise exceptions on security failure
    :param roles: required roles
    :param super_user: requires super-user permissions
    :param multi_tenant: require users to be authenticated to the tenant
    """
    return AuthProvider.connect().auth(
        permissions=permissions,
        auto_error=auto_error,
        roles=roles,
        super_user=super_user,
        multi_tenant=multi_tenant,
    )


@router.get(
    "/whoami",
    name="whoami",
    response_model=Friend,
    response_model_by_alias=True,
    # responses=errors,
)
async def whoami(
    friend: Friend = Depends(auth(multi_tenant=False)),
) -> Friend:
    """Get the current user."""
    return friend
