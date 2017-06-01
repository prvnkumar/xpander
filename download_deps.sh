#! /bin/sh

echo "Updating apt-get..."
sudo apt-get -y update

echo -e "\nInstalling git..."
sudo apt-get -y install git

echo -e "\nInstalling virtualenv..."
sudo apt-get -y install python-virtualenv

echo -e "\nInstalling python2.7 and pip..."
sudo apt-get -y install python2.7
sudo apt-get -y install python-pip

#echo -e "\nCloning repo... You may be prompted for credentials"
#git clone https://github.com/prvnkumar/xpander.git

echo -e "\nGetting mininet..."
if [ -d "$mininet" ]; then
    git clone git://github.com/mininet/mininet
    cd mininet
    git checkout -b 2.2.1 2.2.1
    cd ..
    ./mininet/util/install.sh -a 
else
    echo -e "\nMininet already downloaded. Skipping this step."
fi

echo -e "\nSetting up virtual environment..."
if [ -d "$mininet" ]; then
    virtualenv --system-site-packages venv
else
    echo -e "\nVirtual Environment already set up. Skipping this step."
fi
source venv/bin/activate

echo -e "\nInstalling python dependencies..."
sudo pip install --upgrade pip
sudo apt-get -y install libfreetype6-dev libpng-dev
sudo pip install --ignore-installed numpy
sudo pip install --ignore-installed matplotlib
sudo pip install --ignore-installed pulp
sudo pip install --ignore-installed networkx

