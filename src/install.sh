#!/bin/bash

if [ ! -d /etc/eztv-downloader/shows ]; then
	mkdir -p /etc/eztv-downloader/shows
fi

cp Conf /etc/eztv-downloader
cp eztv-checkEpisodes.py /usr/bin/
cp eztv-addTVshow.py /usr/bin
cp eztvLogger.py /usr/bin
