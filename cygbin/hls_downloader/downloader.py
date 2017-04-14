import requests
import os
import boss
import time


def _download(uri, filename):
    '''
    download from uri and save as filename (relative to CWD)
    @param uri
    @param filename
    '''
    resp = requests.get(uri, verify=False)
    with open(filename, 'wb') as f:
        f.write(resp.content)


def download(uri, local, clear_local=False):
    '''
    Download resource from uri, save to local, i.e. path/to/target.file (relative to CWD)

    @param uri Full URI of the target
    @param local path/to/target.file
    '''
    boss.blocking_print('downloading {uri} to {local}'.format(uri=uri, local=local))
    if os.path.exists(local):
        if clear_local:
            os.remove(local)
        else:
            boss.blocking_print('{local} exists'.format(local=local))
            return True

    target_name = os.path.basename(local)
    subfolder = os.path.dirname(local)
    if subfolder and not os.path.exists(subfolder):
        os.makedirs(subfolder)

    _download(uri, target_name)
    try:
        os.rename(target_name, local)
    except WindowsError:
        boss.blocking_print('Error: exception while moving {filename}'.format(filename=target_name))
        return False
    return True


def download_async(uri, local, clear_local=False):
    subfolder = os.path.dirname(local)
    if subfolder and not os.path.exists(subfolder):
        os.makedirs(subfolder)
    command = {
        'uri': uri,
        'local': local,
        'clear_local': False
    }
    task = boss.Task(task_id=uri, command=command)
    boss.dedicate(task)


def _download_task(task):
    '''
    @param task Task instance
    @return True indicating download succeeds, False otherwise
    '''
    return download(task.command['uri'], task.command['local'], task.command['clear_local'])


def start(num_workers=2):
    boss.blocking_print('Start downloader with {i} workers'.format(i=num_workers))
    boss.start(num_workers=num_workers, task_processor=_download_task)


def stop():
    boss.blocking_print('Stop downloader')
    boss.stop()


def join():
    '''
    wait until all download done
    '''
    while not boss.have_all__TASKS_done():
        boss.blocking_print('Waiting for all downloads done')
        time.sleep(1)
    boss.blocking_print('All downloads done')


def main():
    # blocking download
    uri = 'http://devimages.apple.com.edgekey.net/streaming/examples/bipbop_4x3/bipbop_4x3_variant.m3u8'
    local = 'bipbop_4x3/bipbop_4x3_variant.m3u8'

    download(uri=uri, local=local, clear_local=True)

    # async batch download
    start(num_workers=4)

    for i in range(0, 20):
        uri = 'http://devimages.apple.com.edgekey.net/streaming/examples/bipbop_4x3/gear1/fileSequence{i}.ts'.format(i=i)
        local = 'bipbop_4x3/gear1/fileSequence{i}.ts'.format(i=i)
        download_async(uri=uri, local=local, clear_local=True)
    join()
    stop()


if __name__ == '__main__':
    main()
