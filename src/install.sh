#!/bin/bash

if [ ! -d /etc/eztv-downloader/shows ]; then
	mkdir -p /etc/eztv-downloader/shows
fi

if [ ! -e /etc/eztv-downloader/Conf ]; then
    cp Conf /etc/eztv-downloader
fi

cp eztv-checkEpisodes.py /usr/bin/
cp eztv-addTVshow.py /usr/bin
cp eztvLogger.py /usr/bin
