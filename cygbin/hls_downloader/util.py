import os
from urlparse import urlparse


def chdir(path):
    if not os.path.exists(path):
        os.makedirs(path)
    old_cwd = os.getcwd()
    os.chdir(path)
    print('current working directory: {cwd}'.format(cwd=path))
    return old_cwd


def is_full_uri(uri):
    return uri.startswith('http://') or uri.startswith('https://')


def parse_uri(uri):
    '''
    parse URI into host_root, subpath, filename

    e.g. http://example.com/path/to/stream_id/index.m3u8
        host_root = http://example.com
        subpath = path/to/stream_id
        filename = index.m3u8

    @param uri
    @return host_root, subpath, filename
    '''
    print('parsing {uri}'.format(uri=uri))
    url = urlparse(uri)
    host_root = url.scheme + '://' + url.netloc
    subpath = os.path.dirname(url.path)[1:]
    filename = os.path.basename(url.path)

    return host_root, subpath, filename


def check(path):
    count_01, count_02, count_03 = 0, 0, 0
    for root, dirs, files in os.walk(path):
        for f in files:
            if '-01-' in f:
                count_01 += 1
            if '-02-' in f:
                count_02 += 1
            if '-03-' in f:
                count_03 += 1
    print(count_01, count_02, count_03)
    pass


def main():
    check('C:\Users\zou\Github\hls_downloader\channelgroup5\channelgroup5\cg543production\ch332')

if __name__ == '__main__':
    main()
