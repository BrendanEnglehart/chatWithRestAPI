# Productionalizing the Rest API
Note, this is just for the Rest API, not for frontend. Once you finish the Rest API, you can proceed to the Frontend if you plan to use that. 

## Connecting to MongoDB
1. Have an account setup with MongoDB. If you plan to use an alternative database, you will need to amend some of the database methods. For most databases that simply means finds become selects and you will have to convert the json into a select statement.
2. Create a database and enable your address to access the database
3. Copy the URI from your MongoDB Database and create a `.env` file in the database directory. Add `URI=youruri` to the `.env` file 
```
URI="mongodb+srv//username:values.mongodb.net/?appname=Database"
```

## Running on a VM or BareMetal
1. CD into the main directory and start up a Python virtual environment `python -m venv /your/path/to/venv`
2. Run `pip install -r requirements.txt`
3. run  `gunicorn --bind 0.0.0.0:$PORT app:gunicorn` replacing $PORT with the port you wish to run this on, typically 5001. 

## Running in a container
Build the docker image in the main directory and then setup your config file for your flavor of container. If you are using K8s it should look something like
```
...
spec:
  template:
    spec:
      containers:
      - name: restAPI
        image: $IMAGE
        ports:
        - containerport: $PORT
```
