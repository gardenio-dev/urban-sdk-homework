from fastapi import Path

from urban_sdk_homework.modules.traffic.services import TrafficService

# Note to the Future: If we ever want to implement multi-tenancy, we can
# uncomment the tenant parameter and pass it to the service.
# def service(
#     tenant: str = Path(description="This is the tenant that owns the data."),
# ):
#     """
#     Get an traffic service instance for a tenant.

#     :param tenant: the tenant that owns the data
#     :returns: the service instance
#     """
#     return TrafficService.connect(tenant=tenant)


def service():
    """
    Get a traffic service instance for a tenant.

    :param tenant: the tenant that owns the data
    :returns: the service instance
    """
    return TrafficService.connect()