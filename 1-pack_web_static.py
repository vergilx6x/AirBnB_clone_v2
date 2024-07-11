#!/usr/bin/python3
# Fabfile to generate a .tgz archive from the contents of web_static.

from fabric.api import local, task
import os
import time


def do_pack():
    """Create a tar gzipped archive of the directory web_static."""
    file = "versions/web_static_{}.tgz".format(time.strftime("%Y%m%d%H%M%S"))

    if not os.path.isdir("versions"):
        result = local("mkdir -p versions")
        if result.failed:
            print("Failed to create 'versions' directory.")
            return None

    result = local("tar -cvzf {} web_static".format(file))
    if result.failed:
        print("Failed to create tar archive.")
        return None

    print("Tar archive created successfully: {}".format(file))
    return file
