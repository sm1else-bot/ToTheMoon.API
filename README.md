# ToTheMoon.API
Crypto Price Alert Web Application's Core Backend, developed as a recruitment task for Krypto 

### Tech Stack:
The backend is written in Python with Flask for the web application framework, SQLite for the Database Engine, SQLAlchemy as the Object Relational Mapper and Postman is used for API testing.

The web app is also configured for dockerization and an image can be built by running 'docker build -t ToTheMoonAPI:latest .'

### Description:
This backend works in two 'modes', 'config' by default and 'activated' via the /emailmode endpoint. Config mode has 3 API endpoints, creating an alert, deleting an alert and fetching all alerts by user which can be filtered by status and such. After some frontend magic, this can be used in building a web app to send you E-Mail alerts as the real time price index of BTC-USD reaches your preferred target using GMail SMTP. The Authentication is done with SHA-256 Encryption using JWT access tokens that are valid for 60 minutes post generation

### Installation:
1. Pull this repository and extract the lib.rar file inside the venv directory
2. rename the venv directory into .venv (Hidden Folder)
3. open a Terminal session within the api folder (Command Prompt on windows preferred)
4. activate the virtual environment by using .venv/Scripts/activate
5. install dependencies from the text file using run conda install --file requirements.txt or similar
6. run the commands below from the api directory in the terminal
set FLASK_APP=application.py
set FLASK_ENV=development 
or equivalent commands as per operating system
7. write and execute the command: flask run
 
#### If everything goes well, the backend should be up and running on your localhost at port 5000

The homepage at localhost:5000/ shows the current price of bitcoin as retreived from CoinGecko's API 

## Documentation:

### API Endpoints:

##### There are 4 Endpoints in total, 3 for the Alerts and 1 to switch to activated mode, which continues to run and update the user.

#### /alerts/create - POST Requests

Usage: Create an alert for a particular user to get email alerts when the price of BTC crosses a particular target.

parameters: u_id - user id, a_id - alert id, a_target - target price

Status is set to created when an alert is made using the POST call

#### /alerts/delete - PUT Requests

Usage: Delete an alert based on alert id, status is changed to deleted and the alert is not sent if it was not triggered before deletion, record is preserved in the database.

parameters: a_id - alert id

#### /alerts - GET Requests

Usage: Fetch all alerts made for a particular user, filter by user id and query filter for the alert status.

parameters: u_id - user id, queryfilter - status of the alert, can be one of ['created','deleted','triggered']

#### /emailmode - GET Requests

Unlike the other 3 endpoints where we have a raw json in the request body with the required parameters, this serves as a toggle for the 'activated' mode that will start checking and updating bitcoin_rate in real time in accordance with Coinbase's API (switched from CoinGecko for a better functional API response that's easier to format and compare) and while it looks like it's loading forever in the browser at this API path, it just means that its functional and sending e-mails via hardcoded gmail SMTP credentials.

The console will also output the current value of Bitcoin every 5 minutes, with some modifications this can be returned from the client side as well, but that's for the frontend guys to play around with, right?

### Endpoints that are related to CRUD operations will require access tokens to execute, which are valid for 60 minutes post generation during login.


## Dependencies for this project:

check Requirements.txt for it, no time to format it properly here :')

## About the Developer:

Name: Jessenth Ebenezer S
Registration No: 19BCE1462








