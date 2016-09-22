# 21 Flask Boilerplate

The 21 Flask Boilerplate provides a template app with built-in 21 Bitcoin Computer features to enable developers to quickly get their project off the ground.  The Boilerplate includes two1 library integration providing Bitcoin Computer operators  with access to mining and wallet information from a client-side application. The application also providers new users with a multisignature HD wallet provided by BitGo, enabling users to send and receive Bitcoin from an individually-provisioned wallet.

## How to develop on the Flask Boilerplate

The 21 Flask Boilerplate must be run on a 21 Bitcoin Computer, please ensure that you have Python3 and Pip installed.

### Quick-Start (without BitGo wallet software)

Install the required libraries. 
Install this first line if you are working with the 21 free client on a Ubuntu instance.
```
$ sudo apt-get install build-essential libssl-dev libffi-dev python-dev
$ sudo pip3 install -r requirements.txt
```
Create and initialize the database.
```
$ python3 createdb.py
```
Run the application.
```
$ python3 run.py
```
If running 21 BC as desktop, open a browser and navigate to:
```
localhost:5000
```
If ssh'ing into your 21 BC, Install unzip:
``` 
$ sudo apt-get install unzip
```
 Download [ngrok](https://ngrok.com) on your Bitcoin Computer, then:
``` 
$ unzip /path/to/ngrok.zip
```
Run ngrok
```
$ /path/to/ngrok http 5000
```
Navigate to the forwarding link provided by ngrok (will end with ngrok.io): 
```
EX: https://[random string].ngrok.io
```
To access the admin panel which provides the 21 BC mining and wallet diagnostics navigate to:
```
/admin
```
and use the username 'admin' and password 'password'.

To access the Bitcoin wallet (only works after BitGo wallet software setup) navigate to: 
```
/marketplace
```
and sign up for an account. The information you enter will be stored on your local database.
### BitGo wallet software setup

1. Install Node and NPM
	```
	curl -sL https://deb.nodesource.com/setup_4.x | sudo -E bash -
	sudo apt-get install -y nodejs
	```

2. Install BitGo Express
	```
	git clone https://github.com/BitGo/bitgo-express
	cd bitgo-express
	npm install
	```

3. Signup on BitGo and get a developer's token
  * Sign up at www.bitgo.com/wallet.
  * Once logged in, select the gear on the top right hand corner.
  * Select ‘API Access’.
  * Select the ‘Add Access Token’ button.
  * Enter all necessary information and select ‘Add Token’.
  * Set the BTC token limit to something reasonable, and ensure that you enter the public IP address of your 21 computer.
  * Your token will appear at the top of the page.
  * Take this token and set it to the ACCESS_TOKEN variable in config.py 

4. Run BitGo Express
	```
	./bin/bitgo-express --debug --port 3080 --env prod --bind localhost &
	```

## Folder Structure

The folder structure mandates that everything be held in the ``/app`` folder, all initialization and configurations to be maintained out of this folder

``/static`` - Contains all javascript and css

``/templates`` - Contains the Jinja2 templates which source all javascript and styles from the statics folder

``/views`` - Contains all of the routes and associated logic

``/toolbox`` - Contains utilities such as the mutlisig wallet / email libraries

``/models`` - Contains all database models

``/forms`` - Contains the rules and error checking for all forms in the templates

## 21 Specific Features

- [x] Admin panel to provide information on 21 diagnostics
- [x] Per user, individually provisioned wallets
- [x] HD child address generation
- [ ] QR Code support
- [x] Wallet send flow
- [ ] Public listing of 402 endpoints (nice to have)
- [ ] Public access to 402 endpoint for each user, will be centralized through 21-user for now (nice to have)
- [x] Admin panel accessible by the 21 owner
- [x] All information available through 21-cli displayable for admins
- [ ] All functionality available with the 21-cli available to admins (flush, mine, etc.)

Please feel free to fill in anything else that you feel would be useful or to create an issue with your suggestion, with an emphasis on tools that have broad use cases

## Generic Boilerplate Features

- [x] User account sign up, sign in, password reset, all through asynchronous email confirmation.
- [ ] Social media logins (Twitter, Facebook, Github) 
- [x] Form generation.
- [x] Error handling.
- [x] HTML macros and layout file.
- [x] "Functional" file structure.
- [x] Python 3.x compliant.
- [x] Asynchronous AJAX calls.
- [ ] Application factory.
- [x] Online administration.
- [ ] Static file bundling, automatic SCSS to CSS conversion and automatic minifying.
- [ ] Websockets (for example for live chatting)
- [x] Virtual environment example.
- [ ] Heroku deployment example.
- [x] Digital Ocean deployment example.
- [ ] Tests.
- [ ] Logging.
- [ ] Language selection.

## Libraries

### Backend

- [Flask](http://flask.pocoo.org/).
- [Flask-Login](https://flask-login.readthedocs.org/en/latest/) for the user accounts.
- [Flask-SQLAlchemy](https://pythonhosted.org/Flask-SQLAlchemy/) interacting with the database.
- [Flask-WTF](https://flask-wtf.readthedocs.org/en/latest/) and [WTForms](https://wtforms.readthedocs.org/en/latest/) for the form handling.
- [Flask-Mail](https://pythonhosted.org/Flask-Mail/) for sending mails.
- [itsdangerous](http://pythonhosted.org/itsdangerous/) for generating random tokens for the confirmation emails.
- [Flask-Bcrypt](https://flask-bcrypt.readthedocs.org/en/latest/) for generating secret user passwords.
- [Flask-Admin](https://flask-admin.readthedocs.org/en/latest/) for building an administration interface.

### Frontend

- [Semantic UI](http://semantic-ui.com/) for the global style. Very similar to [Bootstrap](http://getbootstrap.com/).
- [Leaflet JS](http://leafletjs.com/) for the map. I only added for the sake of the example.

## Deployment

- Heroku
- [Digital Ocean](deployment/Digital-Ocean.md)


## Configuration

Configuration paramaters can be set in ``config.py``. Please change the default params if using in a production environment.

There is a working Gmail account to confirm user email addresses and reset user passwords. The same goes for API keys, you should keep them secret. You can read more about secret configuration files [here](https://exploreflask.com/configuration.html).

Read [this](http://flask.pocoo.org/docs/0.10/config/) for information on the possible configuration options.



