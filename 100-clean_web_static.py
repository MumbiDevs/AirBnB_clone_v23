#!/usr/bin/env python3
"""
Fabric script that deletes out-of-date archives, using the function do_clean.
"""

from fabric.api import env, local, run
import os

# Define your server IPs or hostnames here
env.hosts = ['<IP web-01>', '<IP web-02>']


def do_clean(number=0):
    """
    Deletes out-of-date archives from versions and /data/web_static/releases folders.
    Args:
        number: Number of archives to keep (including the most recent).
                If 0 or 1, keep only the most recent archive.
                If 2, keep the most recent and second most recent archives, etc.
    """
    try:
        number = int(number)
        if number < 1:
            number = 1
    except ValueError:
        number = 1

    # Local clean-up of versions folder
    local("ls -t versions | tail -n +{} | xargs -I {{}} rm versions/{{}}".format(number + 1))

    # Remote clean-up of releases folder on web servers
    with cd('/data/web_static/releases'):
        run("ls -t | tail -n +{} | xargs -I {{}} rm -rf {{}}".format(number + 1))

