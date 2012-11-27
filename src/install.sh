#!/bin/bash

install -v -d /etc/eztv-downloader

if [ ! -e /etc/eztv-downloader/Conf ]; then
    install -v Conf /etc/eztv-downloader
fi

install -v eztv-checkEpisodes.py /usr/bin/
install -v eztv-addTVshow.py /usr/bin
install -v eztvLogger.py /usr/bin
