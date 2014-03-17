#!/bin/bash

# Prequisites:
# - Python 2.7 with development headers (python-dev)

HOMEDIR=`pwd`

# Install pip
curl https://raw.github.com/pypa/pip/master/contrib/get-pip.py | sudo python

# Install django
sudo pip install django

# Install readline (optional; if not, add --without-readline to ./configure)
wget ftp://ftp.cwru.edu/pub/bash/readline-6.3.tar.gz
tar -xzf readline-6.3.tar.gz
cd readline-6.3
./configure
make
sudo make install
# For RPM-systems: sudo yum install readline readline-devel
# For Ubuntu: sudo apt-get install libreadline6 libreadline6-dev

# Install Postges 9.3
cd ~/Downloads
wget http://ftp.postgresql.org/pub/source/v9.3.0/postgresql-9.3.0.tar.gz
tar -xzf postgresql-9.3.0.tar.gz
cd postgresql-9.3.0
./configure --enable-debug --without-zlib
make
sudo make install

# Set up Postgres
sudo adduser postgres
passwd postgres
mkdir /usr/local/pgsql/data
sudo chown postgres:postgres /usr/local/pgsql/data
su -c "/usr/local/pgsql/bin/initdb -D /usr/local/pgsql/data/" postgres
su -c "/usr/local/pgsql/bin/postmaster -D /usr/local/pgsql/data > /home/postgres/logfile 2>&1 &" postgres
su -c "/usr/local/pgsql/bin/createdb agent" postgres
sudo ln -s /usr/local/pgsql/bin/psql /usr/local/bin/psql

# Add Postgres binaries to path (optional)
echo 'PATH="/usr/local/pgsql/bin":$PATH' > ~/.bashrc
source ~/.bashrc

# To login: psql agent postgres

cd $HOMEDIR

# Install psycopg2
sudo PATH=/usr/local/pgsql/bin:$PATH pip install psycopg2

# Add django user with appropriate permissions
