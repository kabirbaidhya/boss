''' SFTP operations for file uploads and downloads. '''

import os
import sys
from time import time
from shutil import copy, copytree
from tempfile import mkdtemp

from boss.core.fs import compress, size_unit
from boss.core.util.colors import green, cyan
from boss.api.ssh import run, put, normalize_path
from boss.core.constants.upload_status import (
    PREPARING, COMPRESSING, COMPRESSED,
    PREPARING_TO_UPLOAD, UPLOADING, UPLOADED,
    FINALIZING, DONE
)

# Default status message map
DEFAULT_MESSAGES = {}
DEFAULT_MESSAGES[PREPARING] = 'Preparing'
DEFAULT_MESSAGES[COMPRESSING] = 'Compressing'
DEFAULT_MESSAGES[COMPRESSED] = 'Compressed'
DEFAULT_MESSAGES[PREPARING_TO_UPLOAD] = 'Uploading'
DEFAULT_MESSAGES[UPLOADING] = 'Uploading'
DEFAULT_MESSAGES[UPLOADED] = 'Uploaded'
DEFAULT_MESSAGES[FINALIZING] = 'Finalizing'
DEFAULT_MESSAGES[DONE] = 'Upload Completed'


class Uploader(object):
    ''' Abstract base uploader class. '''

    def __init__(self, callback=None):
        ''' Uploader constructor. '''
        self.callback = callback or default_status_message

    def update(self, status, **params):
        ''' Update status to the stdout. '''
        message = self.callback(status, **params)
        sys.stdout.write(message)
        sys.stdout.flush()


class DirectoryUploader(Uploader):
    '''
    DirectoryUploader
    A utility class for uploading files and directories easily.
    '''

    def __init__(self, local_path, callback=None):
        ''' DirectoryUploader constructor. '''
        Uploader.__init__(self, callback)

        self.local_path = local_path
        self.tar_path = os.path.join(mkdtemp(), 'upload.tar.gz')
        self.remote_tmp_path = tmp_path()

    def upload(self, remote_path):
        ''' Start the upload operation. '''
        self.update(PREPARING)
        remote_path = normalize_path(remote_path)

        # Compress the directory.
        self.update(COMPRESSING)
        compress(self.local_path, self.tar_path)

        total_size = os.path.getsize(self.tar_path)
        self.update(COMPRESSED, total=total_size)

        def put_callback(sent, total):
            self.update(UPLOADING, sent=sent, total=total)

        # Upload the tar zipped file to the remote.
        # The compressed folder gets uploaded to a temp path first.
        # Then later is extracted to the provided path on the remote.
        self.update(PREPARING_TO_UPLOAD, total=total_size)
        put(self.tar_path, self.remote_tmp_path, put_callback)

        # Extract the files to the remote directory
        self.update(FINALIZING)
        run([
            'mkdir -p {}'.format(remote_path),
            'tar zxvf {src} --strip-components=1 -C {dest}'.format(
                src=self.remote_tmp_path,
                dest=remote_path
            )
        ])

        os.remove(self.tar_path)
        self.update(DONE)


class FileUploader(Uploader):
    '''
    FileUploader
    A utility class for uploading a single file.
    '''

    def __init__(self, path, callback=None):
        ''' FileUploader constructor. '''
        Uploader.__init__(self, callback)

        self.path = os.path.abspath(path)
        self.filename = os.path.basename(path)
        self.remote_tmp_path = '/tmp/' + self.filename

    def upload(self, remote_path):
        ''' Start the upload operation. '''
        self.update(PREPARING)
        remote_path = normalize_path(remote_path)
        total_size = os.path.getsize(self.path)

        def put_callback(sent, total):
            self.update(UPLOADING, sent=sent, total=total)

        # Upload the file to a tmp path.
        self.update(PREPARING_TO_UPLOAD, total=total_size)
        put(self.path, self.remote_tmp_path, put_callback)

        self.update(FINALIZING)
        # Move the uploaded file to the remote_path.
        run('mv {} {}'.format(self.remote_tmp_path, remote_path))

        self.update(DONE)


