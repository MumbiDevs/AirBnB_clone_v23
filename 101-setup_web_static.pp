# Ensure Nginx is installed
package { 'nginx':
  ensure => installed,
}

# Define directories and file paths
$web_static_path = '/data/web_static'
$releases_path = "${web_static_path}/releases"
$shared_path = "${web_static_path}/shared"
$test_release_path = "${releases_path}/test"
$current_link = "${web_static_path}/current"

# Ensure directories exist
file { [$web_static_path, $releases_path, $shared_path, $test_release_path]:
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
  mode   => '0755',
}

# Create a fake HTML file
file { "${test_release_path}/index.html":
  ensure  => file,
  content => '<html><head></head><body>Holberton School</body></html>',
  owner   => 'ubuntu',
  group   => 'ubuntu',
  mode    => '0644',
}

# Manage symbolic link /data/web_static/current
file { $current_link:
  ensure => link,
  target => $test_release_path,
  force  => true,
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

# Define Nginx site configuration for hbnb_static
file { '/etc/nginx/sites-available/default':
  ensure  => file,
  content => "
    server {
        listen 80 default_server;
        listen [::]:80 default_server;

        root /var/www/html;
        index index.html index.htm index.nginx-debian.html;

        server_name _;

        location /hbnb_static {
            alias ${current_link};
        }

        location / {
            try_files \$uri \$uri/ =404;
        }
    }
  ",
  notify => Service['nginx'],
}

# Restart Nginx when configuration changes
service { 'nginx':
  ensure    => running,
  enable    => true,
  subscribe => File['/etc/nginx/sites-available/default'],
}
