from subprocess import run, CalledProcessError, TimeoutExpired
from sys import platform, version as pyver, exit, executable
from ssl import create_default_context, CERT_NONE
from urllib.error import URLError, HTTPError
from importlib import import_module
from os import mkdir, remove, rmdir
from time import perf_counter, time
from urllib.request import urlopen
from os.path import abspath
from zipfile import ZipFile
from shutil import move
from json import loads


pname:         str = 'test'
ctx                = create_default_context()
ctx.check_hostname = False
ctx.verify_mode    = CERT_NONE
ctx.                 set_ciphers('RSA')

def _exit(code: int, details: str):
    print(details)
    exit(code)

def get(url: str) -> bytes:  
    try:
        return urlopen(url, timeout=10, context=ctx).read()
    except (URLError, HTTPError) as err:
        if '[Errno 8]' in str(err):
            _exit(1, 'Please check your internet connection')
        else:
            _exit(1, 'Unspecified urlopen error')

def call(cmd: str) -> int:
    try:
        return run(cmd, shell=True).returncode
    except (CalledProcessError, TimeoutExpired):
        return 1

if __name__ != '__main__':
    _exit(1, '')

try:
    ipath:   str = input(' Installation path (Press enter to skip): ')
    itype:   str = input(' What type would you like? (cli/gui): ').upper()
    s1:    float = perf_counter()
    vdata:  dict = loads(get('https://api.github.com/repos/' +
                         f'feetbots/{pname}/releases?per_page=100').decode())
    getv:  float = round(perf_counter() - s1, 3)
    start: float = perf_counter()
    version: str = [i['tag_name'].split('-')[0] for i in vdata][0]
    pyv:    list = pyver.split(' ', 1)[0].split('.')[:2]

    print('\n')
    if platform != 'darwin':
        _exit(1, 'You need MacOS to install EzMusic!')
    elif int(pyv[0]) == 3 and int(pyv[1]) < 9:
        _exit(1, 'You need python 3.9 or above \nYou currently have version {0}'.format('.'.join(pyv)))
    elif ipath != '':
        if ipath[-1] != '/':
            ipath += '/ezmusic/'
        else:
            ipath += 'ezmusic/'
    elif ipath == '':
        ipath = abspath('./') + '/ezmusic/'
    elif itype not in ['CLI', 'GUI']:
        _exit(1, 'Invalid installation type')

    packages: list = [
        'Cython==0.29.33', 'kivy==2.1.0',
        'pyobjc==9.0.1', 'pyperclip==1.8.2',
        'pytube==12.1.2', 'tooltils==1.4.0'
    ]
    with open('requirements.txt', 'a+') as _f:
        _f.writelines(packages)

    opts: str = '--upgrade --trusted-host pypi.org --trusted-host ' + \
                'pypi.python.org --trusted-host files.pythonhosted.org'
    call(f'{executable} -m pip install -r requirements.txt {opts}')
    try:
        import_module('pytube')
        remove('requirements.txt')
    except ModuleNotFoundError:
        _exit(1, 'Please install requirements.txt manually')

    data: bytes = get(f'https://github.com/feetbots/{pname}/archive/refs/tags/{version}.zip')

    with open(ipath + 'files.zip', 'wb+') as _f:
        _f.write(data)
    with ZipFile(ipath + 'files.zip') as _f:
        _f.extractall(ipath)
        
    for i in ['files.zip', 'requirements.txt']:
        remove(ipath + i)

    mkdir(ipath + 'cache/')
    mkdir(ipath + 'songs/')
    if itype == 'cli':
        remove(ipath + 'bin/gui.py')
        remove(ipath + 'tools/gui.py')
    else:
        remove(ipath + 'bin/cli.py')

    with open(ipath + 'storage/config.json', 'a+') as _f:
        json: str = '{\n' + \
                    '  "installed": ' + str(time()) + ',\n' + \
                    '  "autoUpdate": true,\n' + \
                    '  "version": "' + version[1:] + '",\n' + \
                    '  "type": ' + itype + ',\n' + \
                    '  "inputMode: True,\n' + \
                    '  "darkMode: True\n' + \
                    '}'
        _f.write(json)

    code: int = call('mkdir ~/usr/local')
    if code == 0 or code == 1:
        for i in ['ba', 'z', '']:
            call(f'echo "export PATH=$PATH:{ipath}bin/{itype.lower()}.py:~/usr/local/bin" >> ~/.{i}shrc')
    else:
        rmdir(ipath)
        _exit(1, 'An error occured while adding the launcher to PATH')

    print('Installation finished',
          ' - Located in {}'.format(ipath[:-8]),
          ' - Version: {}'.format(version[1:]),
          ' - Took {}s'.format(round(perf_counter() - start + getv, 3)),
          sep='\n')

except (KeyboardInterrupt, EOFError):
    rmdir(ipath)
    _exit(1, '')
