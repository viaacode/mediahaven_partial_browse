# Get Partial

> Auto-generated documentation for [get_partial.get_partial](../../get_partial/get_partial.py) module.

Created on Mon Apr  4 13:27:58 2022
# get a partial browse
## Description:

- [Mediahaven_partial](../README.md#readme) / [Modules](../MODULES.md#mediahaven_partial-modules) / [Get Partial](index.md#get-partial) / Get Partial
- [Examples:](#examples)
    - [MhRequest](#mhrequest)
    - [check_export_status](#check_export_status)
        - [Description:](#description)
    - [dwnl](#dwnl)
    - [export_poll_status](#export_poll_status)
        - [Description:](#description)
    - [get_fragment_id](#get_fragment_id)
    - [get_partial](#get_partial)
    - [Description:](#description)
    - [get_token](#get_token)
        - [Description:](#description)
    - [main](#main)
    - [Description:](#description)

function export_partial:

- export a partial from mediahaven browse

# Examples:

- print(get_partial(pid='df6k09f48v',start_frames=14700,end_frames=19325))

- check_export_status('20220404_162824__viaa@viaa_b316b0e1-c45a-4136-9a19-29a9b2211c4e')

- print(export_poll_status('20220404_162824__viaa@viaa_b316b0e1-c45a-4136-9a19-29a9b2211c4e'))

@author: tina

#### Attributes

- `console` - define a Handler which writes INFO messages or higher to the sys.stderr: `logging.StreamHandler()`
- `formatter` - set a format which is simpler for console use: `logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')`

## MhRequest

[[find in source code]](../../get_partial/get_partial.py#L186)

```python
class MhRequest(object):
    def __init__(query, size=25, version=1):
```

### Description:
- Class with mediahaven query abstraction

## check_export_status

[[find in source code]](../../get_partial/get_partial.py#L96)

```python
def check_export_status(exportid):
```

### Description:

- checks the status of a madiahaven export job

#### Arguments

- exportid

#### Returns

- downloadable url

## dwnl

[[find in source code]](../../get_partial/get_partial.py#L240)

```python
@retry(
    (ValueError, TypeError, AttributeError),
    tries=20,
    delay=1,
    backoff=2,
    max_delay=4,
)
def dwnl(url, file):
```

fetch a file given a url

## export_poll_status

[[find in source code]](../../get_partial/get_partial.py#L141)

```python
def export_poll_status(exportid):
```

### Description:

- wait until file is ready for download

#### Arguments

- mediahaven exportid

## get_fragment_id

[[find in source code]](../../get_partial/get_partial.py#L232)

```python
@retry(
    (ValueError, TypeError, AttributeError),
    tries=20,
    delay=1,
    backoff=2,
    max_delay=4,
)
def get_fragment_id(pid):
```

Returns the fragmentId if given pid

## get_partial

[[find in source code]](../../get_partial/get_partial.py#L303)

```python
def get_partial(pid=None, filename=None, start_frames=0, end_frames=500):
```

## Description:

- export a fragment of a given pid using start and end frames

#### Arguments

- `pid` - meemoo pid id

- `filename` - optional, destination filename(path)

- `start_frames` - start of fragment in frames

- `end_frames` - end of fragment in frames

## get_token

[[find in source code]](../../get_partial/get_partial.py#L161)

```python
@retry(
    (ValueError, TypeError, AttributeError),
    tries=20,
    delay=1,
    backoff=2,
    max_delay=4,
)
def get_token():
```

### Description:

- get a token for mediahaven rest api using Oauth2

## main

[[find in source code]](../../get_partial/get_partial.py#L256)

```python
def main():
```

## Description:

- export a fragment of a given pid using start and end frames

#### Arguments

- `pid` - meemoo pid id

- `filename` - optional, destination filename(path)

- `start_frames` - start of fragment in frames

- `end_frames` - end of fragment in frames
