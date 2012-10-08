#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib, re, ConfigParser, sys, os, traceback, eztvLogger

Conf = ConfigParser.RawConfigParser()
Conf.read("/etc/eztv-downloader/Conf")



def download(url):
    file_name = url.split('/')[-1]
    u = urllib.urlopen(url)
    f = open(Conf.get('Download', 'folder') + file_name, 'wb')
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
        print status,

    f.close()

for cfg in os.listdir("/etc/eztv-downloader/shows/"):
    if cfg.endswith(".cfg"):
        config = ConfigParser.RawConfigParser()
        config.read("/etc/eztv-downloader/shows/" + cfg)

        episodio_local=[config.getint('Serie', 'Season'), config.getint('Serie', 'Episode')]
        episodios_novos = []

        try:
            params = {"SearchString": config.getint('Serie', 'id')}
            query = urllib.urlencode(params)
            url = "http://eztv.it/search/"

            serie = urllib.urlopen(url, query)
            episodios = serie.read()
            serie.close()

            arquivos = re.findall("http.+[sS]\d{2}[eE]\d{2}.+[.]torrent", episodios)

            for arquivo in arquivos[::-1]:
#		print arquivo
                episodio = [int(re.search('([sS]\d{2}[eE]\d{2})', arquivo).group(0).upper().split('E')[0].split('S')[1]), int(re.search('([sS]\d{2}[eE]\d{2})', arquivo).group(0).upper().split('E')[1])]
#		print str(episodio_local) + " " + str(episodio)
                if episodio_local >= episodio:
                    pass
                else:
		    for word in arquivo.split():
		        if word.endswith('.torrent"'):
			    word = word.split("\"")
			    word = word[len(word)-2].split()[0]
#			    print "FIM " + str(word)
			    episodios_novos.append(word)
			    break
			elif word.endswith('.torrent'):
			    word = word.split("\"")[1]
#			    print "WAGNER " + str(word)
			    episodios_novos.append(word)
			    break
#                    episodios_novos.append([ word for word in arquivo.split() if word.endswith('.torrent"') ][0].split("\"")[0])
		    episodio_local = episodio
  
            if len(episodios_novos) > 0:
                series_logger.logging.info(str(len(episodios_novos)) + " novos episódios em " + cfg.replace(".cfg", ""))
                for episodio_novo in episodios_novos:
                    download(str(episodio_novo))
                config.set('Serie', 'Season', int(re.search('([sS]\d{2}[eE]\d{2})', episodios_novos[len(episodios_novos)-1]).group(0).upper().split('E')[0].split('S')[1]))
                config.set('Serie', 'Episode', int(re.search('([sS]\d{2}[eE]\d{2})', episodios_novos[len(episodios_novos)-1]).group(0).upper().split('E')[1]))
                with open("/etc/eztv-downloader/" + cfg, 'wb') as configfile:
                    config.write(configfile)

            else:
                eztvLogger.logging.info("Nenhum episódio novo em " + cfg.replace(".cfg", ""))
	except:
	    print "Erro!"
	    traceback.print_exc(file=sys.stdout)

