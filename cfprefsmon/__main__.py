from typing import Optional

import click
from maclog.log import get_logger
from pymobiledevice3.cli.cli_common import LockdownCommand
from pymobiledevice3.lockdown import LockdownClient
from pymobiledevice3.services.os_trace import OsTraceService

FORMAT = 'CFPreference[{domain}][{user}][{key}] = {value}  # Process: {procname}'

NO_VALUE_PREFIX = 'found no value '
HAS_VALUE_PREFIX = 'looked up value '
FOR_KEY_PREFIX = 'for key '
FOR_KEY_SUFFIX = 'in CFPref'
DOMAIN_PREFIX = '> (Domain: '
USER_PREFIX = ', User: '

DEFAULT_USER = 'kCFPreferencesAnyUser'

PREFS = {}


def print_entry(message: str, filename: str, subsystem: Optional[str] = None, category: Optional[str] = None,
                unique: bool = False, color: bool = False, undefined: bool = False) -> None:
    if subsystem != 'com.apple.defaults' or category != 'User Defaults':
        return

    if 'cfprefs' not in message.lower():
        return

    if not message.startswith(HAS_VALUE_PREFIX) and not message.startswith(NO_VALUE_PREFIX):
        return

    # print(message)
    user = DEFAULT_USER
    value = None

    key = message.split(FOR_KEY_PREFIX, 1)[1].split(FOR_KEY_SUFFIX, 1)[0].strip()
    domain = message.rsplit(DOMAIN_PREFIX, 1)[1].split(',', 1)[0].strip()
    procname = filename
    has_value = False

    if USER_PREFIX in message:
        user = message.rsplit(USER_PREFIX, 1)[1].split(',', 1)[0].strip()

    if not user:
        user = DEFAULT_USER

    if message.startswith(HAS_VALUE_PREFIX):
        value = message.split(HAS_VALUE_PREFIX, 1)[1].split(FOR_KEY_PREFIX, 1)[0]
        has_value = True

    if domain not in PREFS:
        PREFS[domain] = {}

    if user not in PREFS[domain]:
        PREFS[domain][user] = []

    if unique and key in PREFS[domain][user]:
        return

    PREFS[domain][user].append(key)

    if color:
        domain = click.style(domain, fg='yellow')
        user = click.style(user, fg='bright_green')
        key = click.style(key, fg='green')
        procname = click.style(procname, fg='magenta')

        if not has_value:
            value = click.style(value, fg='red')

    if (not undefined) or (undefined and not has_value):
        print(FORMAT.format(domain=domain, user=user, key=key, value=value, procname=procname))


@click.group()
def cli():
    pass


@cli.command()
@click.option('--unique', is_flag=True, help='output only unique entries')
@click.option('--color/--no-color', default=True, help='make colored output')
@click.option('--undefined', is_flag=True, help='filter only non-existing keys')
def host(unique, color, undefined):
    """ Sniff on macOS host """
    for entry in get_logger():
        print_entry(entry.event_message, entry.process_image_path, entry.subsystem, entry.category, unique=unique,
                    color=color, undefined=undefined)


@cli.command(cls=LockdownCommand)
@click.option('--unique', is_flag=True, help='output only unique entries')
@click.option('--color/--no-color', default=True, help='make colored output')
@click.option('--undefined', is_flag=True, help='filter only non-existing keys')
def mobile(service_provider: LockdownClient, unique, color, undefined):
    """ Sniff on connected iOS device """
    for entry in OsTraceService(service_provider).syslog():
        if entry.label is None:
            continue
        print_entry(entry.message, entry.filename, entry.label.subsystem, entry.label.category, unique=unique,
                    color=color, undefined=undefined)


if __name__ == '__main__':
    cli()
