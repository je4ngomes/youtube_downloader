from ytcontrol import youtubeDownload
from sys import argv

doc_help ='''
How to run this program?
    usage: youtubedownloader.py [url]

optional arguments:

    -q This one is optional to add this parameter you use "-q followed by the quality"
    or you can just let it in blank by default de quality will be medium.
      -low
      -medium
      -high
      
      usage: youtubedownloader.py [url] -q low
    
    --channel Download all content of a channel
    
    --playlist Download playlist


'''

if __name__ == '__main__':
    
    yt = youtubeDownload(argv[1])

    if '--help' in argv:
        print(doc_help)

    else:
        if '-q' in argv:
            q = {'low': '240p', 'medium': '360p', 'high': '720p'}
            for i in argv:
                if i in q:
                    quality= q[i]
        else:
            quality = '320p'

        try:
            if '--playlist' in argv or '--channel' in argv:
                yt.content_playlist(quality)
            else:
                yt.content_video()
        except:
            print('Something Goes Wrong! Try Again.')

        for _ in yt.next_link(quality).items():
            yt.download_files(_[1]['name'],_[1]['link'])
        print('Download Finished...')  
            
