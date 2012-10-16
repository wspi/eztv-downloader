eztv-downloader
===============

Download new torrents files of your favorite TV Show from eztv.it

You need to have installed python-lxml

apt-get install python-lxml or yum install python-lxml

run install.sh as root

First Configure /etc/eztv-downloader/Conf where it's your download folder and where you want it to log
Remember to give permission to write in the log file to the user that will run the eztv-checkEpisodes.py

Add your favorite TV Shows with the eztv-addTVshow.py script "tv show name" Last_Season Last_Episode

example: Imagine you are watching The Big Bang Theory, and the last episode you have it's from Season 5, Episode 3
eztv-addTVshow.py "the big bang theory" 5 3

later just add /usr/bin/eztv-checkEpisodes.py script to the cron and have fun


