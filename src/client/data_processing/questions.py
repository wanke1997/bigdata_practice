from pyspark.sql import SparkSession
import happybase

# hbase parameters
hbase_host = 'hbase-master'
hbase_port = 9090
hbase_table = 'bigdata_table'
app_name = "data_processing"

# methods are defined here
def tutorial(sparkContext):
    rdd = sparkContext.parallelize([1,2,3,4,5,6])
    file.write("rdd in string: "+str(rdd)+"\n")
    res = rdd.collect()
    file.write("rdd.collect() in string: "+str(res)+"\n")
    res = rdd.reduce(lambda x,y:x+y)
    file.write("reduce result:"+str(res)+"\n")

def retrieve_data(sparkContext):
    connection = happybase.Connection(
        host=hbase_host, 
        port=hbase_port, 
        autoconnect=False,
    )
    connection.open()
    # connect to a table
    table = connection.table(hbase_table)
    # scan the table
    cnt = 0
    dataset = []
    for _, cf in table.scan():
        cnt += 1
        data = (
            cf[b"basic:time"].decode("utf-8"),
            cf[b"connection:request"].decode("utf-8"),
            cf[b"connection:response"].decode("utf-8"),
            cf[b"property:departAirport"].decode("utf-8"),
            int(cf[b"status:success"].decode("utf-8")),
            int(cf[b"status:fail"].decode("utf-8")),
        )
        dataset.append(data)
    file.write("length of dataset:"+str(len(dataset))+"\n")
    connection.close()

    rdd = sparkContext.parallelize(dataset)
    return rdd

def Q1(rdd, time_range:str, start_time:str):
    if time_range=="day" and len(start_time)==8 or time_range=="hour" and len(start_time)==10:
        time_length = len(start_time)
        rdd2 = rdd.filter(lambda x:x[0].startswith(start_time))\
                .map(lambda x:(x[0][:time_length],x[1],x[3]))\
                .map(lambda x:(x,1))
        res = rdd2.reduceByKey(lambda x,y:x+y).sortBy(lambda x:-x[1]).collect()
        file.write("Q1 answer:\n")
        for line in res:
            file.write(str(line)+"\n")
        file.write("\n")
    else:
        file.write("Q1 ERROR: illegal time_range input\n")

def Q2(rdd, time_range:str, start_time:str, request:str):
    if time_range=="day" and len(start_time)==8 or time_range=="hour" and len(start_time)==10:
        time_length = len(start_time)
        success = rdd.filter(lambda x:x[0].startswith(start_time))\
                  .filter(lambda x:x[1]==request)\
                  .filter(lambda x:x[4]==1)\
                  .map(lambda x:((x[0][:time_length],x[1],x[2]),1))\
                  .reduceByKey(lambda x,y:x+y)
        
        fail = rdd.filter(lambda x:x[0].startswith(start_time))\
                  .filter(lambda x:x[1]==request)\
                  .filter(lambda x:x[5]==1)\
                  .map(lambda x:((x[0][:time_length],x[1],x[2]),1))\
                  .reduceByKey(lambda x,y:x+y)

        cogrouped = success.cogroup(fail)
        res = cogrouped.mapValues(lambda x: (list(x[0]), list(x[1])))\
              .map(lambda x:(x[0],([0], x[1][1])) if len(x[1][0])==0 else x)\
              .map(lambda x:(x[0],(x[1][0], [0])) if len(x[1][1])==0 else x)\
              .map(lambda x:(x[0],x[1][0][0],x[1][1][0],x[1][0][0]/(x[1][0][0]+x[1][1][0])))\
              .sortBy(lambda x:-x[3])\
              .collect()
        file.write("Q2 answer:\n")
        for line in res:
            file.write(str(line)+"\n")
        file.write("\n")
    else:
        file.write("Q2 ERROR: illegal input\n")

def Q3(rdd):
    # 3.1. find five airlines who made most requests
    rdd2 = rdd.map(lambda x:(x[1],1))
    res = rdd2.reduceByKey(lambda a,b:a+b).sortBy(lambda x:-x[1]).collect()
    file.write("Q3.1 answer:\n")
    for line in res:
        file.write(str(line)+"\n")
    file.write("\n")

    # 3.2. find five airlines who made the most SUCCESSFUL requests
    rdd2 = rdd.filter(lambda x:x[4]==1).map(lambda x:(x[1],1))
    res = rdd2.reduceByKey(lambda a,b:a+b).sortBy(lambda x:-x[1]).collect()
    file.write("Q3.2 answer:\n")
    for line in res:
        file.write(str(line)+"\n")
    file.write("\n")

    # 3.3. find five airlines who made the most FAILED requests
    rdd2 = rdd.filter(lambda x:x[5]==1).map(lambda x:(x[1],1))
    res = rdd2.reduceByKey(lambda a,b:a+b).sortBy(lambda x:-x[1]).collect()
    file.write("Q3.3 answer:\n")
    for line in res:
        file.write(str(line)+"\n")
    file.write("\n")

if __name__ == "__main__":
    # config spark
    spark = SparkSession \
        .builder \
        .appName(app_name) \
        .config("spark.executor.memory", "7g")\
        .getOrCreate()
    sparkContext = spark.sparkContext

    # define output files
    file_name = "spark_output.txt"
    file = open(file_name, "w")
    file.write("################################################################\n")

    # tutorial
    # tutorial(sparkContext)

    # get rdd
    rdd = retrieve_data(sparkContext)

    # answer Q1
    # time_range = "day"
    # start_time = "20190423"

    time_range = "hour"
    start_time = "2019042312"
    Q1(rdd,time_range=time_range,start_time=start_time)

    # answer Q2
    # time_range = "day"
    # start_time = "20190423"
    # request = "1P"

    time_range = "hour"
    start_time = "2019042312"
    request = "1P"
    Q2(rdd, time_range=time_range, start_time=start_time, request=request)

    # answer Q3
    Q3(rdd)

    file.write("################################################################\n")
    file.close()