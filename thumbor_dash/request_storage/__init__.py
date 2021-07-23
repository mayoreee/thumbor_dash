from os.path import expanduser,  join
home = expanduser("~")

REQUEST_STORAGE_ROOT_PATH = join(home, 'thumbor', 'request_storage')
