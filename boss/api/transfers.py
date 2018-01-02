''' SFTP operations for file uploads and downloads. '''

import os
import sys
from time import time
from tempfile import mkdtemp

from boss.core.fs import compress, size_unit
from boss.core.util.colors import green, cyan
from boss.api.ssh import run, put, normalize_path


class Uploader(object):
    '''
    Uploader
    --------
    A utility class for uploading files and directories easily.
    '''

    # Status constants
    STATUS_PREPARING = 1
    STATUS_COMPRESSING = 2
    STATUS_COMPRESSED = 3
    STATUS_PREPARING_TO_UPLOAD = 4
    STATUS_UPLOADING = 5
    STATUS_UPLOADED = 6
    STATUS_FINALIZING = 7
    STATUS_DONE = 8

    def __init__(self, local_path, callback=None):
        ''' Uploader constructor. '''
        tmp_folder = mkdtemp()
        self.local_path = local_path
        self.name = 'upload-{}.tar.gz'.format(str(time()).replace('.', '-'))
        self.tar_path = os.path.join(tmp_folder, self.name)
        self.remote_tmp_path = '/tmp/' + self.name

        self.callback = callback or default_status_message

    def update(self, status, **params):
        ''' Update status to the stdout. '''
        message = self.callback(status, **params)
        sys.stdout.write(message)
        sys.stdout.flush()

    def upload(self, remote_path):
        ''' Start the upload operation. '''
        self.update(Uploader.STATUS_PREPARING)
        remote_path = normalize_path(remote_path)

        # Compress the directory.
        self.update(Uploader.STATUS_COMPRESSING)
        compress(self.local_path, self.tar_path)

        total_size = os.path.getsize(self.tar_path)
        self.update(Uploader.STATUS_COMPRESSED, total=total_size)

        def put_callback(sent, total):
            self.update(Uploader.STATUS_UPLOADING, sent=sent, total=total)

        # Upload the tar zipped file to the remote.
        # The compressed folder gets uploaded to a temp path first.
        # Then later is extracted to the provided path on the remote.
        self.update(Uploader.STATUS_PREPARING_TO_UPLOAD, total=total_size)
        put(self.tar_path, self.remote_tmp_path, put_callback)

        # Extract the files to the remote directory
        self.update(Uploader.STATUS_FINALIZING)
        run([
            'mkdir -p {}'.format(remote_path),
            'tar zxvf {src} --strip-components=1 -C {dest}'.format(
                src=self.remote_tmp_path,
                dest=remote_path
            )
        ])

        os.remove(self.tar_path)
        self.update(Uploader.STATUS_DONE)


# Default status message map
DEFAULT_MESSAGES = {}
DEFAULT_MESSAGES[Uploader.STATUS_PREPARING] = 'Preparing'
DEFAULT_MESSAGES[Uploader.STATUS_COMPRESSING] = 'Compressing'
DEFAULT_MESSAGES[Uploader.STATUS_COMPRESSED] = 'Compressed'
DEFAULT_MESSAGES[Uploader.STATUS_PREPARING_TO_UPLOAD] = 'Uploading'
DEFAULT_MESSAGES[Uploader.STATUS_UPLOADING] = 'Uploading'
DEFAULT_MESSAGES[Uploader.STATUS_UPLOADED] = 'Uploaded'
DEFAULT_MESSAGES[Uploader.STATUS_FINALIZING] = 'Finalizing'
DEFAULT_MESSAGES[Uploader.STATUS_DONE] = 'Upload Completed'


def default_status_message(status, **params):
    ''' Default status callback function for Uploader. '''
    message = green(DEFAULT_MESSAGES[status])
    blank = '\r' + (' ' * 50) + '\r'  # Blank padding to clear the output line
    result = blank + message

    if status == Uploader.STATUS_PREPARING:
        result = '\n' + result
    elif status == Uploader.STATUS_PREPARING_TO_UPLOAD:
        result = blank + '{} [{}]'.format(
            message,
            cyan(size_unit(params['total']))
        )
    elif status == Uploader.STATUS_UPLOADING:
        sent = params['sent']
        total = params['total']
        progress = (sent * 100.0 / total)
        result = blank + '{} [{}] - {:.2f}%'.format(
            message,
            cyan(size_unit(total)), progress
        )
    elif status == Uploader.STATUS_DONE:
        result += '\n\n'

    return result


def upload_dir(local_path, remote_path, callback=None):
    ''' Upload local directory to the remote. '''
    uploader = Uploader(local_path, callback)

    return uploader.upload(remote_path)
