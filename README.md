# Greet
You need atleast python 3.6 and redis server to run greet.

```
#setup dependencies
pip install flask redis

# start redis server
redis-server

# run app
python greet.py
```

Once application starts running visit http://localhost:8080 to view the greeting. 

```
curl http://localhost:8080
```

To change name in greeting, send a POST request

```
curl -X POST -H "Content-Type: application/json" -d "{\"name\": \"Ben\"}" http://localhost:8080
```


