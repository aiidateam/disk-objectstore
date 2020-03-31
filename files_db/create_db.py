#!/usr/bin/env python
import os
import sys
import shutil

from common import DB_FILE, REPO_FOLDER, LOOSE_FOLDER, PACK_FOLDER
from models import get_session
 
if __name__ == '__main__':
    try:
        param = sys.argv[1]
        if param == '--clear':
            clear = True
        else:
            print("Only possible option: --clear, to clear the existing DB first", file=sys.stderr)
            sys.exit(1)
    except IndexError:
        clear = False

    if clear:
        if os.path.exists(REPO_FOLDER):
            shutil.rmtree(REPO_FOLDER)
    if not os.path.exists(REPO_FOLDER):
        os.makedirs(REPO_FOLDER)
    get_session(DB_FILE, create=True)
    for folder in [LOOSE_FOLDER, PACK_FOLDER]:
        if not os.path.exists(folder):
            os.makedirs(folder)
