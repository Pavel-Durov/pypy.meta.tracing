from curses import noecho
from sys import argv
import dropbox
import os


def dropbox_connect():
    dbx = None
    try:
        dbx = dropbox.Dropbox(token)
    except Exception as e:
        print('Error connecting to Dropbox with access token: ' + str(e))
    return dbx


def upload_file(local_file, remote_file):
    try:
        dbx = dropbox_connect()
        print('connected')
        with open(local_file, "rb") as f:
            f = dbx.files_upload(f.read(), remote_file,
                                 mode=dropbox.files.WriteMode("overwrite"))
        print('DONE uploading {} file to {}'.format(local_file, remote_file))
    except Exception as e:
        print(e)


if __name__ == '__main__':

    token = os.getenv('DROPBOX_ACCESS_TOKEN', None)
    print(token)
    assert token is not None

    local_file = argv[1]
    remote_file = argv[2]
    print('uploading {} file to {}'.format(local_file, remote_file))
    upload_file(local_file, remote_file)
