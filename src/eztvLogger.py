#!/usr/bin/env python

import logging, ConfigParser

Conf = ConfigParser.RawConfigParser()
Conf.read("/etc/eztv-downloader/Conf")

logName = Conf.get('Log', 'path') + Conf.get('Log', 'name')

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename=logName,
                    filemode='w')
