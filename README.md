EMS Tracking API
================

This is an API for tracking packages sent through EMS (China Post Express Mail Service). It uses FastAPI as the web framework and DigitalOcean for deployment.

Prerequisites
-------------

-   Python 3.6+
-   FastAPI
-   Pillow
-   requests
-   numpy


Installation
------------

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the dependencies.


`pip install -r requirements.txt`

Usage
-----

To run the API on your local machine, use the following command:


`uvicorn main:app --reload`

This will run the API on `http://localhost:8000/`

Make a `GET` request to `http://localhost:8000/ems/track?tracking_number={tracking_number}`

Deployment
----------

To deploy this API on DigitalOcean, you will need to create a droplet and install all the dependencies on the server.

Use the following command to run the API on your droplet:


`uvicorn main:app --host 0.0.0.0 --port 8000`

Make sure to configure your server firewall and DNS settings to allow incoming traffic on port 8000.


To Deploy and work in background using Nginx
https://dev.to/shuv1824/deploy-fastapi-application-on-ubuntu-with-nginx-gunicorn-and-uvicorn-3mbl

`sudo apt update
 sudo apt install nginx`

Install gunicorn and uvicorn

`pip install gunicorn uvicorn`


Configure Nginx
Now our application is ready to be run and tested. To be able to serve the application over HTTP we have to make an Nginx config for our application.

`sudo vim /etc/nginx/sites-available/myapp`

Put the followings on that file:

`server {
       server_name <server-ip>;
       location / {
           include proxy_params;
           proxy_pass http://127.0.0.1:8000;
       }
}`

Now we save the file and exit. Then we make a symbolic link to this config file in the /etc/nginx/sites-enabled directory.
`sudo ln -s /etc/nginx/sites-available/myapp /etc/nginx/sites-enabled/`

Then we restart the Nginx service.
`sudo systemctl restart nginx.service`

Now we can start our uvicorn server to check if our application is working or not.
`gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:80`



API Endpoint
--------

`GET /ems/track?tracking_number={tracking_number}`

Description
-----------

This endpoint allows you to track your EMS package by providing the tracking number. It returns a JSON object containing the tracking information for the package.

Parameters
----------

-   `tracking_number`: The tracking number of the package you want to track.

Example Request
---------------

`GET /ems/track?tracking_number=LY932726434CN`
