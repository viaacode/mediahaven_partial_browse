# README

## Install
install meemoo chassis from https://github.com/viaacode/chassis.py

run installer 
`python setup.py install`

## configure
create a config file like below `config.yml`

```
viaa:
  logging:
    level: DEBUG

app:
  get_partial:
    mh_user: mh_user
    mh_password: mh_pass
    mh_client_id: oauth_id
    mh_client_secret: oauth_secret


```
## scripts
```
mediahaven_partial -h
usage: mediahaven_partial [-h] -p PID -s START_FRAMES -e END_FRAMES -f FILENAME

export mediahaven partial from browse

optional arguments:
  -h, --help            show this help message and exit
  -p PID, --pid PID     meemoo PID.
  -s START_FRAMES, --start_frames START_FRAMES
                        start frame
  -e END_FRAMES, --end_frames END_FRAMES
                        end frame
  -f FILENAME, --filename FILENAME
                        file/path.mp4
```
and 
```
usage: timecode_convert [-h] -v VALUE -s START -r FRAMERATE

export mediahaven partial from browse

optional arguments:
  -h, --help            show this help message and exit
  -v VALUE, --value VALUE
                        10:00:00:00 or int 600
  -s START, --start START
                        start frame
  -r FRAMERATE, --framerate FRAMERATE
                        nr of frames / seconds

```

## scripts examples

```
timecode_convert -v 10:00:66 -s 10:00:00 -r 25
1650
mediahaven_partial -p df6k09f48v -s 14700 -e 19325 -f test.mp4

```
