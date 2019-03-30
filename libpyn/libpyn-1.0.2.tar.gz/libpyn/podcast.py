import os
import logging
import requests
from time import sleep
from bs4 import BeautifulSoup as bs

# Set Logger
log = logging.getLogger('libpyn')
log.setLevel(logging.WARNING)
handlerpath = os.path.dirname(os.path.realpath(__file__)) + '/podcast.log'
handler = logging.FileHandler(handlerpath)
handler.setLevel(logging.DEBUG)
consoleHandler = logging.StreamHandler()
formatter = logging.Formatter('Libpyn: [%(levelname)s] %(message)s')
handler.setFormatter(formatter)
consoleHandler.setFormatter(formatter)
log.addHandler(consoleHandler)
log.addHandler(handler)
log.info('Running file libpyn.podcast.py:')



class Podcast:


    def __init__(self, link):

        self.mp3list = []   # List of podcasts from channel
        self.dir = os.path.dirname(os.path.realpath(__file__))
        self.headers = {'user-agent': 'libpyn/1.0.0'}

        # Get Links
        log.debug('Parsing link: %s' % link)
        if not '/rss' in link:
            self.rsslink = link + '/rss'
            self.htmllink = link
        if '/rss' in link:
            self.rsslink = link
            self.htmllink = link[:-4]

        # Parse links
        try:
            log.info('Parsing RSS feed...')
            xml = requests.get(self.rsslink, headers=self.headers).text
            self.xmlsoup = bs(xml, "lxml")
            log.info('Parsing XML feed...')
            html = requests.get(self.htmllink, headers=self.headers).text
            self.htmlsoup = bs(html, "lxml")
        except:
            log.exception('Link is not valid.')

        # Get RSS data
        self.name = self.xmlsoup.find('title').text
        log.debug('Podcast title: %s' % self.name)
        for item in self.xmlsoup.findAll('item'):
            self.mp3list.append(self.getRSSItem(item))
        return


    # Get data from each podcast on an RSS channel
    def getRSSItem(self, item):

        try:
            podcast = {}    # Dictionary for storing podcast info
            podcast['title'] = item.find('title').text
            podcast['date'] = item.find('pubdate').text
            podcast['mp3'] = item.find('enclosure')['url']
            podcast['image'] = item.find('itunes:image')['href']

        except Exception:
            log.exception('Could not parse item.')
        return podcast

    # Get HTML iframes of latest episodes
    def iframes(self):

        iframes = {}

        for item in self.htmlsoup.findAll('iframe'):
            title = item['title']
            item = str(item).split('src="')
            item = str(item[0] + 'src="https:' + item[1])
            iframes[title] = item
        return iframes


    # Download mp3 file(s)
    def download(self, path=None, foldername=None):

        if path:
            try:
                os.chdir(path)
            except:
                log.exception('Could not find directory at: %s ...' % path)

        # Find Downloads folder, make one if it doesn't exist
        else:
            home = os.path.expanduser('~')
            try:
                os.chdir(home + '/Downloads')
            except:
                log.warning('Could not find Downloads folder. Creating...')
                os.mkdir('%s/Downloads/' % home)
                os.chdir('%s/Downloads/' % home)

        # Create foldername if none was passed
        if not foldername:
            foldername = self.name.replace(' ', '_')

        # Create directory if it doesn't exist
        if not foldername in os.listdir():
            os.mkdir(foldername)

        os.chdir('%s/%s' % (os.getcwd(), foldername))
        log.info('Storing mp3 files in %s' % str(os.getcwd()))

        # Get into podcast directory, keep note of previously saved files
        try:
            filelist = []   # List of downloaded mp3 files
            for podcast in os.listdir():
                file = podcast.replace(' ', '_')[:-4]
                log.info('%s found locally, will not be downloaded...' % file)
                filelist.append(file)

        # Create foldername directory if it doesn't exist
        except:
            log.warning('/%s/ doesn\'t exist. Creating...')
            os.mkdir('./%s/' % foldername)
            os.chdir('./%s/' % foldername)

        # Download files
        for podcast in self.mp3list:
            exists = False      # Flag for if file already exists

            # Ensure podcasts aren't redownloaded if directory not empty
            for file in filelist:
                if podcast['title'].replace(' ', '_').replace('/', '_') == file:
                    exists = True
                    log.warning('%s already exists. Skipping...' % file)
                if exists == True:
                    break

            # Download file
            if exists  == False:
                sleep(1)    # Ensure no IP ban
                filename = podcast['title'].replace(' ', '_').replace('/', '_') + '.mp3'
                file = requests.get(podcast['mp3'], headers=self.headers)
                log.info('Downloading %s...' % podcast['title'])
                with open(filename, 'wb') as f:
                    f.write(file.content)
        return
