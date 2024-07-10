#!/usr/bin/env python3
"""
Fabric script that generates a .tgz archive from the contents of the web_static
folder of your AirBnB Clone repo, using the function do_pack.
"""

from fabric.api import local
from datetime import datetime
import os

def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.
    Returns:
        Archive path if archive was created successfully, None otherwise.
    """
    # Create the folder 'versions' if it doesn't exist
    local("mkdir -p versions")

    # Generate the name of the archive
    now = datetime.now()
    archive_name = "web_static_{}{}{}{}{}{}.tgz".format(
        now.year, now.month, now.day, now.hour, now.minute, now.second)

    # Compress the contents of the web_static folder
    result = local("tar -cvzf versions/{} web_static".format(archive_name))

    # Check if tar command was successful
    if result.failed:
        return None
    else:
        return "versions/{}".format(archive_name)
