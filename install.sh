#!/usr/bin/sh

# Prequisites:
# - Ubuntu
# - Python 2.7

# Install pip
curl https://raw.github.com/pypa/pip/master/contrib/get-pip.py | sudo python

# Install django
sudo pip install django

# Install Postges 9.3
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install postgresql-9.3 postgresql-9.3-contrib postgresql-9.3-client pgadmin3

# Install psycopg2
sudo pip install psycopg2