def default_status_message(status, **params):
    ''' Default status callback function for DirectoryUploader. '''
    message = green(DEFAULT_MESSAGES[status])
    blank = '\r' + (' ' * 50) + '\r'  # Blank padding to clear the output line
    result = blank + message

    if status == PREPARING:
        result = '\n' + result

    elif status == PREPARING_TO_UPLOAD:
        result = blank + '{} [{}]'.format(
            message,
            cyan(size_unit(params['total']))
        )

    elif status == UPLOADING:
        sent = params['sent']
        total = params['total']
        progress = (sent * 100.0 / total)
        result = blank + '{} [{}] - {:.2f}%'.format(
            message,
            cyan(size_unit(total)),
            progress
        )

    elif status == DONE:
        result += '\n\n'

    return result


class BulkUploader(Uploader):
    '''
    BulkUploader
    A utility class for uploading multiple files and directories in bulk easily.
    '''

    def __init__(self, callback=None):
        ''' BulkUploader constructor. '''
        Uploader.__init__(self, callback)

        self.bundle_path = mkdtemp()
        # self.name = 'upload-{}.tar.gz'.format(tmp_path())
        self.tar_path = os.path.join(mkdtemp(), str(time()).replace('.', ''))
        self.paths = []

    def add(self, local_path, remote_path):
        ''' Add a path (file or directory) to be uploaded to the remote end. '''
        self.paths.append((local_path, remote_path))

    def prepare_bundle(self):
        ''' Prepare the bundle of files to be uploaded. '''
        paths = []

        # Copy each of the files to be uploaded in a temporary directory
        for (local_path, remote_path) in self.paths:
            filename = os.path.basename(local_path)
            dest = os.path.join(self.bundle_path, filename)

            if os.path.isdir(local_path):
                copytree(local_path, dest)
            else:
                copy(local_path, dest)

            paths.append(
                (os.path.basename(local_path), normalize_path(remote_path))
            )

        self.paths = paths

    def upload(self):
        ''' Start the upload operation. '''
        remote_upload_path = tmp_path()
        remote_extract_path = tmp_path()

        if not self.paths:
            raise RuntimeError('No files to be uploaded.')

        self.update(PREPARING)
        self.prepare_bundle()

        # Compress the files to be uploaded.
        self.update(COMPRESSING)
        compress(self.bundle_path, self.tar_path)

        total_size = os.path.getsize(self.tar_path)
        self.update(COMPRESSED, total=total_size)

        def put_callback(sent, total):
            self.update(UPLOADING, sent=sent, total=total)

        # Upload the tar zipped file to the remote.
        # The compressed folder gets uploaded to a temp path first.
        # Then later is extracted to the provided path on the remote.
        self.update(PREPARING_TO_UPLOAD, total=total_size)
        put(self.tar_path, remote_upload_path, put_callback)

        # Extract the files to the remote directory
        self.update(FINALIZING)

        moves = []
        for (filename, destination) in self.paths:
            src = os.path.join(remote_extract_path, filename)
            moves.append('mv {} {}'.format(src, destination))

        run([
            'tar zxvf {src} --strip-components=1 -C {dest}'.format(
                src=remote_upload_path,
                dest=remote_extract_path
            ),
            'rm {}'.format(remote_upload_path)
        ] + moves)

        os.remove(self.tar_path)
        self.update(DONE)


def tmp_path():
    ''' Get a temp path. '''
    return '/tmp/' + str(time()).replace('.', '')


def upload(local_path, remote_path, callback=None):
    ''' Upload a local file to the remote. '''
    uploader = FileUploader(local_path, callback)

    return uploader.upload(remote_path)


def upload_dir(local_path, remote_path, callback=None):
    ''' Upload local directory to the remote. '''
    uploader = DirectoryUploader(local_path, callback)

    return uploader.upload(remote_path)
