'''
    Purpose of the program:
        The purpose of this program to prevent the disk to be full
        by occupying unnecessary disk space by a particular folder of a particular user on the server
            
        1- This program reads the json file having following fields 
            1.1- folder: a perticular folder
            1.2- quota: fixed size of disk space, a folder can occupy
            1.3- user: a list of emails to send alert msg to the user if the quota is exceeded
        2- check the size of all given folders and compare with the given quota
        3- if the size of folder's data exceeded, program will send the notification to the user

'''

import json
import subprocess 
import os 
import re
from send_mail import sendmail



def read_configuration(path, file_name):
    #read budget configuration file
    json_file = open(path+file_name) 
    
    #load json file
    json_data = json.load(json_file) 
    json_file.close() 

    return json_data




def get_storage_info(folder, quota, server_name, users):

    # command
    cmd = 'du -hs '+folder
    
    #run command
    output = subprocess.check_output(cmd, shell=True)
    
    # parse the output
    result_list = output.decode("utf-8").split()

    # calculate output size and unit from command output
    res = re.compile("([0-9]+)([a-zA-Z]+)")
    total_size_output = res.match(result_list[0])
    
    try:
        # if the output of command in the format ex. "20G"
        size_output = int(total_size_output.group(1))
        unit_output = total_size_output.group(2).strip()
    except:
        # if the output of command in the format ex. "20.2G" 
        split_by_dot = result_list[0].split('.')
        size_output = int(split_by_dot[0])
        unit_output = split_by_dot[1][-1]
       
    # calculate input size and unit from json data
    total_size_input = res.match(quota)
    size_input = int(total_size_input.group(1))
    unit_input = total_size_input.group(2).strip()


    # message and subject strings in order to send notification to the user
    subject = "ALERT | Storage Quota Exceeded | On "+server_name+" Server | "+folder
    msg = '''You have exceeded the user storage quota:
            
            Folder: {}
            Server Name: {}
            Your Quota: {}
            Your Current Folder Size: {}B'''.format(folder, server_name, quota, str(size_output)+unit_output)


    # condition to check if input and output folder size have the same units
    if ((unit_output == "M") and (unit_input[0] == "M")) or ((unit_output == "G") and (unit_input[0] == "G")):
        if (size_output > size_input):
            print("Quota Exceeded")
            sendmail(users, subject, msg)

    # condition to check if input and output folder size have different units
    elif (unit_output == "G") and (unit_input[0] == "M"):
        size_output = size_output * 1024
        if (size_output > size_input):
            print("Quota Exceeded")
            sendmail(users, subject, msg)
        


if __name__ == '__main__':

    # initialize json file and path by getting environment variables
    path = os.getenv("JSON_FILE_PATH")
    file_name = os.getenv("BUDGET_CONFIGURATION_JSON")
    server_name = os.getenv("SERVER_NAME")

    # get configuration data
    configuration_data = read_configuration(path, file_name)

    for item in range(len(configuration_data)):
        target_file_info = configuration_data[item]
        folder = target_file_info['folder']
        quota = target_file_info['quota']
        users = target_file_info['user']
        get_storage_info(folder, quota, server_name, users)
