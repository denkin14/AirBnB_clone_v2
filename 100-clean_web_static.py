#!/usr/bin/python3
""" This Fabric script will clean outdated archive files
"""
from fabric.api import cd, lcd, local, run, env, with_settings
from fabric.api import task, runs_once

env.hosts = ["52.86.91.204", "100.25.199.84"]


@runs_once
def do_local(number):
    """ local operations """

    with lcd('versions'):
        # check for number of files
        num_files = int(local('ls -1 | wc -l', capture=True))

        # check if number is greater than files in the directory
        if number >= num_files:
            return

        # compute the  number of files to delete
        if number == 1 or number == 0:
            limit = num_files - 1
        else:
            limit = num_files - number

        # delete files
        local("{}{}{}".format("for((i=0; i < ", limit,
              "; i++)); do rm -rf -v $(ls -r1t | head -n 1); done"),
              shell='/bin/bash')


def do_remote(number):
    """ remote operations """

    with cd('/data/web_static/releases'):
        # check for number of files
        num_files = int(run('ls -1 | wc -l'))

        # check if number is greater than files in directory
        if number >= num_files:
            return

        # compute number of files to delete
        if number == 1 or number == 0:
            limit = num_files - 1
        else:
            limit = num_files - number

        # delete files
        run("{}{}{}".format("for((i=0; i < ", limit,
            "; i++)); do rm -rf -v $(ls -r1t | head -n 1); done"))


@task
@with_settings(warn_only=True)
def do_clean(number=0):
    """ fabric task to remove outdate files """
    number = int(number)
    do_local(number)
    do_remote(number)
