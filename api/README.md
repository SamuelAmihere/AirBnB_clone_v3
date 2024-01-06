# API
## Environment Requirement
* __OS:__ Ubuntu 14.04 LTS
* __language:__ Python 3.4.3
* __application server:__ Flask 0.12.2, Jinja2 2.9.6
* __web server gateway:__ gunicorn (version 19.7.1)
* __database:__ mysql Ver 14.14 Distrib 5.7.18
* __documentation:__ Swagger (flasgger==0.6.6)
* __Style:__
  * __python:__ PEP 8 (v. 1.7.0)

## Let's Test the API

* Execute program:

```
HBNB_MYSQL_USER=hbnb_dev HBNB_MYSQL_PWD=hbnb_dev_pwd \
HBNB_MYSQL_HOST=localhost HBNB_MYSQL_DB=hbnb_dev_db HBNB_TYPE_STORAGE=db \
HBNB_API_HOST=0.0.0.0 HBNB_API_PORT=5000 python3 -m api.v1.app
```

* Testing:

* Testing from CLI:

```
$ curl -X GET http://0.0.0.0:5000/status

{
  "status": "OK"
}
```

Check content type:
```
$ curl -X GET -s http://0.0.0.0:5000/api/v1/status -vvv 2>&1 | grep Content-Type
< Content-Type: application/json
$ 
```

Let's check some stats about objects in the database
```
$ curl -X GET http://0.0.0.0:5000/api/v1/stats
{
  "amenities": 47, 
  "cities": 36, 
  "places": 154, 
  "reviews": 718, 
  "states": 27, 
  "users": 31
}
$ 
```
