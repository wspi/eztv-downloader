#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser, sys, urllib, re, traceback, eztvLogger 

filename = sys.argv[1].title()

if ('The ' in filename):
	filename = filename.split('The ')[1]

if (' Of ' in filename):
	filename = filename.replace(' Of ', ' of ')

season = sys.argv[2]
episode = sys.argv[3]

try:

	url = urllib.urlopen("http://eztv.it")
	site = url.read()
	url.close()

	id = str(re.findall("value\=\"\d+.\>" + filename + ".", site)).split("\"")[1]

	config = ConfigParser.RawConfigParser()

	config.add_section('Serie')
	config.set('Serie', 'id', id)
	config.set('Serie', 'Season', season)
	config.set('Serie', 'Episode', episode)

	with open('/etc/eztv-downloader/shows/' + filename.replace(' ', '') + '.cfg', 'wb') as configfile:
		config.write(configfile)
        eztvLogger.logging.info("Serie " + filename + " criada!")
except:
	print "Nenhuma série encontrada com esse nome"
	traceback.print_exc(file=sys.stdout)
