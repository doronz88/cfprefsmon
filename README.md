# Description

Simple utility to search for interesting preferences in iDevices.

# Installation

```shell
python3 -m pip install -U --user cfprefsmon
```

# Example

In this example, where the value for each preference is `None`, this is probably some hidden feature we can maybe enable
on a jailbroken device.

```
➜  cfprefmon git:(master) ✗ cfprefsmon
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
