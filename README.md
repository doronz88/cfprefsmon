# cfprefsmon

## Overview

`cfprefsmon` streams CFPreferences activity so you can spot interesting keys and values on a macOS host or a connected iOS device.

## Installation

```shell
python3 -m pip install -U cfprefsmon
```

## Usage

```none
 Usage: cfprefsmon [OPTIONS] COMMAND [ARGS]...

 Inspect CFPreferences activity on macOS hosts and iOS devices.

╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.                                                           │
│ --show-completion             Show completion for the current shell, to copy it or customize the installation.                    │
│ --help                        Show this message and exit.                                                                         │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ host     Stream CFPreferences activity from the macOS host.                                                                       │
│ mobile   Stream CFPreferences activity from a connected iOS device.                                                               │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## Examples

In this example, several preferences resolve to `None`, which can hint at uninitialized or internal-only settings.

```none
➜  cfprefmon git:(master) ✗ cfprefsmon mobile
CFPreference[com.apple.springboard][kCFPreferencesAnyUser][SBDisableHomeButton] = 0   # Process: /System/Library/CoreServices/SpringBoard.app/SpringBoard
CFPreference[com.apple.springboard][kCFPreferencesAnyUser][SBStoreDemoAppLock] = 0   # Process: /System/Library/CoreServices/SpringBoard.app/SpringBoard
CFPreference[com.apple.springboard][kCFPreferencesAnyUser][ThermalLockoutEnabledBrickMode] = 0   # Process: /System/Library/CoreServices/SpringBoard.app/SpringBoard
CFPreference[com.apple.backboardd][kCFPreferencesAnyUser][BKForceMirroredOrientation] = None  # Process: /usr/libexec/backboardd
CFPreference[com.apple.backboardd][kCFPreferencesAnyUser][BKForceMirroredOrientation] = None  # Process: /usr/libexec/backboardd
CFPreference[com.apple.iokit.IOMobileGraphicsFamily][kCFPreferencesAnyUser][canvas_width] = None  # Process: /System/Library/CoreServices/SpringBoard.app/SpringBoard
CFPreference[com.apple.iokit.IOMobileGraphicsFamily][kCFPreferencesAnyUser][canvas_height] = None  # Process: /System/Library/CoreServices/SpringBoard.app/SpringBoard
CFPreference[com.apple.iokit.IOMobileGraphicsFamily][kCFPreferencesAnyUser][enable_ktrace] = None  # Process: /System/Library/CoreServices/SpringBoard.app/SpringBoard
CFPreference[com.apple.iokit.IOMobileGraphicsFamily][kCFPreferencesAnyUser][override_display_width] = None  # Process: /System/Library/CoreServices/SpringBoard.app/SpringBoard
CFPreference[com.apple.iokit.IOMobileGraphicsFamily][kCFPreferencesAnyUser][override_display_height] = None  # Process: /System/Library/CoreServices/SpringBoard.app/SpringBoard
CFPreference[com.apple.iokit.IOMobileGraphicsFamily][kCFPreferencesAnyUser][override_panel_width] = None  # Process: /System/Library/CoreServices/SpringBoard.app/SpringBoard
CFPreference[com.apple.iokit.IOMobileGraphicsFamily][kCFPreferencesAnyUser][override_panel_height] = None  # Process: /System/Library/CoreServices/SpringBoard.app/SpringBoard
CFPreference[com.apple.iokit.IOMobileGraphicsFamily][kCFPreferencesAnyUser][benchmark] = None  # Process: /System/Library/CoreServices/SpringBoard.app/SpringBoard
CFPreference[com.apple.coreservices.useractivityd][kCFPreferencesAnyUser][ActivityAdvertisingAllowed] = 1   # Process: /System/Library/PrivateFrameworks/UserActivity.framework/Agents/useractivityd
CFPreference[com.apple.coreservices.useractivityd][kCFPreferencesAnyUser][ActivityAdvertisingAllowed] = 1   # Process: /System/Library/PrivateFrameworks/UserActivity.framework/Agents/useractivityd
CFPreference[com.apple.coreservices.useractivityd][kCFPreferencesAnyUser][EnableHandoffInPowerSaverMode] = 1   # Process: /System/Library/PrivateFrameworks/UserActivity.framework/Agents/useractivityd
...
```

Filter to a single domain and specific users:

```shell
cfprefsmon mobile --domain 'com.apple.softwareupdateservicesd' --user 'kCFPreferencescurrentUser' --user 'mobile'
```

Only output entries when values change during monitoring:

```shell
cfprefsmon mobile --value-change
```
