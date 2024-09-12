# Instruction:
1) Create `db directory` in root folder
2) Place sql dump file into **db directory**
`it should be named the same as MYSQL_DATABASE variable in docker-compose.yml (ru_cococo.sql)`
2) In root directory
`docker-compose up --build`
## How to change MySQL database port
Currently mysql db is on port **3307** if you want to change:

1) Change the MYSQL_TCP_PORT: 3307 line `in docker-compose.yml` to the port you like
2) Change ports:- 3307:3307 line `in docker-compose.yml` to same port you selected in previous step
3) Change sql connection string in flask app `ru_cococo_website/App/database.py` line 23:
```python
connection_string = "mysql+mysqlconnector://root:12345678@db:3307/ru_cococo" # This
engine = create_engine(connection_string, echo=False)
base = declarative_base()
```
change the part after `mysql+mysqlconnector://`:

**user:password@db:port/db_name**
   
