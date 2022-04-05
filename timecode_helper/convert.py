#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 08:59:37 2022
## Examples:

    print(convert(value='10:08:06:12',framerate=25,start='10:00:00:00').timecode_to_frames())

    print(convert(value=600,framerate=25,start=500).frames_to_timecode())

    print(convert(value='00:08:06:12',framerate=25,start='00:00:00:00')())

based on the work found in https://stackoverflow.com/a/34607115

#### TODO:
    - consider usiong the meemoo logger

@author: tina
"""
import argparse
import logging
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
logger = logging.getLogger(__name__)  # root logger
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='exporter.log',
                    filemode='a')
# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# set a format which is simpler for console use
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('__main__').addHandler(console)

def _timecode(seconds, framerate):
    return '{h:02d}:{m:02d}:{s:02d}:{f:02d}' \
            .format(h=int(seconds/3600),
                    m=int(seconds/60%60),
                    s=int(seconds%60),
                    f=round((seconds-int(seconds))* framerate))


def _frames(seconds, framerate):
    return seconds * framerate


def _seconds(value,framerate):
    if isinstance(value, str):
        _zip_ft = zip((3600, 60, 1, 1/framerate), value.split(':'))
        return sum(f * float(t) for f,t in _zip_ft)
    elif isinstance(value, (int, float)):  # frames
        return value / framerate
    else:
        return 0

class convert(object):
    def __init__(self, value, framerate,start=0):
        self.framerate = framerate
        self.value = value
        self.start = start

    def __call__(self):
        if isinstance(self.value, str):
            timecode = self.value
            return _frames(_seconds(timecode,
                                    self.framerate) - _seconds(self.start,
                                                               self.framerate),
                                                               self.framerate)
        elif isinstance(self.value, (int, float)):
            frames = self.value
            return _timecode(_seconds(frames,
                                      self.framerate) + _seconds(self.start,
                                                                 self.framerate),
                                                                 self.framerate)
    def timecode_to_frames(self,start=None):
        timecode = self.value
        return _frames(_seconds(timecode,
                                self.framerate) - _seconds(self.start,
                                                           self.framerate),
                                                           self.framerate)
    def frames_to_timecode(self,start=None):
        frames = self.value
        return _timecode(_seconds(frames,
                                  self.framerate) + _seconds(self.start,
                                                             self.framerate),
                                                             self.framerate)

def main():
    """## Description:

        - convert a timecode string to frames or frames to timecode

    Args:
         value: string or int

        start: ofset start time eg 10:00:00:00

        framerate: nr of frames / second


    """
    parser = argparse.ArgumentParser(description="export mediahaven partial from browse")
    parser.add_argument(
      "-v",
      "--value",
      help="10:00:00:00 or int 600",
      required=True,
      )
    parser.add_argument(
      "-s",
      "--start",
      help="start frame",
      required=True,
      )
    parser.add_argument(
      "-r",
      "--framerate",
      help="nr of frames / seconds",
      required=True,
      )
    args = parser.parse_args()
    logger.info(str(args))
    o = convert(value=args.value,framerate=int(args.framerate),start=args.start)()
    o = int(round(o))
    print(str(o))
    logger.info(str(o))
    return o


if __name__ == '__main__':
    main()
