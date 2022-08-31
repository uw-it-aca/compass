# Compass

A application for managing student advising information.

## System Requirements

- Python (3+)
- Docker
- Node

## Development Stack

- Django (3.2)
- Vue (3.x)
- Bootstrap (5.2)

## Development (using Docker)

Go to your repository

        $ cd new-repo

Copy the sample .env file so that your environment can be run.

        $ cp .env.sample .env

Update any .env variables for local development purposes

Docker/Docker Compose is used to containerize your local build environment and deploy it to an 'app' container which is exposed to your localhost so you can view your application. Docker Compose creates a 'devtools' container - which is used for local development. Changes made locally are automatically syncd to the 'app' container.

        $ docker-compose up --build

View your application using your specified port number in the .env file

        Demo: http://localhost:8000/
