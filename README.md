# Post Tracking API


This is an API for tracking packages sent through China Post services.

## Supported Post Services


-   EMS
-   Global Track Trace


## Tech Stack

-   Python 3.6+
-   FastAPI
-   Pillow
-   requests
-   numpy


## Installation

### Install the dependencies

> pip install -r requirements.txt

or

> pip3 install -r requirements.txt

## Usage


To run the API on your local machine, use the following command: 

> uvicorn main:app --host 0.0.0.0 --port 5000

Make sure to configure your server firewall and DNS settings to allow incoming traffic on port 5000.

This will run the API on:

    http://localhost:5000/


Make a `GET` request:

    http://localhost:5000/{service_name}/track?tracking_number={tracking_number}


Make a `GET` request with proxy:

    http://localhost:5000/{service_name}/track?tracking_number={tracking_number}&proxy=1


Deployment with docker
----------------------

###  Installing docker

Follow these instructions [Install Docker Engine on Ubuntu](https://docs.docker.com/engine/install/ubuntu/)

###  Installing docker-compose

> sudo apt install docker-compose


###  Build the application image

> docker-compose build

###  Start and run the application container

> docker-compose up -d



**Note**
In case you updated anything in the code or even access whitelist, you should rebuild and rerun the application.

### Other useful commands:

List all images that are currently stored
> docker images

List all running containers
> docker ps



Deployment with Nginx
---------------------

To Deploy and work in background using Nginx
https://dev.to/shuv1824/deploy-fastapi-application-on-ubuntu-with-nginx-gunicorn-and-uvicorn-3mbl

`sudo apt update`

`sudo apt install nginx`


Install gunicorn and uvicorn

`pip install gunicorn uvicorn`


Configure Nginx
Now our application is ready to be run and tested. To be able to serve the application over HTTP we have to make an Nginx config for our application.

`sudo vim /etc/nginx/sites-available/myapp`

Put the followings on that file:
```
server {
       server_name <server-ip>;
       location / {
           include proxy_params;
           proxy_pass http://127.0.0.1:8000;
       }
}
```

Now we save the file and exit. Then we make a symbolic link to this config file in the /etc/nginx/sites-enabled directory.
`sudo ln -s /etc/nginx/sites-available/myapp /etc/nginx/sites-enabled/`

Then we restart the Nginx service.

`sudo systemctl restart nginx.service`

Now we can start our uvicorn server to check if our application is working or not.

`gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:80`




API Endpoint
--------

> GET /{service_name}/track?tracking_number={tracking_number}

Description
-----------

This endpoint allows you to track your EMS package by providing the tracking number. It returns a JSON object containing the tracking information for the package.

Parameters
----------

-   `tracking_number`: The tracking number of the package you want to track.

Example Request
---------------

`GET /ems/track?tracking_number=LY932726434CN`
