# ToTheMoon.API
Crypto Price Alert Web Application's Core Backend, developed as a recruitment task for Krypto 

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
