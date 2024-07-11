#!/usr/bin/python3
# Fabfile that creates and distributes an archive to my web servers,
# using the function deploy


from fabric.api import local
import os
import time
from fabric.api import env
from fabric.api import put
from fabric.api import run

env.hosts = ["100.25.156.92", "52.87.219.72"]


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


def do_deploy(archive_path):
    """Distributes an archive to my web servers.
    Args:
        archive_path: The path of the archive to distribute.
    """
    if os.path.isfile(archive_path) is False:
        return False
    file = archive_path.split("/")[-1]
    file_name = file.split(".")[0]

    if put(archive_path, "/tmp/{}".format(file)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/".
           format(file_name)).failed is True:
        return False
    if run("mkdir -p /data/web_static/releases/{}/".
           format(file_name)).failed is True:
        return False
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".
           format(file, file_name)).failed is True:
        return False
    if run("rm /tmp/{}".format(file)).failed is True:
        return False
    if run("mv /data/web_static/releases/{}/web_static/* "
           "/data/web_static/releases/{}/".
           format(file_name, file_name)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/web_static".
           format(file_name)).failed is True:
        return False
    if run("rm -rf /data/web_static/current").failed is True:
        return False
    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".
           format(file_name)).failed is True:
        return False
    return True


def deploy():
    """Create and distribute an archive to a web server."""
    file = do_pack()
    if file is None:
        return False
    return do_deploy(file)
