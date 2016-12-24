#!/usr/bin/env bash

echo "Installing requirements via apt-get"
apt-get -qq update -y >/dev/null
apt-get -qq install -y python3-pip >/dev/null
apt-get -qq install -y python3-dev >/dev/null
apt-get -qq install -y python3-setuptools >/dev/null

echo "Upgrading and installing pip requirements"
pip install --upgrade pip
pip install -r requirements.txt
pip install coverage

echo "Copying settings.ini.example file to settings.ini"
cp settings.ini.example settings.ini

echo "Enabling set-e"
set -e

echo "----- migrations -----"
python manage.py makemigrations
python manage.py migrate
echo "----- migrations -----"

echo "----- pip freeze -----"
pip freeze
echo "----- pip freeze -----"

echo "Docker/Django configured."
