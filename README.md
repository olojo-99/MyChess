# MyChess

## Install the following packages/library versions

### MacOS
    pip3 install channels==3.0.4
    pip3 install channels-redis==4.0.0
    pip3 install django-redis
    brew install redis

### Linux
    pip3 install channels==3.0.4
    pip3 install channels-redis==4.0.0
    pip3 install django-redis
    sudo apt install redis-server

    For redis configuration on Ubuntu, see https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-redis-on-ubuntu-18-04


## Django Setup
    python3 manage.py makemigrations
    python3 manage.py migrate --run-syncdb

## Running Servers
    python3 manage.py runserver
    redis-server

## Playing Games
    Go to localhost on two separated clients (i.e. open an incognito browser)
    Register or Log in
    Click on account name hyperlink for game menu
    Challenge user or accept challenge