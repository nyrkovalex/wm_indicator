wm_indicator
============

Simple appindicator to switch window managers.

Any wm that supports `--replace` option can be added to `SUPPORTED_MANAGERS`
dictionary. 
Application automatically detects if window manager executable is available 
on `$PATH` and skips nonexisting managers.

In order to use provided icon it should be placed under `~/.icons` path.
