#!/usr/bin/env bash

# Install nginx if not already installed
if ! command -v nginx &> /dev/null
then
    sudo apt-get -y update
    sudo apt-get -y install nginx
fi

# Create necessary directory structure
sudo mkdir -p /data/web_static/releases/test/ /data/web_static/shared/
sudo touch /data/web_static/releases/test/index.html
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html > /dev/null

# Create or recreate symbolic link
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership of the /data/ folder to ubuntu user and group
sudo chown -R ubuntu:ubuntu /data/

# Update nginx configuration to serve /data/web_static/current/ to hbnb_static
sudo sed -i '/^\s*location \/hbnb_static {/a\
\        alias /data/web_static/current/;' /etc/nginx/sites-available/default

# Restart nginx to apply changes
sudo service nginx restart

exit 0
