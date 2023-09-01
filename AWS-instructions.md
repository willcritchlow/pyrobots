# Getting up and running on an ubuntu AWS server

- `sudo apt-get update`
- `sudo apt-get upgrade`

## if you want to build the c++ files

`sudo apt-get install cmake`

- `git clone https://github.com/willcritchlow/robotstxt.git`
- `cd robotstxt`
- `git checkout pythoncallingexecutable`

`sudo apt-get install build-essential`

- `mkdir c-build && cd c-build`
- `cmake .. -DROBOTS_BUILD_TESTS=ON`
- `make`

Note: if not built on this machine, will need the folder to be copied in to the same path (/home/ubuntu/robotstxt) so that linking works (until / unless I understand C++ better)

## to get the flask app up and running

`cd`

`sudo apt-get install python3-venv`

`python3 -m venv ./virtualenv/pyrobots`

`source ./virtualenv/pyrobots/bin/activate`

`pip install --upgrade pip`

`git clone https://github.com/willcritchlow/pyrobots.git`

`cd pyrobots`

`python3 -m pip install -r requirements.txt`

`sudo apt-get install nginx`

`sudo cp nginx.conf /etc/nginx/nginx.conf`

REBOOT

`source ./virtualenv/pyrobots/bin/activate`

`cd pyrobots`

`sudo apt-get install gunicorn`

`gunicorn -w 4 pyrobots:app --daemon`

`sudo nginx -s stop`

`sudo nginx`

Set up cloudflare pointing at IP address (to get https)

Attach IP address to server in AWS

Open up port 443 in AWS

## After redeploying code

`ps aux | grep 'gunicorn'`

`kill -HUP <master_process_id>`

or possibly:

`pkill gunicorn`

`source ./virtualenv/pyrobots/bin/activate`

`cd pyrobots`

`gunicorn -w 4 pyrobots:app --daemon`

`sudo nginx -s stop`

`sudo nginx`