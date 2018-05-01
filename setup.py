from urllib.request import urlretrieve, urlopen
import platform
import re as regex
import os

#install dependencies
os.system('sudo pip install -r requeriment.txt')

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


html = str(urlopen('http://phantomjs.org/download.html').read())

def get_links():
    regex.escape(r'.')
    _64bit = regex.search(r'https://bitbucket.org/ariya/phantomjs/downloads/phantomjs[-0-9.]+-linux-x86_64.tar.bz2', html)
    _32bit = regex.search(r'https://bitbucket.org/ariya/phantomjs/downloads/phantomjs[-0-9.]+-linux-i686.tar.bz2', html)
    filename_64bit = regex.search(r'phantomjs[-0-9.]+-linux-x86_64', html)
    filename_32bit = regex.search(r'phantomjs[-0-9.]+-linux-i686', html)

    return {'32bit': _32bit.group(), '64bit': _64bit.group(), 'filename_32bit': filename_32bit.group(), 'filename_64bit': filename_64bit.group()}


def main(arch):
    link_and_filename = get_links()
    filename, url = link_and_filename['filename_{}'.format(arch)], link_and_filename[arch]

    with TqdmUpTo(unit='B',desc='Phantomjs', unit_scale=True, miniters=1) as t:  # all optional kwargs
        urlretrieve(
        url,
        filename='Phantomjs.tar.bz2',
        reporthook=t.update_to
    )
    os.system(
        'tar xvjf Phantomjs.tar.bz2 && '
        'mv {filename} /usr/local/share && sudo ln -sf /usr/local/share/{filename}/bin/phantomjs /usr/local/bin'.format(filename=filename) 
    )

if __name__ == '__main__':
    main(platform.architecture()[0])
