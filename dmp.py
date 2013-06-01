import urllib2
import os

def _get_appdata_path():
    import ctypes
    from ctypes import wintypes, windll
    CSIDL_APPDATA = 26
    _SHGetFolderPath = windll.shell32.SHGetFolderPathW
    _SHGetFolderPath.argtypes = [wintypes.HWND,
                                 ctypes.c_int,
                                 wintypes.HANDLE,
                                 wintypes.DWORD,
                                 wintypes.LPCWSTR]
    path_buf = wintypes.create_unicode_buffer(wintypes.MAX_PATH)
    result = _SHGetFolderPath(0, CSIDL_APPDATA, 0, 0, path_buf)
    return path_buf.value

def dropbox_home():
    from platform import system
    import base64
    import os.path
    _system = system()
    if _system in ('Windows', 'cli'):
        host_db_path = os.path.join(_get_appdata_path(),
                                    'Dropbox',
                                    'host.db')
    elif _system in ('Linux', 'Darwin'):
        host_db_path = os.path.expanduser('~'
                                          '/.dropbox'
                                          '/host.db')
    else:
        raise RuntimeError('Unknown system={}'
                           .format(_system))
    if not os.path.exists(host_db_path):
        raise RuntimeError("Config path={} doesn't exists"
                           .format(p))
    with open(host_db_path, 'r') as f:
        data = f.read().split()
    return base64.b64decode(data[1])

dropbox_folder = os.path.join(dropbox_home(),"Public","dmp")
if not os.path.isdir(dropbox_folder):
    os.makedirs(dropbox_folder)

def send(messagenum, message, dropbox_id):
    ''' Send message with the given message num to the given id '''
    with open(os.path.join(dropbox_folder,"dmp{}".format(dropbox_id)),"wb") as dmpfile:
        dmpfile.write("{}\n{}".format(messagenum,message))
    return True

def receive(receive_dropbox_id,send_dropbox_id):
    while True:
        try:
            data = urllib2.urlopen("https://dl.dropboxusercontent.com/u/{}/dmp/dmp{}".format(send_dropbox_id,receive_dropbox_id)).read()
            messagenum = int(data.split("\n",1)[0])
            message = data.split("\n",1)[1]
            break
        except Exception as e:
            if e == KeyboardInterrupt:
                raise e
    return messagenum, message