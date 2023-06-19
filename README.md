# Users-Manager project

## Project goals:
* Building python product frontend and backend stack
* Creating a CI pipeline for a Python product
* Deploying a high scalable Python product using CD pipeline

## Solution architecture:
###REST_API (module name: rest_app.py)  
The REST API gateway is: 127.0.0.1:5000/users/<USER_ID>

* POST – accepts user_name parameter inside the JSON payload
   > A new user will be created in the database (Please refer to Database section) with the \
        id passed in the URL and with user_name passed in the request payload. \
        ID has to be unique! \
        Example: when posting the {“user_name”: “john”} JSON payload to 127.0.0.1:5000/users/1  \
        A new user will be created in the DB (Please refer to Database section) with the id 1  \
        and the name john. 
   
* GET – returns the user name stored in the database for a given user id
> Following the example: 127.0.0.1:5000/users/1 will return john.

* PUT – will modify existing user name (in the database)
> Following the above example, when posting the {“user_name”: “george”} JSON payload to 127.0.0.1:5000/users/1 <br>
george will replace john under the id 1.

* DELETE – will delete existing user (from database)
> Following the above example, when using delete on 127.0.0.1:5000/users/1
        The user under the id 1 will be deleted.

The REST API gateway is: 127.0.0.1:5000/stop_server 
* STOP_SERVER api function is added in order to add automatic termination to both the web application server \
and the REST Api server

### Database (module name: db_connector.py):
1. Uses (any) remote MySQL service.
2. The REST API (Please refer to REST API section) will read and write data using a
MySQL table "users" table
3. "users" table will have 3 columns:
o user_id – primary key, int, not null
o user_name - varchar[50], not null
o creation_date – varchar[50] which will store user creation date (in any format)
4. Table can be created manually (and not from code) using /mysql/database_users.sql sql commands

### Web interface (module name: web_app.py):
The Web interface will be: 127.0.0.1:5001/users/get_user_data/<USER_ID>
1. The web interface will return the user name of a given user id stored inside users table
(Please refer to Database section).
2. The user name of the user will be returned in an HTML format with a locator to simplify
testing.
3. In case the ID doesn’t exist return an error (in HTML format)

### Testing:
1. Three python modules for testing frontend, backend and both combined.
2. The modules are able to run independently.

* Frontend testing – for web interface testing (module name = frontend_testing.py):
> The script:
    Starts a Selenium Webdriver session.
    Navigate to web interface URL using an existing user id.
    Check that the user name element is showing (web element exists).
    Print user name (using locator).

* Backend testing – for REST API and Database testing (module name = backend_testing.py):
> The script:
    Post a new user data to the REST API using POST method.
    Submit a GET request to make sure status code is 200 and data equals to the
posted data.
    Check posted data was stored inside DB ("users" table).

* Combined testing – for Web interface, REST API and Database testing (module name = combined_testing.py):
> The script:
    Post any new user data to the REST API using POST method.
    Submit a GET request to make sure data equals to the posted data.
    Start a Selenium Webdriver session.
    Navigate to web interface URL using the new user id.
    Check that the user name is correct.

Create another table (in DB) using /mysql/database_config.sql file and call it "config", 
the table will contain:
* The API gateway URL (e.g: 127.0.0.1:5001/users)
* The browser to test on (e.g: Chrome)
* A user name to be inserted \
Use this table to run your tests. This table will contain use-cases for testing to run.

## Project Solution
docker_test/ - dockerFiles for running backend testing applications in docker and kubernetes \
htmldocs/ - project documentation in HTML created by PyDoc \
jenkins/ - different jenkins pipelines for the project:
   >    Jenkinsfile.txt - this pipeline run the project as python desktop applications \
        Jenkinsfile_with_docker.txt - this pipeline build docker images, push it to the Docker Hub and 
   run the project as dockerized microservises application by docker-compose \
        Jenkinsfile_with_three_dockers.txt - same as previous, but running project with three containers \
   (rest_api, mysql and tester) \
        Jenkinsfile_with_k8s.txt - this pipeline deploys the project on kubernetes with help of Helm \
        Jenkinsfile_with_parameters.txt - pipeline with parameters

k8s/ - directory of yaml files for kubernetes different objects creation for deployment of project in Kubernetes
mysql/ - sql files for creation of tables in MySql
restapi/ - directory with Dockerfiles for creation of Docker images for restapi application
restapi-chart/ - restapi application Helm chart

        



