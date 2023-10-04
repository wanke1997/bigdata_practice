import happybase

hbase_host = 'hbase-master'
hbase_port = 9090
hbase_table = 'bigdata_table'

# connect to HBase
connection = happybase.Connection(
    host=hbase_host, 
    port=hbase_port, 
    autoconnect=False,
)
connection.open()

# connect to a table
table = connection.table(hbase_table)

# print all rows
print(type(table.scan()))
cnt = 0
for row_idx, cf in table.scan():
    # print(len(cf.items()))
    cnt += 1
    for col_key, col_value in cf.items():
        col_key_str = col_key.decode('utf-8')
        col_value_str = col_value.decode('utf-8')
        print("row:",row_idx.decode('utf-8'),"col_key:",col_key_str,"col_value:",col_value_str)
print("total:",cnt)

# list all tables
print("all tables:", connection.tables())