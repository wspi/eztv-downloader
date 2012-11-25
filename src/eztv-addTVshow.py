#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser, sys, urllib, re, traceback, eztvLogger 

if (len(sys.argv) < 4):
    print "usage: " + sys.argv[0] + " \"TV Show\" Season Episode [quality]"
    sys.exit(1)


filename = sys.argv[1].title()

if ('The ' in filename):
	filename = filename.split('The ')[1]

if (' Of ' in filename):
	filename = filename.replace(' Of ', ' of ')

season = sys.argv[2]
episode = sys.argv[3]

if len(sys.argv) == 5:
    quality = sys.argv[4]
else:
    quality = 'either'

if re.match('^(720p|hdtv|either)$', quality, re.I):
    quality.lower()
else:
    print "quality must be either HDTV or 720p"
    sys.exit(1)

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
	config.set('Serie', 'Quality', quality)

	with open('/etc/eztv-downloader/shows/' + filename.replace(' ', '') + '.cfg', 'wb') as configfile:
		config.write(configfile)
        eztvLogger.logging.info("TV Show " + sys.argv[1].title() + " added!")
except:
	print "Couldn't find a TV Show with this name!"
	traceback.print_exc(file=sys.stdout)

