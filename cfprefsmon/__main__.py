from collections import namedtuple

from pymobiledevice3.lockdown import LockdownClient
from pymobiledevice3.services.os_trace import OsTraceService

import click

FORMAT = 'CFPreference[{domain}][{user}][{key}] = {value}  # Process: {procname}'

NO_VALUE_PREFIX = 'found no value '
HAS_VALUE_PREFIX = 'looked up value '
FOR_KEY_PREFIX = 'for key '
FOR_KEY_SUFFIX = 'in CFPref'
DOMAIN_PREFIX = '> (Domain: '
USER_PREFIX = ', User: '

DEFAULT_USER = 'kCFPreferencesAnyUser'


@click.command()
@click.option('--udid')
@click.option('--unique', is_flag=True, help='output only unique entries')
@click.option('--color/--no-color', default=True, help='make colored output')
@click.option('--undefined', is_flag=True, help='filter only non-existing keys')
def cli(udid, unique, color, undefined):
    lockdown = LockdownClient(udid=udid)
    prefs = {}
    for entry in OsTraceService(lockdown).syslog():
        if entry.label is None:
            continue

        if entry.label.subsystem != 'com.apple.defaults' or entry.label.category != 'User Defaults':
            continue

        message = entry.message

        if 'cfprefs' not in message.lower():
            continue

        if not message.startswith(HAS_VALUE_PREFIX) and not message.startswith(NO_VALUE_PREFIX):
            continue

        # print(message)
        user = DEFAULT_USER
        value = None

        key = message.split(FOR_KEY_PREFIX, 1)[1].split(FOR_KEY_SUFFIX, 1)[0].strip()
        domain = message.rsplit(DOMAIN_PREFIX, 1)[1].split(',', 1)[0].strip()
        procname = entry.filename
        has_value = False

        if USER_PREFIX in message:
            user = message.rsplit(USER_PREFIX, 1)[1].split(',', 1)[0].strip()

        if not user:
            user = DEFAULT_USER

        if message.startswith(HAS_VALUE_PREFIX):
            value = message.split(HAS_VALUE_PREFIX, 1)[1].split(FOR_KEY_PREFIX, 1)[0]
            has_value = True

        if domain not in prefs:
            prefs[domain] = {}

        if user not in prefs[domain]:
            prefs[domain][user] = []

        if unique and key in prefs[domain][user]:
            continue

        prefs[domain][user].append(key)

        if color:
            domain = click.style(domain, fg='yellow')
            user = click.style(user, fg='bright_green')
            key = click.style(key, fg='green')
            procname = click.style(procname, fg='magenta')

            if not has_value:
                value = click.style(value, fg='red')

        if (not undefined) or (undefined and not has_value):
            print(FORMAT.format(domain=domain, user=user, key=key, value=value, procname=procname))


if __name__ == '__main__':
    cli()
