- pip install 
```
$ pip install -r requirements.txt
```

- Start redis on docker
```
$ docker run --name redis -d -p 6379:6379 redis:latest
```

- Start FastAPI server
```
$ fastapi dev TestTask/main.py
```