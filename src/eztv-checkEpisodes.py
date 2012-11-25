#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib, re, ConfigParser, sys, os, traceback, eztvLogger, lxml.html

Conf = ConfigParser.RawConfigParser()
Conf.read("/etc/eztv-downloader/Conf")

def download(url):
    file_name = url.split('/')[-1]
    u = urllib.urlopen(url)
    f = open(Conf.get('Download', 'folder') + "/" + file_name, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    eztvLogger.logging.info("Downloading: %s Bytes: %s" % (file_name, file_size))

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8)*(len(status)+1)
        #print status,
#        eztvLogger.logging.info(status),

    f.close()


def getEpisode():
    try:    
        for cfg in os.listdir("/etc/eztv-downloader/shows/"):
            if cfg.endswith(".cfg"):
                config = ConfigParser.RawConfigParser()
                config.read("/etc/eztv-downloader/shows/" + cfg)
                
                if config.has_option('Serie', 'Quality'):
                    serie_quality = config.get('Serie', 'Quality')
                else:
                    serie_quality = 'undefined'

        	episodio_local=[config.getint('Serie', 'Season'), config.getint('Serie', 'Episode')]
        	episodios_novos = []

                params = {"SearchString": config.getint('Serie', 'id')}
                query = urllib.urlencode(params)
                url = "http://eztv.it/search/"

                serie = urllib.urlopen(url, query)
                episodios = serie.read()
                serie.close()

	        doc = lxml.html.fromstring(episodios)
	        links = doc.xpath('//a/@href')
	    
  	        torrents = []
                for link in links:
		    if link.endswith(".torrent"):
			torrents.append(re.findall(r'(.*(?:s|season|\.|_)(\d{1,2})(?:e|x|episode)(\d{1,2}).*)', link, re.I))
		

                episodios_processados = []
		
                for torrent in torrents:
                    if (len(torrent)==0):
                        pass
                    else:
                        if serie_quality == '720p' and not re.search('720p', torrent[0][0], re.I):
                            continue
                        if serie_quality == 'hdtv' and re.search('720p', torrent[0][0], re.I):
                            continue

		        episodio = [int(torrent[0][1]), int(torrent[0][2])]
                        if episodio_local >= episodio or episodios_processados.__contains__(episodio):
                            pass
                        else:
                	    episodios_novos.append(torrent[0][0])
		            episodios_processados.append(episodio)
  
                if len(episodios_novos) > 0:
                    eztvLogger.logging.info(str(len(episodios_novos)) + " new episodes from " + cfg.replace(".cfg", ""))
                    for episodio_novo in episodios_novos:
                        download(str(episodio_novo))
  		    ultimo = re.split('E|X', re.search('(\d+[eExX]\d+)', episodios_novos[0]).group(0).upper())
                    config.set('Serie', 'Season', int(ultimo[0]))
                    config.set('Serie', 'Episode', int(ultimo[1]))
                    with open("/etc/eztv-downloader/shows/" + cfg, 'wb') as configfile:
                        config.write(configfile)

                else:
                    eztvLogger.logging.debug("No new episodes from " + cfg.replace(".cfg", ""))
    except:
        print "Error!"
	traceback.print_exc(file=sys.stdout)

getEpisode()
