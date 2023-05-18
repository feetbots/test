from urllib.request import urlopen
from urllib.error import URLError
from shutil import rmtree
from os import mkdir

from pytube.exceptions import RegexMatchError
from tooltils.requests import _ctx
from tooltils.sys import call
from pytube import YouTube

from .app import throw


def cstrip(text: str, chars: str) -> str:
    for i in chars:
        text = text.replace(i)
    
    return text

class song:
    def download(url: str) -> None:
        try:
            st = url.startswith 
            if not st('https://') and not st('http://'):
                url = 'https://' + url
            elif 'youtube.com/watch?v=' not in url:
                return throw('Invalid url')

            vid        = YouTube(url)
            name:  str = cstrip(vid.title, '\'|\$"}{')
            fname: str = 'storage/songs/' + name + '/song.mp4'
            try:
                mkdir('storage/songs/' + name)
            except FileExistsError:
                return throw('Song already downloaded')

            vid.streams.get_lowest_resolution().download(filename=fname)
            
            cmd: str = 'afconvert -f WAVE -d LEI32 "{}" -o "{}"'.format(
                       fname, fname.split('.')[:-1] + '.wav')
            if call(cmd, shell=True) != 0:
                if call(cmd, shell=True) != 0:
                    return throw('Error while converting youtube video')

        except (RegexMatchError, URLError, KeyboardInterrupt) as err:
            if type(err) is RegexMatchError:
                return throw('Invalid youtube video ID: {}'.format(
                             url.split('?v=')[1]))
            elif type(err) is URLError:
                if '[Errno 8]' in str(err):
                    try:
                        urlopen('https://google.com', timeout=5, context=_ctx(False, None))
                        return throw('Unspecified YouTube error')
                    except URLError as err:
                        if '[Errno 8]' in str(err):
                            return throw('Internet connection not found')
                        else:
                            return throw('Unspecified YouTube error')
                elif 'ssl' in str(err):
                    return throw('Unable to download songs on this network')
            else:
                try:
                    rmtree('storage/songs/' + fname, ignore_errors=True)
                except (FileNotFoundError, NameError):
                    pass

    def remove(song: str) -> None:
        ...
