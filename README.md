# Basic users & groups RESTful API (written in Python)

## Dependencies
  - Docker 19.03.8
  - Python 3.7.4
  - Flask 1.1.1
  - PyTest 5.4.3
  - Requests 2.23.0
<br /><br />

## Installation & Execution
After cloning/downloading 'restful-api'...
<br />

**1. create environment file**
```
$ cd restful-api
$ cp env.dev .env.dev
```

**2. install dependencies in virtual environment**
```
$ cd services/rest
$ python3 -m venv venv
$ source venv/bin/activate
(venv)$ pip3 install flask==1.1.1
(venv)$ pip3 install pytest==5.4.3
(venv)$ pip3 install requests==2.23.0
```

**3. build & run docker image**
```
(venv)$ docker-compose build
(venv)$ docker-compose up -d
```

**4. create & initialize db**
```
(venv)$ docker-compose exec rest python manage.py create_db
```

**5. run tests**
```
(venv)$ py.test -v
```
<br />

## Notes

### API Routes
Once installed and running, you can make api requests using the following routes:
<br />

```
http://127.0.0.1:5000/groups
(POST)

http://127.0.0.1:5000/groups/<group name>
(GET, PUT, DELETE)

http://127.0.0.1:5000/users
(POST)

http://127.0.0.1:5000/groups/<userid>
(GET, PUT, DELETE)
```

### Tests & Database
Tests should be run from an initialized database with no data. Tests are organized to execute sequentially; i.e. each test relies on all of the tests before passing. **_Always 'create & initialize db' (step 4 above) before executing tests._**
