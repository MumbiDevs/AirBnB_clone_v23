#!/usr/bin/env python3
"""
Fabric script that distributes an archive to your web servers, using the function do_deploy.
"""

from fabric.api import env, put, run, local
from os.path import exists
from datetime import datetime
import os

# Define your server IPs or hostnames here
env.hosts = ['<IP web-01>', '<IP web-02>']


def do_deploy(archive_path):
    """
    Distributes an archive to your web servers.
    Args:
        archive_path: Path to the archive to deploy on the server.
    Returns:
        True if all operations have been done correctly, False otherwise.
    """
    if not os.path.exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, '/tmp/')

        # Extract archive name without extension
        archive_filename = os.path.basename(archive_path)
        archive_name = os.path.splitext(archive_filename)[0]

        # Create directory to uncompress the archive
        run('mkdir -p /data/web_static/releases/{}/'.format(archive_name))

        # Uncompress the archive to the target directory
        run('tar -xzf /tmp/{} -C /data/web_static/releases/{}/'.format(
            archive_filename, archive_name))

        # Remove the uploaded archive from /tmp/
        run('rm /tmp/{}'.format(archive_filename))

        # Move contents of web_static to the release directory
        run('mv /data/web_static/releases/{}/web_static/* '
            '/data/web_static/releases/{}/'.format(archive_name, archive_name))

        # Remove the now unnecessary web_static folder
        run('rm -rf /data/web_static/releases/{}/web_static'.format(archive_name))

        # Remove the existing symbolic link if it exists
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link linked to the new version
        run('ln -s /data/web_static/releases/{}/ /data/web_static/current'.format(archive_name))

        print("New version deployed!")
        return True

    except:
        return False
