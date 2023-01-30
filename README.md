# Post Tracking API v.3.0


This is an API for tracking packages sent through China Post services.

## Supported Post Services


-   EMS
-   Global Track Trace
-   USPS


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


## Deployment with docker


###  Installing docker using the repository

 [Install Docker Engine on Ubuntu](https://docs.docker.com/engine/install/ubuntu/)

#### 1. Update the apt package index and install packages to allow apt to use a repository over HTTPS:

> sudo apt-get update\
> sudo apt-get install ca-certificates curl gnupg lsb-release

#### 2. Add Docker’s official GPG key:

> sudo mkdir -p /etc/apt/keyrings\
> curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

#### 3. Use the following command to set up the repository:
> echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

#### 4. Grant read permission for the Docker public key file before updating the package index:
> sudo chmod a+r /etc/apt/keyrings/docker.gpg\
> sudo apt-get update

#### 5. Install Docker Engine, containerd, and Docker Compose:
> sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin docker-compose

## Building and running the application

###  Build the application image

> docker-compose build

###  Start and run the application container

> docker-compose up -d

###  **NOTE:** If you updated anything in the code or even access whitelist run:

> docker-compose up -d --force


## Other useful commands:

### List all images that are currently stored

> docker images

### List all running containers

> docker ps




## API Endpoint
### EMS
> GET /ems/track?tracking_number={tracking_number}&proxy={0 or 1}

### Global Track
> GET /globaltracktrace/track?tracking_number={tracking_number}&proxy={0 or 1}

### USPS
> GET /usps/track?tracking_number={tracking_number}&proxy={0 or 1}


## Parameters

-   `tracking_number`: The tracking number of the package you want to track.
-   `proxy [optional; default=0]`: Set to 1 if you want to use proxy and 0 if you don't.


