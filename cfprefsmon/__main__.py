from typing import Annotated, Optional

import typer
from maclog.log import get_logger
from pymobiledevice3.cli.cli_common import ServiceProviderDep, user_requested_colored_output
from pymobiledevice3.services.os_trace import OsTraceService
from typer_injector import InjectingTyper

FORMAT = "CFPreference[{domain}][{user}][{key}] = {value}  # Process: {procname}"

NO_VALUE_PREFIX = "found no value "
HAS_VALUE_PREFIX = "looked up value "
FOR_KEY_PREFIX = "for key "
FOR_KEY_SUFFIX = "in CFPref"
DOMAIN_PREFIX = "> (Domain: "
USER_PREFIX = ", User: "

DEFAULT_USER = "kCFPreferencesAnyUser"

PREFS = {}

UniqueOption = Annotated[bool, typer.Option("--unique", help="output only unique entries", is_flag=True)]
UndefinedOption = Annotated[bool, typer.Option("--undefined", help="filter only non-existing keys", is_flag=True)]
HostDomainFilterOption = Annotated[
    Optional[list[str]], typer.Option("--domain-filter", help="filter only given domain")
]
HostUserFilterOption = Annotated[Optional[list[str]], typer.Option("--user-filter", help="filter only given user")]
MobileDomainFilterOption = Annotated[
    Optional[list[str]],
    typer.Option("--domain", help="filter only given domain"),
]
MobileUserFilterOption = Annotated[
    Optional[list[str]],
    typer.Option("--user", help="filter only given user"),
]
ValueChangeOption = Annotated[bool, typer.Option("--value-change", help="output only on value change", is_flag=True)]


def print_entry(
    message: str,
    filename: str,
    subsystem: Optional[str] = None,
    category: Optional[str] = None,
    unique: bool = False,
    color: bool = False,
    undefined: bool = False,
    domain_filter: Optional[list[str]] = None,
    user_filter: Optional[list[str]] = None,
    value_change: bool = False,
) -> None:
    if subsystem != "com.apple.defaults" or category != "User Defaults":
        return

    if "cfprefs" not in message.lower():
        return

    if not message.startswith(HAS_VALUE_PREFIX) and not message.startswith(NO_VALUE_PREFIX):
        return

    # print(message)
    user = DEFAULT_USER
    value = None

    key = message.split(FOR_KEY_PREFIX, 1)[1].split(FOR_KEY_SUFFIX, 1)[0].strip()
    domain = message.rsplit(DOMAIN_PREFIX, 1)[1].split(",", 1)[0].strip()
    procname = filename
    has_value = False

    if USER_PREFIX in message:
        user = message.rsplit(USER_PREFIX, 1)[1].split(",", 1)[0].strip()

    if not user:
        user = DEFAULT_USER

    if message.startswith(HAS_VALUE_PREFIX):
        value = message.split(HAS_VALUE_PREFIX, 1)[1].split(FOR_KEY_PREFIX, 1)[0]
        has_value = True

    if domain not in PREFS:
        PREFS[domain] = {}

    if user not in PREFS[domain]:
        PREFS[domain][user] = {}

    # filter output according to user supplied domain/user
    if (domain_filter and domain not in domain_filter) or (user_filter and user not in user_filter):
        return

    if unique and key in PREFS[domain][user]:
        return

    # skip if not unique or value has not changed
    skip = False
    if key in PREFS[domain][user] and ((value_change and value == PREFS[domain][user][key]) or unique):
        skip = True
    if skip:
        return

    PREFS[domain][user][key] = value

    if color:
        domain = typer.style(domain, fg="yellow")
        user = typer.style(user, fg="bright_green")
        key = typer.style(key, fg="green")
        procname = typer.style(procname, fg="magenta")

        if not has_value:
            value = typer.style(value, fg="red")

    if (not undefined) or (undefined and not has_value):
        print(FORMAT.format(domain=domain, user=user, key=key, value=value, procname=procname))


cli = InjectingTyper(
    help="Discover interesting CFPreferences values on iDevices.",
    no_args_is_help=True,
)


@cli.command()
def host(
    unique: UniqueOption = False,
    undefined: UndefinedOption = False,
    domain_filter: HostDomainFilterOption = None,
    user_filter: HostUserFilterOption = None,
    value_change: ValueChangeOption = False,
):
    """Sniff over macOS host"""
    for entry in get_logger():
        print_entry(
            entry.event_message,
            entry.process_image_path,
            entry.subsystem,
            entry.category,
            unique=unique,
            undefined=undefined,
            color=user_requested_colored_output(),
            domain_filter=domain_filter,
            user_filter=user_filter,
            value_change=value_change,
        )


@cli.command()
def mobile(
    service_provider: ServiceProviderDep,
    unique: UniqueOption = False,
    undefined: UndefinedOption = False,
    domain_filter: MobileDomainFilterOption = None,
    user_filter: MobileUserFilterOption = None,
    value_change: ValueChangeOption = False,
):
    """Sniff over connected iOS device"""
    for entry in OsTraceService(service_provider).syslog():
        if entry.label is None:
            continue
        print_entry(
            entry.message,
            entry.filename,
            entry.label.subsystem,
            entry.label.category,
            unique=unique,
            undefined=undefined,
            color=user_requested_colored_output(),
            domain_filter=domain_filter,
            user_filter=user_filter,
            value_change=value_change,
        )


if __name__ == "__main__":
    cli()
