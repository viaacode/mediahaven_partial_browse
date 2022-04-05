# convert

> Auto-generated documentation for [timecode_helper.convert](../../timecode_helper/convert.py) module.

Created on Tue Apr  5 08:59:37 2022
## Examples:

- [Mediahaven_partial](../README.md#readme) / [Modules](../MODULES.md#mediahaven_partial-modules) / [Timecode Helper](index.md#timecode-helper) / convert
    - [convert](#convert)
        - [convert().frames_to_timecode](#convertframes_to_timecode)
        - [convert().timecode_to_frames](#converttimecode_to_frames)
    - [main](#main)
    - [Description:](#description)

print(convert(value='10:08:06:12',framerate=25,start='10:00:00:00').timecode_to_frames())

print(convert(value=600,framerate=25,start=500).frames_to_timecode())

print(convert(value='00:08:06:12',framerate=25,start='00:00:00:00')())

based on the work found in https://stackoverflow.com/a/34607115

#### TODO:
    - consider usiong the meemoo logger

@author: tina

#### Attributes

- `console` - define a Handler which writes INFO messages or higher to the sys.stderr: `logging.StreamHandler()`
- `formatter` - set a format which is simpler for console use: `logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')`

## convert

[[find in source code]](../../timecode_helper/convert.py#L62)

```python
class convert(object):
    def __init__(value, framerate, start=0):
```

### convert().frames_to_timecode

[[find in source code]](../../timecode_helper/convert.py#L87)

```python
def frames_to_timecode(start=None):
```

### convert().timecode_to_frames

[[find in source code]](../../timecode_helper/convert.py#L81)

```python
def timecode_to_frames(start=None):
```

## main

[[find in source code]](../../timecode_helper/convert.py#L94)

```python
def main():
```

## Description:

- convert a timecode string to frames or frames to timecode

#### Arguments

- `value` - string or int

- `start` - ofset start time eg 10:00:00:00

- `framerate` - nr of frames / second
