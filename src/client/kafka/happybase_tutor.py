# ref: https://blog.csdn.net/weixin_35757704/article/details/123018548

import happybase


# connect to HBase
connection = happybase.Connection(
    host='hbase-master', 
    port=9090, 
    autoconnect=False,
)
connection.open()
print("connected to hbase")

# list all tables
print(connection.tables())

# create a table
if 'my_table'.encode('utf-8') not in connection.tables():
    print("I AM HERE")
    connection.create_table(
        'my_table',
        {
            'cf1': dict(),
            'cf2': dict(),
        }
    )

# connect to a table
table = connection.table('my_table')

# add and delete a row from table
table.put('row1', {'cf1:col_1':'a', 'cf2:col_1':'b'})
table.put('row2', {'cf1:col_1':'1', 'cf1:col_2':'2', 'cf2:col1':'c'})
table.delete('row2')

# print a row
row = table.row('row1')
for key in row.keys():
    print(key.decode('utf-8'), row[key].decode('utf-8'))
    
# print all rows
for row_idx, cf in table.scan():
    for col_key, col_value in cf.items():
        col_key_str = col_key.decode('utf-8')
        col_value_str = col_value.decode('utf-8')
        print("row:",row_idx.decode('utf-8'),"col_key:",col_key_str,"col_value:",col_value_str)

# delete a table
if 'my_table'.encode('utf-8') in connection.tables():
    connection.disable_table('my_table'.encode('utf-8'))
    connection.delete_table('my_table'.encode('utf-8'))
    print("deleted",connection.tables())