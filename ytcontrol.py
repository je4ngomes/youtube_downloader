from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from time import sleep
import urllib.request as re
from urllib.error import HTTPError
import os
from tqdm import tqdm

class TqdmUpTo(tqdm):
    """Provides `update_to(n)` which uses `tqdm.update(delta_n)`."""
    def update_to(self, b=1, bsize=1, tsize=None):
        """
        b  : int, optional
            Number of blocks transferred so far [default: 1].
        bsize  : int, optional
            Size of each block (in tqdm units) [default: 1].
        tsize  : int, optional
            Total size (in tqdm units). If [default: None] remains unchanged.
        """
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)  # will also set self.n = b * bsize




class youtubeDownload:
    
    host = 'http://megavn.com/'

    def __init__(self, url):
        self.browser = webdriver.PhantomJS()
        self.url_video = url

        self.download = {}
    
    def _return_source(self, html_id):
        inputElement = self.browser.find_element_by_id(html_id)
        inputElement.send_keys(self.url_video)
        button = self.browser.find_element_by_id('btndownload')
        button.click()
        sleep(10)
        return self.browser.page_source
      
    
    def content_playlist(self, quality):
        id = {'720p': 'quality3', '360p': 'quality4', '240p': 'quality5'}
        self.browser.get(self.host + 'playlist.php')
        button = self.browser.find_element_by_id(id[quality])
        button.click()

        SoupObj = BeautifulSoup(self._return_source('txtList').__str__(),'html.parser')
        self.browser.quit()

        names = [
            name.text for name in SoupObj.find('table', {'id': 'ListVideo'}).find_all('a') 
            if name.text not in ['720p mp4', '360p mp4', '240p 3gp']
        ]

        video_links = SoupObj.find('table', {'id': 'ListVideo'}).find_all('a', {'class': 'btn'})


        for i, name in enumerate(names, start=1):
            if names.count(name) == 2:
                names.remove(name)
            self.download['video' + str(i)] = {'video': {}}
            self.download['video' + str(i)]['name'] = name+'.mp4'
                
        else:
            del i


        for i,link in enumerate(video_links, start=1):
            if video_links.count(link) == 2:
                video_links.remove(link)              
            self.download['video' + str(i)]['video'][quality] = link.attrs['href']
     

    def content_video(self):
        self.browser.get(self.host)
        SoupObj = BeautifulSoup(self._return_source('txtLink').__str__(), 'html.parser')
        self.browser.quit() # close browser after get source

        self.download['video1'] = {'video': {}}
        self.download['video1']['name'] = SoupObj.find('div', {'id': 'Download_Image'}).find('h5').find('a').text +'.mp4'
        
        video = SoupObj.find('div', {'class': 'panel-primary'}).find_all('a', {'class': 'btn'})
        
        
        for v in video:
            if v.attrs.get('href'):
                self.download['video1']['video'][v.text.split()[0]] = v.attrs['href']
      

    def next_link(self, quality, start=1):
        link_and_name = {}

        for i,k in enumerate(self.download, start=start):
            link_and_name[i] = {}
            link_and_name[i]['name'] = self.download[k]['name']
            link_and_name[i]['link'] = self.download[k]['video'][quality]
        return link_and_name


    def download_files(self, filename, url):       

        try:
            with TqdmUpTo(unit='B',desc=filename, unit_scale=True, miniters=1) as t:  # all optional kwargs
                re.urlretrieve(
                    url,
                    filename=filename,
                    reporthook=t.update_to
                )

            sleep(5)
        except KeyboardInterrupt:
            os.remove(filename)
            print('Download Interrupted')
            exit()
        


