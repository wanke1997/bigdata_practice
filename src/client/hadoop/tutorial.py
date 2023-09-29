from hdfs import *
from json import dumps

client = Client("http://namenode:9870")


# create a file or directory
client.delete("/test",recursive=True)
client.makedirs('/test',permission=777)
print("INFO: the directory is created")

# client.makedirs('/test',permission=777)
res = client.list("/test")
print(res)

# upload a file
# client.upload("/test", "/data/benda.txt")


# create a file
# client.write("/test/hello.txt", data="hello world")
# res = client.list("/test")
# print(res)

# delete a file or directory
# client.delete("/test",recursive=True)
# res = client.list("/")
# print(res)

# create a json file
records = [
  {'name': 'foo', 'weight': 1},
  {'name': 'bar', 'weight': 2},
]
client.write('/test/records.jsonl', data=dumps(records), encoding='utf-8')

res = client.list("/test")
print(res)