# Testing Flask #

## Description ##

A repository for learning to use python flask following the steps found [here](http://flask.pocoo.org/docs/1.0/tutorial/)
This is a toy repository for using Flask


## Installation & Requirements ##

**Requirements**
* pip3
* pipenv
* autoenv
* python3
* python-libs
* Flaskr


## Usage ##

Example codes for building python flask applications


* `pipenv shell` To launch virtual environment
* `pip install -e .` To install application OR
* `pip install flaskr-1.0.0-py3-none-any.whl`
* defining the environment:
```bash
set FLASK_APP=flaskr
set FLASK_ENV=development
```

* The database can be initialized with the command: `flask initdb`
* The app can be run simply by the command: `flask run`
* Generate a secret key for production:
```bash
python -c 'import os; print(os.urandom(16))'

b'_5#y2L"F4Q8z\n\xec]/'
```
* Create the config.py file in the instance folder and add
```python
SECRET_KEY = b'_5#y2L"F4Q8z\n\xec]/'
```
* production server example `waitress-serve --call 'flaskr:create_app'`
## License ##
