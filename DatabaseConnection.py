import json
import pymssql

with open('config.json') as config:
    configFile = json.load(config)

conn = pymssql.connect(
    server=f"{configFile['DatabaseEndPoint']}:{configFile['DatabasePort']}",
    user=configFile['DatabaseUsername'],
    password=configFile['DatabasePassword'],
    database=configFile['DatabaseName'],
    as_dict=True
)