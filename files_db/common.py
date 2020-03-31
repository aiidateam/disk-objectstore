import os
CURRENT_FOLDER = db_folder = os.path.realpath(os.path.join(
    os.path.dirname(__file__)))

REPO_FOLDER = os.path.join(CURRENT_FOLDER, 'objects')

LOOSE_FOLDER = os.path.join(REPO_FOLDER, 'loose')
PACK_FOLDER = os.path.join(REPO_FOLDER, 'packs')

DB_FILE = os.path.join(REPO_FOLDER, 'index.sqlite')

PREFIX_LEN = 2 # how many characters for pack size (2 means 'aa', 'ab', 'ac', ...; 3 means 'aaa', 'aab', 'aac', ... etc)