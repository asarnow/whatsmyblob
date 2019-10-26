# Copyright (C) 2018 Daniel Asarnow
# University of California, San Francisco
import mrcfile
import os.path
from whatsmyblob import constants


def handle_upload_mrc(jobid, upload):
    dest = os.path.join(constants.TEMP_ROOT, jobid, "query.mrc")
    with open(dest, 'wb+') as f:
        for c in upload.chunks():
            f.write(c)
    try:
        with mrcfile.open(dest, permissive=True) as f:
            pass
    except:
        return False
    return True

