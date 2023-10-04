import happybase

connection = happybase.Connection(host='hbase-master', port=9090)
connection.open()
connection.create_table(
    'mytable',
    {'cf1': dict(max_versions=10),
     'cf2': dict(max_versions=1, block_cache_enabled=False),
     'cf3': dict(),  # use defaults
    }
)
print(connection.tables())