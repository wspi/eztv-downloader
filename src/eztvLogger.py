#!/usr/bin/env python

import logging, ConfigParser

Conf = ConfigParser.RawConfigParser()
Conf.read("/etc/eztv-downloader/Conf")

logName = Conf.get('Log', 'filename')

if Conf.has_option('Log', 'level'):
    logLevel = Conf.get('Log', 'level')
else:
    logLevel = 'INFO'

logging.basicConfig(level=logLevel,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename=logName,
                    filemode='a')
