#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 13:27:58 2022
# get a partial browse
## Description:

    function export_partial:

        - export a partial from mediahaven browse

# Examples:

    - print(get_partial(pid='df6k09f48v',start_frames=14700,end_frames=19325))

    - check_export_status('20220404_162824__viaa@viaa_b316b0e1-c45a-4136-9a19-29a9b2211c4e')

    - print(export_poll_status('20220404_162824__viaa@viaa_b316b0e1-c45a-4136-9a19-29a9b2211c4e'))

@author: tina
"""
import argparse
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import logging
from retry import retry
#from pprint import pprint
from string import Template
import time
import shutil
from viaa.configuration import ConfigParser
config = ConfigParser()
mh_user = config.app_cfg['get_partial']['mh_user']
mh_password = config.app_cfg['get_partial']['mh_password']
mh_client_id = config.app_cfg['get_partial']['mh_client_id']
mh_client_secret = config.app_cfg['get_partial']['mh_client_secret']
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

token = ''
BASEURL = 'https://archief.viaa.be/mediahaven-rest-api/v2/records?q='
EXPORT_URL= 'https://archief.viaa.be/mediahaven-rest-api/v2/exports'
http_proxy = ""
https_proxy = ""
ftp_proxy = ""
proxyDict = {
    "http": http_proxy,
    "https": https_proxy,
    "ftp": ftp_proxy
}
queryTemplate= Template("""
{
  "Records": [
    {
      "RecordId": "$fragId",
      "Filename": "$pid",
      "Partial": {
        "Type": "Frames",
        "Start": $start_frames,
        "End": $end_frames
      }
    }
  ],
  "Filename": "$filename",
  "ExportLocationId": "810",
  "Reason": "GIVE proj",
  "DestinationPath": "",
  "UseOriginal": false,
  "Options": {
    "Metadata": {
      "Type": "Sidecar",
      "Format": "Mhs",
      "OnlyMetadata": false
    }
  }
}
    """)

def check_export_status(exportid):
    """### Description:

        - checks the status of a madiahaven export job
    Args:

        - exportid

    Returns:

        - downloadable url

    """
    url = EXPORT_URL  + '/' +exportid
    global token
    s = requests.Session()
    retries = Retry(total=5,
                    backoff_factor=2,
                    status_forcelist=[502, 503, 504])
    s.mount('https://', HTTPAdapter(max_retries=retries))
    logger.info('GET using: ' + url+ exportid)
    header = {'Authorization': token}
    r = s.get(url,
              headers=header,
              proxies=proxyDict)
    logger.info('Rest status code: %s ' % r.status_code)
    if r.status_code == 401:
        token = get_token()
        header = {'Authorization': token}
        r = s.get(url,
                  headers=header,
                  proxies=proxyDict)
    try:
        download_url = r.json()['DownloadUrl']
        logger.info('download: ' + download_url)
    except IndexError as e:
        logger.warning('no results , err: %s' % e)
        return 'NULL'
    except KeyError:
        logger.warning('rest out: ' + str(r.json()))

    return download_url



def export_poll_status(exportid):
    """### Description:

        - wait until file is ready for download

    Args:

        - mediahaven exportid

    """
    while True:
        r = check_export_status(exportid)
        print(r)
        if r == '':
            time.sleep(15)
            logger.warning('file not ready yet')
        else:
            return r


@retry((ValueError, TypeError, AttributeError), tries=20, delay=1, backoff=2,
       max_delay=4)
def get_token():
    """### Description:

        - get a token for mediahaven rest api using Oauth2

    """
    url = 'https://archief.viaa.be/auth/ropc.php'

    payload = {'client_id': mh_client_id,
               'client_secret':mh_client_secret,
               'username': mh_user,
               'password':mh_password}
    r = requests.post(url,
                      data=payload)
    try:
        rtoken = r.json()['access_token']
        token = 'Bearer ' + rtoken
        logger.info('got a token: {}'.format(token))
    except Exception:
        return None
    return token


class MhRequest(object):
    """### Description:
        - Class with mediahaven query abstraction"""
    def __init__(self, query,

                 size=25,
                 version=1):
        self.query_string = query
        self.size = size
        self.url_base = BASEURL
        self.token = None
        self.externalId = 'null'
        self.status = 'not_found'


    def __call__(self):
        global token
        if self.token is not None:
            token = self.token
        s = requests.Session()
        retries = Retry(total=5,
                        backoff_factor=2,
                        status_forcelist=[502, 503, 504])
        s.mount('https://', HTTPAdapter(max_retries=retries))
        logger.info('GET using: ' + self.url_base + self.query_string)
        header = {'Authorization': token}
        r = s.get(self.url_base + self.query_string,
                  headers=header,
                  proxies=proxyDict)
        logger.info('Rest status code: %s ' % r.status_code)
        if r.status_code == 401:
            token = get_token()
            header = {'Authorization': token}
            r = s.get(self.url_base + self.query_string,
                      headers=header,
                      proxies=proxyDict)
        try:
            return r.json()
        except IndexError as e:
            logger.warning('no results , err: %s' % e)
            return 'NULL'
        except KeyError:
            logger.warning('rest out: ' + str(r.json()))



@retry((ValueError, TypeError, AttributeError), tries=20, delay=1, backoff=2,
       max_delay=4)
def get_fragment_id(pid):
    """Returns the fragmentId if given pid"""
    o = MhRequest(query='%2B(PID:{})'.format(pid))()
    if o['NrOfResults'] >= 2:
        for i in o['Results']:
            if i['Internal']['BrowseStatus'] != "no_browse":
                return i['Internal']['FragmentId']
    else:
        #print(o)
        fragment_id=o['Results'][0]['Internal']['FragmentId']
        return fragment_id
#print(get_fragment_id('6w96715g4g'))
@retry((ValueError, TypeError, AttributeError), tries=20, delay=1, backoff=2,
       max_delay=4)
def dwnl(url, file):
    """fetch a file given a url"""
    try:
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with open(file, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
        logger.info('File downloaded {}'.format(file))
        return True
    except Exception as e:
        logger.error(str(e))


def main():
    """## Description:

        - export a fragment of a given pid using start and end frames

    Args:
         pid: meemoo pid id

        filename: optional, destination filename(path)

        start_frames: start of fragment in frames

        end_frames: end of fragment in frames

    """
    parser = argparse.ArgumentParser(description="export mediahaven partial from browse")
    parser.add_argument(
      "-p",
      "--pid",
      help="meemoo PID.",
      required=True,
      )
    parser.add_argument(
      "-s",
      "--start_frames",
      help="start frame",
      required=True,
      )
    parser.add_argument(
      "-e",
      "--end_frames",
      help="end frame",
      required=True,
      )
    parser.add_argument(
      "-f",
      "--filename",
      help="file/path.mp4",
      required=True,
      )
    args = parser.parse_args()
    logger.info(str(args))
    get_partial(pid=args.pid,
                filename=args.filename,
                start_frames=args.start_frames,
                end_frames=args.end_frames)

def get_partial(pid=None,filename=None,
                   start_frames=0,end_frames=500):
    """## Description:

        - export a fragment of a given pid using start and end frames

    Args:
         pid: meemoo pid id

        filename: optional, destination filename(path)

        start_frames: start of fragment in frames

        end_frames: end of fragment in frames

    """
    fragId = get_fragment_id(pid=pid)
    if filename is None:
        filename = pid+'-patrtial'+'.mp4'
    efilename = filename.replace('/','_')
    query = queryTemplate.substitute(pid=pid,
                                     fragId=fragId,
                                     start_frames=start_frames,
                                     end_frames=end_frames,
                                     filename=efilename)
    global token
    s = requests.Session()
    retries = Retry(total=5,
                    backoff_factor=2,
                    status_forcelist=[502, 503, 504])
    s.mount('https://', HTTPAdapter(max_retries=retries))
    logger.info('POST using: ' + EXPORT_URL+ str(query))
    header = {'Authorization': token}
    r = s.post(EXPORT_URL,
              headers=header,
              proxies=proxyDict,
              data=query)
    logger.info('Rest status code: %s ' % r.status_code)
    if r.status_code == 401:
        token = get_token()
        header = {'Authorization': token}
        r = s.post(EXPORT_URL,
                  headers=header,
                  proxies=proxyDict,
                  data=query)
    print(str(r.json()))
    exportid =  r.json()[0]['ExportJobId']
    logger.info('checking id: '+ exportid)
    url=export_poll_status(exportid)
    dwnl(url, filename)
    return r.json()





if __name__ == '__main__':
    main()
