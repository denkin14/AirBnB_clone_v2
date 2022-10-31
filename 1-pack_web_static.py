#!/usr/bin/python3
""" Fabric script for generating compressed tar file
"""

from datetime import datetime
from fabric.api import local, lcd, settings


def do_pack():
    """creates compressed archive file of web_static folder
    """
    # essential variables for file name
    file_name = 'web_static_{}.tgz'.format(
            datetime.now().strftime('%Y%m%d%H%M%S'))

    # create directory if it doesn't exist
    with settings(warn_only=True):
        if local('test -d versions').failed:
            local('mkdir versions')

    # create compressed tar file in the versions directory
    with lcd('versions'):
        execute = local('tar -zcvf {} ../web_static'.format(file_name))

    if execute.succeeded:
        return 'versions/{}'.format(file_name)
