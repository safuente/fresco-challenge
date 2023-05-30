Backend Coding Challenge Fresco (Santiago Alvarez)
====================================

Recipe API made in Django REST. It is needed to have installed make command and Docker to run the app.
A Postgres database was used to persist the data.
Flake8 package was used as a code linter.

## Run local environment

To run the container please execute the following command:

    make up

Once the command is executed go to the following link http://localhost:8000. You will have access to swagger
in order to test the API

## Test the API
1) Create a user for testing executing the following command:

       make user

2) Create some test ingredients to be used to create recipes :
   
        make ingredients


After that you have to make a post request to http://localhost:8000/api/users/token using the email and password 
with the testing credentials in Makefile in user command.
This endpoint is going to return a token. 

To set the token in the swagger you have to click on "Authorize" and then copy in tokenAuth (apiKey) section in value input field
the following content:

        Token <value_of_the_token_endpoint>

Then close the window. This token is going to be used to request all the endpoint of recipe API

3) You have 4 endpoints for recipes:

         POST: create a recipe
         UPDATE: update recipe value
         GET: get the list of recipes for the current user
         GET DETAIL: get a recipe by id

4) You can check the list of ingredients from the django admin:

      make superuser

After that you can acces to the admin to http://localhost:8000/admin using the email and password 
with the testing credentials in Makefile in superuser command. Here you can check the ingredients to use in recipe creation


## Other useful commands

Build docker image

    make build

Stop containers

    make stop

Stop containers

    make stop

Delete containers

    make rm

Run unit tests

    make test

Run flake8 linter:

    make lint