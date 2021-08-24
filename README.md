# app_name

This is a template repository used for creating Django-Vue applications. Use this template to create a new project repository.

## System Requirements

- Python (3+)
- Docker
- Node

## Development Stack

- Django (2.1 - 2.3)
- Webpack (5.x)
- Vue (3.x)
- Bootstrap (5.x)

## Cloning

Clone this template repo as a new repo (command line)

        $ git clone git@github.com:uw-it-aca/axdd-django-vue.git <new-repo>

OR.. using the Gihub interface, click on the "Use this template" button. Github will automatically clone this repo and setup everything for you.

## Configuration

After cloning this repo, find and replace the following instances to match your new repo name.

        'axdd-django-vue' with <new-repo>

Find and replace the following instance of the new Django app_name.

        'app_name' with <new_app>
        'app_name_vue' with <new_app_vue>

Copy the sample .env file so that your environment can be run.

        $ cp .env.sample .env

Update any .env variables for local development purposes

## Update README

Replace the README.md file with the README_sample.md

        $ mv README_sample.md README.md
        $ git rm README_sample.md

View the new README on your new Github repository page. Your project should be ready to start development after following those additional steps!
