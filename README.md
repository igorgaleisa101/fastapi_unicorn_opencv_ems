EMS Tracking API
================

This is an API for tracking packages sent through EMS (China Post Express Mail Service). It uses FastAPI as the web framework and DigitalOcean for deployment.

Prerequisites
-------------

-   Python 3.6+
-   FastAPI
-   PIL
-   requests


Installation
------------

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the dependencies.


`pip install fastapi
pip install pillow
pip install requests
pip install captchasolver`

Usage
-----

To run the API on your local machine, use the following command:


`uvicorn main:app --reload`

This will run the API on `http://localhost:8000/`

Make a `POST` request to `http://localhost:8000/track` with json data


`{
    "tracking_number":"LY932726434CN"
}`

Deployment
----------

To deploy this API on DigitalOcean, you will need to create a droplet and install all the dependencies on the server.

Use the following command to run the API on your droplet:


`uvicorn main:app --host 0.0.0.0 --port 8000`

Make sure to configure your server firewall and DNS settings to allow incoming traffic on port 8000.

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