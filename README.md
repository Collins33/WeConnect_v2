# WeConnect

WeConnect provides a platform that brings businesses and individuals together. This platform creates awareness for businesses and gives the users the ability to write reviews about the businesses they have interacted with using an api

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/fc3b48f3c8ae41c281b52e3055612cfc)](https://www.codacy.com/app/Collins33/WeConnect_v2?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Collins33/WeConnect_v2&amp;utm_campaign=Badge_Grade)

## Getting Started

-git clone https://github.com/Collins33/WeConnect_v2.git

-cd WeConnect_v2

-virtualenv venv

-source venv/bin/activate

-pip install -r requirements.txt

## Database
-Ensure Postgresql is installed in your machine

-Create database weconnect

## Migrations
-python manage.py db init

-python manage.py db migrate

-python manage.py db upgrade

## Running tests
-pytest

### Prerequisites

-python 3.6

-virtual environment

-postgresql

## Running it on machine
-create .env file and add the environment variables

-run source .env

-flask run

## ENDPOINTS
| Endpoint                                | FUNCTIONALITY |
| ----------------------------------------|:-------------:|
| POST /api/auth/register                 | This will register  the user       |
| POST /api/auth/login                    | This will login a registered user  |
| POST /api/auth/logout                   | This will log out a logged in user |
| POST /api/auth/reset-password           | This will reset the password       | 
| POST  /api/businesses                   | This will add the business         |
| PUT /api/businesses/businessId          | This will update the business      | 
| DELETE /api//businesses/businessId      | This will delete a business        |
| GET  /api/businesses                    | This will get all businesses       |
| GET  /api/businesses/businessId         | retrieve a single business by id   |
| GET  /api/businesses/businessName       | retrieve a single business by name |
| POST  /api/businesses/businessId/reviews| add a review                  |
| GET  /api/businesses/businessId/reviews | get all reviews for a business               |       
       
       


## Built With

* [Flask](http://flask.pocoo.org/) - The web framework used
* [Pip](https://pypi.python.org/pypi/pip) - Dependency Management
* [HTML/CSS/BOOTSTRAP](https://getbootstrap.com/)-Front-end 


 

## Authors

* **COLLINS NJAU MURU** 



## License

This project is licensed under the MIT License ]




