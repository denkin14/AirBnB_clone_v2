i#!/usr/bin/python3
"""This Fabric script deploys to remote servers
"""
from fabric.api import cd, env, run, put, with_settings
from os import path

env.hosts = ["44.200.168.223", "18.204.14.103"]


@with_settings(warn_only=True)
def do_deploy(archive_path):
    """ Function to distribute archive files to webservers
    """
    # essential file names
    file_name = archive_path.split('/')[-1]
    extract_folder = file_name.replace('.tgz', "")
    destination = '/data/web_static/releases/'
    full_path = '{}/{}'.format(destination, extract_folder)
    link = "/data/web_static/current"

    # check if archive file exists
    if not path.isfile(archive_path):
        return False

    # transfer file to remote
    if put(archive_path, "/tmp/").failed:
        return False

    # change directory and extract file
    with cd(destination):
        if run('mkdir {}'.format(extract_folder)).failed:
            return False
    with cd(full_path):
        if run('tar -xzvf /tmp/{}'.format(file_name)).failed:
            return False
        # mv files and delete folder
        if run('mv web_static/* .').failed:
            return False
        if run('rm -rf web_static').failed:
            return False

    # rm  archive file
    if run('rm -rf /tmp/{}'.format(file_name)).failed:
        return False

    # create new symbolic link
    if run('ln -sfn {} {}'.format(full_path, link)).failed:
        return False

    return True
