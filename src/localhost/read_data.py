import os
import json

def check_data_format(file_name:str):
    file = open(file_name, 'r')
    line = file.readline()
    components = line.strip().split("|")
    names = ['rowkey','time','MAC','PCM','departAirport','airline','agent','country','request','response','error','errorCode','errorType','success','fail']
    jsonObject = json.dumps(dict(map(lambda i,j:(i,j), names, components)))
    print(jsonObject)
    file.close()

def write_smaller_data(input_file_name:str, output_file_name:str):
    input_file = open(input_file_name, 'r')
    output_file = open(output_file_name, 'w')
    
    line = input_file.readline()
    count = 0
    while line is not None and line != '' and count<100000:
        line = input_file.readline()
        output_file.write(line)
        count += 1
    print("we write",count,"records to a new file")
    input_file.close()
    output_file.close()
    
dir = os.getcwd()
print(dir)
file_name = dir+"/data/GDS_logs.txt"
smaller_file_name = dir+"/data/GDS_logs_small.txt"
# check_data_format(file_name)
# print("we have received",1,"messages")
write_smaller_data(file_name, smaller_file_name)
