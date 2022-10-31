#!/usr/bin/python3
"""Full deployment with fabric script
"""
from datetime import datetime
from fabric.api import cd, env, lcd, local, put, run, task, with_settings
from fabric.api import runs_once
from os import path

env.hosts = ["52.86.91.204", "100.25.199.84"]


@runs_once
@with_settings(warn_only=True)
def do_pack():
    """ creates compressed archive file of web_static folder
    """

    # essential variables for file name
    file_name = "web_static_{}.tgz".format(
            datetime.now().strftime('%Y%m%d%H%M%S'))

    # create directory if it doesn't exist
    if local('test -d versions').failed:
        local('mkdir versions')

    # create compressed tar file in the versions directory
    with lcd('versions'):
        execute = local('tar -zcvf {} ../web_static'.format(file_name))

    # check cmd success and return path
    if execute.succeeded:
        return "versions/{}".format(file_name)


@with_settings(warn_only=True)
def do_deploy(archive_path):
    """ deploys archive files to webservers
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


@task
def deploy():
    """ main fabric task to pack and deploy
    """

    tar = do_pack()
    if tar is None:
        return False

    status = do_deploy(tar)
    return status
