# hls_downloader
Download whole HLS resources

usage: download_hls.py [-h] [--stream STREAM] [--id ID] [--workers WORKERS]

                       [--refresh_interval REFRESH_INTERVAL]

                       [--num_refreshes NUM_REFRESHES]

Download HLS streams -- default to download Apple reference HLS streams

optional arguments:

  -h, --help            show this help message and exit

  --stream STREAM       master playlist URI, m3u8 resource

  --id ID               stream id. Used a subfolder name for the downloads

  --workers WORKERS     Number of download workers

  --refresh_interval REFRESH_INTERVAL

                        Interval (second) of refreshing the master playlist,

                        for downloading LIVE resources

  --num_refreshes NUM_REFRESHES

                        Number of refreshing the master playlist, for

                        downloading LIVE resources
