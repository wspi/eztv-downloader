#!/usr/bin/env python

import logging, ConfigParser

Conf = ConfigParser.RawConfigParser()
Conf.read("/etc/eztv-downloader/Conf")

logName = Conf.get('Log', 'filename')
logLevel = Conf.get('Log', 'level')

logging.basicConfig(level=logLevel,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename=logName,
                    filemode='a')
