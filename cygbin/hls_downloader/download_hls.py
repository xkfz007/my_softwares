import m3u8
import os
import argparse
import downloader
import util
import time


def download_master_playlist(master_playlist_uri):
    '''
    @param master_playlist_uri Full URI of master playlist
    '''
    host, subpath, filename = util.parse_uri(master_playlist_uri)
    downloader.download(master_playlist_uri, filename, clear_local=True)  # always refresh playlist - so the script can be used for parsing live streams
    print('loading {master_playlist_uri}'.format(master_playlist_uri=master_playlist_uri))
    with open(filename, 'r') as f:
        content = f.read()
    master_playlist = m3u8.loads(content)
    return master_playlist


def download_stream(uri, subpath=None):
    '''
    @param uri
    @param subpath Relative subpath, if None, use uri's subpath
    '''
    stream_playlist_host, stream_playlist_subpath, stream_playlist_filename = util.parse_uri(uri)
    local_stream_playlist_filename = os.path.join(stream_playlist_subpath, stream_playlist_filename)
    if subpath:
        local_stream_playlist_filename = os.path.join(subpath, stream_playlist_filename)
    downloader.download(uri, local_stream_playlist_filename, clear_local=True)   # always refresh playlist - so the script can be used for parsing live streams

    print('loading {local}'.format(local=local_stream_playlist_filename))
    with open(local_stream_playlist_filename, 'r') as f:
        content = f.read()
    stream_playlist = m3u8.loads(content)
    print('{num_segments} segments to download in {stream_playlist}'.format(num_segments=len(stream_playlist.segments), stream_playlist=uri))
    for segment in stream_playlist.segments:
        print('to download {url}'.format(url=segment.uri))
        if segment.uri.startswith('#'):
            continue
        if util.is_full_uri(segment.uri):
            segment_host, segment_subpath, segment_filename = util.parse_uri(segment.uri)
            downloader.download_async(segment.uri, os.path.join(segment_subpath, segment_filename))
        else:
            segment_uri = stream_playlist_host + '/' + stream_playlist_subpath + '/' + segment.uri
            downloader.download_async(segment_uri, os.path.join(subpath, segment.uri))
        if segment.byterange:
            break


def download_hls_stream(master_playlist_uri, id='.', num_workers=10, refreash_interval=0, num_refreshes=1):
    '''
    Download hls stream to local folder indiciated by id
    @param master_playlist_uri
    @param id Defaut CWD
    @param num_workers Number of downloader workers
    @param refresh_interval unit: second, Default 0
    @param num_refreshes Default 1
    '''
    print('master_playlist_uri: {master_playlist_uri}'.format(master_playlist_uri=master_playlist_uri))
    local_root = id

    print('downloading {uri} to {local}'.format(uri=master_playlist_uri, local=local_root))
    old_cwd = util.chdir(local_root)

    downloader.start(num_workers)

    for r in range(0, num_refreshes):
        master_playlist = download_master_playlist(master_playlist_uri)

        if master_playlist.is_variant:
            host_root, subpath, master_playlist_file = util.parse_uri(master_playlist_uri)
            # download resource from stream playlist
            for playlist in master_playlist.playlists:
                if util.is_full_uri(playlist.uri):
                    download_stream(playlist.uri)
                    pass
                else:
                    playlist_uri = host_root + '/' + subpath + '/' + playlist.uri
                    download_stream(playlist_uri, os.path.dirname(playlist.uri))

            # download resource from media
            for m in master_playlist.media:
                if not m.uri:
                    continue
                if util.is_full_uri(m.uri):
                    download_stream(m.uri)
                    pass
                else:
                    media_uri = host_root + '/' + subpath + '/' + m.uri
                    download_stream(media_uri, os.path.dirname(m.uri))
        else:
            download_stream(master_playlist_uri)

        if refreash_interval:
            print('Refreshing the master playlist in {interval} seconds'.format(interval=refreash_interval))

        time.sleep(refreash_interval)

    downloader.join()
    downloader.stop()
    os.chdir(old_cwd)


def main():
    parser = argparse.ArgumentParser(description='Download HLS streams -- default to download Apple reference HLS streams')
    parser.add_argument('--stream', help='master playlist URI, m3u8 resource')
    parser.add_argument('--id', help='stream id. Used a subfolder name for the downloads')
    parser.add_argument('--workers', default=10, type=int, help='Number of download workers')
    parser.add_argument('--refresh_interval', default=0, type=int, help='Interval (second) of refreshing the master playlist, for downloading LIVE resources')
    parser.add_argument('--num_refreshes', default=1, type=int, help='Number of refreshing the master playlist, for downloading LIVE resources')
    args = parser.parse_args()

    if args.stream:
        download_hls_stream(args.stream, args.id, args.workers, args.refresh_interval, args.num_refreshes)
    else:  # default tasks
        download_hls_stream('http://devimages.apple.com.edgekey.net/streaming/examples/bipbop_4x3/bipbop_4x3_variant.m3u8', 'bipbop_4x3')
        # download_hls_stream('http://devimages.apple.com.edgekey.net/streaming/examples/bipbop_16x9/bipbop_16x9_variant.m3u8', 'bipbop_16x9')
        # download_hls_stream('http://tungsten.aaplimg.com/VOD/bipbop_adv_example_v2/master.m3u8', 'bipbop_adv_example_v2')
        # download_hls_stream('http://cwm-sp-lab3.hq.k.grp/live/hls/clear/bbc1clear/index.m3u8', 'bbc1')


if __name__ == '__main__':
    main()
