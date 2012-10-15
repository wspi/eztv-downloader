#!/usr/bin/env python

import logging, ConfigParser

Conf = ConfigParser.RawConfigParser()
Conf.read("/etc/eztv-downloader/Conf")

logName = Conf.get('Log', 'filename')

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename=logName,
                    filemode='a')
