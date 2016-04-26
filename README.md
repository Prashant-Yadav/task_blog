# task_blog
Simple Task for job application (creating a blogging app)

## Prerequisites

- Django 1.5+
- PostgreSQL 9+
- psqycopg 2+

## Installation

- Install the python virtualenv. I recommend to use virtualenvwrapper. Go through this link to install and configure [virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/).

- Install and configure PostgreSQL. First deactivate virtualenv.

	`deactivate`

	Now we need to install dependencies for PostgreSQL through following command:

	`sudo apt-get install libpq-dev python-dev`

	Now that you have done this, install PostgreSQL through following command:

	`sudo apt-get install postgresql postgresql-contrib`

- Configure PostgreSQL. First we have to login into postgresql server through `postgres` user.

	`sudo su -postgres`

	Now run below command to create database and name it `blog_database` :

	`createdb blog_database`

	Database has been created and named `blog_database`. Now we have to create role for this database. For creating a role named `blog_admin`, run following command:

	`createuser -P`

	You will now be met with a series of 6 prompts. The first one will ask you for the name of the new user. 

	Now activate the postgresql command line interface as follows:

	`psql`

	Finally, grant this new user access to your new database with this command.

	`GRANT ALL PRIVILEGES ON DATABASE blog_admin TO blog_admin;`

- Now activate your virtualenv again and move to the root directory of the repository which you have cloned through below command:


	`git clone https://github.com/Prashant-Yadav/task_blog.git`

- Install all the packages and dependencies through following command:

	`pip install -r requirements.txt`

- Now move to the dbblog directory through this command:

	`cd djblog/`

- To migrate the database, use following command:

	`python manage.py migrate`

- Runserver using below command:

	`python manage.py runserver`

You can access the project homepage through the link [http://localhost:8000/](http://localhost:8000/)