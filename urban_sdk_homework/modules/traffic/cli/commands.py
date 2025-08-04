from click import pass_context
from click import pass_obj

from urban_sdk_homework.cli import main
from urban_sdk_homework.core.click import multi_tenant
from urban_sdk_homework.core.console import pprint
from urban_sdk_homework.modules.traffic.services import TrafficService


@main.group()
@multi_tenant
@pass_context
def traffic(ctx, tenant: str):
    """traffic subcommands."""
    ctx.obj = TrafficService.connect(tenant=tenant)


@traffic.command()
@pass_obj
def say_hello(
    service: TrafficService,
):
    """Get a friendly greeting."""
    pprint(service.say_hello())
