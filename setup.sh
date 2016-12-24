#!/usr/bin/env bash

echo "Installing requirements via apt-get"
apt-get -qq update -y
apt-get -qq install -y python3-pip
apt-get -qq install -y python3-dev
apt-get -qq install -y python3-setuptools

echo "Upgrading and installing pip requirements"
pip install --upgrade pip
pip install -r requirements.txt
pip install coverage

echo "Copying settings.ini.example file to settings.ini"
cp settings.ini.example settings.ini

set -e

echo "----- migrations -----"
python manage.py makemigrations
python manage.py migrate
echo "----- migrations -----"

echo "----- pip freeze -----"
pip freeze
echo "----- pip freeze -----"

echo "No tests to run, but Django works, have a nice day..."
