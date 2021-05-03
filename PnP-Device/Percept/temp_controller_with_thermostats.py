# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import os
import asyncio
import random
import logging
import json
import math

from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device.aio import ProvisioningDeviceClient
from datetime import timedelta, datetime
from azure.iot.device import Message, MethodResponse,MethodRequest
from azure.iot.hub import DigitalTwinClient
import pnp_helper
import threading

logging.basicConfig(level=logging.ERROR)

# the interfaces that are pulled in to implement the device.
# User has to know these values as these may change and user can
# choose to implement different interfaces.
thermostat_digital_twin_model_identifier = "dtmi:itri:cms:RPCstat;1"
# device_info_digital_twin_model_identifier = "dtmi:azure:DeviceManagement:DeviceInformation;1"

# The device "TemperatureController" that is getting implemented using the above interfaces.
# This id can change according to the company the user is from
# and the name user wants to call this Plug and Play device
model_id = "dtmi:itri:cms:RPCstat;8"

# the components inside this Plug and Play device.
# there can be multiple components from 1 interface
# component names according to interfaces following pascal case.
# device_information_component_name = "deviceInformation"
# rpc_component_name_01 = 'levanlin-rpc-12-01-001'
# rpc_component_name_02 = 'rpc-11-03-002'
# rpc_component_name_03 = 'rpc-11-03-003'
# rpc_component_name_04 = 'rpc-11-03-004'
rpc_component_name_01 = 'rpc-t-1219-001'
# rpc_component_name_01 = 'rpc-t-1215-001'
rpc_component_name_02 = 'rpc-t-1215-002'
rpc_component_name_03 = 'rpc-t-1215-003'
rpc_component_name_04 = 'rpc-t-1215-004'
thermostat_1_component_name = rpc_component_name_01
thermostat_2_component_name = rpc_component_name_02
thermostat_3_component_name = rpc_component_name_03
thermostat_4_component_name = rpc_component_name_04

SLEEPTIME = 5
PARTICLE5umName = '5um'
PARTICLE3umName ='3um'
PARTICLE1umName ='1um'
PARTICLE05umName='05um'

PROPERTY5UM = 'particle5um'
PROPERTY3UM = 'particle3um'
PROPERTY1UM = 'particle1um'
PROPERTY05UM = 'particle05um'
PROPERTYALARM = 'rpcAlarm' 

PROPERTY5THRESHOLE = 'threshole5um'
PROPERTY3THRESHOLE = 'threshole3um'
PROPERTY1THRESHOLE = 'threshole1um'
PROPERTY05THRESHOLE = 'threshole05um'
PROPERTYWATCHTIME = 'timetowatch'
PROPERTYSLEEPTIME = 'timetosleep'
PROPERTYROOMID = 'featureId'
PROPERTYTIMESTAMP = 'timestamp'

COMMAND_WATCHTIME ="settimetowatch"
COMMAND_SLEEPTIME = "settimetosleep"

COMMAND_ADD = 'commandtoadd'
COMMAND_DEL = 'commandtodelete'
COMMAND_GET = 'getconfiguration'

SET_PROPERTY = [PROPERTY5THRESHOLE, PROPERTY3THRESHOLE,PROPERTY1THRESHOLE,PROPERTY05THRESHOLE, \
    COMMAND_WATCHTIME,COMMAND_SLEEPTIME,COMMAND_ADD,COMMAND_DEL,COMMAND_GET]

# serial_number = "alohomora"
#####################################################
# COMMAND HANDLERS : User will define these handlers
# depending on what commands the component defines

#####################################################
# GLOBAL VARIABLES
THERMOSTAT_1 = None
THERMOSTAT_2 = None

IOTHUB_DEVICE_SECURITY_TYPE="connectionString"
# IOTHUB_DEVICE_CONNECTION_STRING_DEV="HostName=levanlin-adt-iothub.azure-devices.net;DeviceId=levanlin-rpc-12-01-001;SharedAccessKey=Bxs2uLz1qYY0peFdfyaD7W/fzuX3E1rJuTP7aTZNQpQ="
# IOTHUB_DEVICE_CONNECTION_STRING_DEV2="HostName=levanlin-adt-iothub.azure-devices.net;DeviceId=rpc-11-03-002;SharedAccessKey=JgiWWWtnejuxISUJvvKAz7J29zl42P4jy9bDmePJcvQ="
# IOTHUB_DEVICE_CONNECTION_STRING_DEV3="HostName=levanlin-adt-iothub.azure-devices.net;DeviceId=rpc-11-03-003;SharedAccessKey=2Lek/xU4cYF79J7qTq7Dp97CRtARi6LOEKdvSHiI5Sw="
# IOTHUB_DEVICE_CONNECTION_STRING_DEV4="HostName=levanlin-adt-iothub.azure-devices.net;DeviceId=rpc-11-03-004;SharedAccessKey=dzIH1t3b5lQRFdm2738bJ/C2NaRkFLtSPtqXvSgG7aU=" 

######## archer ########################
IOTHUB_DEVICE_CONNECTION_STRING_DEV="HostName=levanlin-adt-iothub.azure-devices.net;SharedAccessKeyName=iothubowner;SharedAccessKey=wGPJkNKHb6LC1oKfDOt3XV4j8jKxXQborTmUowvwUTk="
# IOTHUB_DEVICE_CONNECTION_STRING_DEV="HostName=levanlin-adt-iothub.azure-devices.net;DeviceId=rpc-t-1215-001;SharedAccessKey=P0vy0kYIuYHn5MVUKkPzokhP+orLmz84QF6fGXw9RhQ="
IOTHUB_DEVICE_CONNECTION_STRING_DEV2="HostName=levanlin-adt-iothub.azure-devices.net;DeviceId=rpc-t-1215-002;SharedAccessKey=aT0lHCQE9SmmpnEWnY7vQn3wiUNaTRlwIusiFBPySOU="
IOTHUB_DEVICE_CONNECTION_STRING_DEV3="HostName=levanlin-adt-iothub.azure-devices.net;DeviceId=rpc-t-1215-003;SharedAccessKey=7KRT2Hu7mLQ0MYksIA+EZ6yl6z0H0wTBkjApP0LL3vM="
IOTHUB_DEVICE_CONNECTION_STRING_DEV4="HostName=levanlin-adt-iothub.azure-devices.net;DeviceId=rpc-t-1215-004;SharedAccessKey=iCLIWRS7Ku6uFCaN3IOG9YA5g4elidkpX4OJlKNyE7k="


SLEEPTIME = 5
# serial_number = "alohomora"
#####################################################
# COMMAND HANDLERS : User will define these handlers
# depending on what commands the component defines

#####################################################
# GLOBAL VARIABLES
THERMOSTAT_1 = None
THERMOSTAT_2 = None

class Thermostat(object):
    def __init__(self, name, moving_win=10,running=False,roomid = 0):

        self.moving_window = moving_win
        self.records =[]# [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.records_5um =[]
        self.records_3um=[]
        self.records_1um = []
        self.records_05um =[]
        self.index = 0
        self.um5Threshole = 50000
        self.um3Threshole = 50000
        self.um1Threshole = 50000
        self.um05Threshole= 50000
        self.cur = 0
        self.max = 0
        self.min = 0
        self.avg = 0
        self.run = running
        self.name = name
        self.watchTime = 10
        self.sleepTime = 5
        self.roomId = roomid
      
    def setRunning(self, id,value):
        # print('set rpc mode {} running {} '.format(id , self.run))
        if id ==  COMMAND_ADD and self.run == False:
            self.run = True
            self.roomId = value
        elif id == COMMAND_DEL and self.run == True:
            self.run = False
            self.roomId = 0
       
    def setTime(self, id, values):
        # print('set time id {} values {}'.format(id, values))
        if id == COMMAND_WATCHTIME :
            self.watchTime = values
        elif id == COMMAND_SLEEPTIME:
            self.sleepTime= values

    def setThreshole(self,id, values):
        # print('threshole id {} values {}'.format(id, values))
        if id == PROPERTY5THRESHOLE:
            self.um5Threshole = values
        elif id == PROPERTY3THRESHOLE:
            self.um3Threshole = values
        elif id == PROPERTY1THRESHOLE:
            self.um1Threshole = values
        elif id == PROPERTY05THRESHOLE:
            self.um05Threshole = values
        
    def putRecord(self,current_temp, particleid):
        if particleid == PARTICLE5umName:
            self.records_5um.append(current_temp)
            # print('size 5um {}'.format(len(self.records_5um)))
        elif particleid == PARTICLE3umName:
            self.records_3um.append(current_temp)
            # print('size 3um {}'.format(len(self.records_3um)))
        elif particleid == PARTICLE1umName:
            self.records_1um.append(current_temp)
            # print('size 1um {}'.format(len(self.records_1um)))
        elif particleid == PARTICLE05umName:
            self.records_05um.append(current_temp)
            # print('size 05um {}'.format(len(self.records_05um)))

    def calculate_rpc_average(self,particleid):
        if particleid == PARTICLE5umName and len(self.records_5um) >= self.watchTime:
            avg = sum(self.records_5um) / len(self.records_5um)
            # print('avg {} size 5um {}'.format(avg,len(self.records_5um)))
            self.records_5um.clear()
            return math.ceil(avg)
        elif particleid == PARTICLE3umName and len(self.records_3um) >= self.watchTime:
            avg = sum(self.records_3um) / len(self.records_3um)
            # print('avg {} size 3um {}'.format(avg,len(self.records_3um)))
            self.records_3um.clear()
            return math.ceil(avg)
        elif particleid == PARTICLE1umName and len(self.records_1um) >= self.watchTime:
            avg = sum(self.records_1um) / len(self.records_1um)
            # print('avg {} size 1 um {}'.format(avg,len(self.records_1um)))
            self.records_1um.clear()
            return math.ceil(avg)
        elif particleid == PARTICLE05umName and len(self.records_05um) >= self.watchTime:
            avg = sum(self.records_05um) / len(self.records_05um)
            # print('avg {} size 05um {}'.format(avg,len(self.records_05um)))
            self.records_05um.clear()
            return math.ceil(avg)

#     def record(self, current_temp):
#         self.cur = current_temp
#         self.records[self.index] = current_temp
#         self.max = self.calculate_max(current_temp)
#         self.min = self.calculate_min(current_temp)
#         self.avg = self.calculate_average()

#         self.index = (self.index + 1) % self.moving_window

#     def calculate_max(self, current_temp):
#         if not self.max:
#             return current_temp
#         elif current_temp > self.max:
#             return self.max

#     def calculate_min(self, current_temp):
#         if not self.min:
#             return current_temp
#         elif current_temp < self.min:
#             return self.min

#     def calculate_average(self):
#         return sum(self.records) / len(self.record) #self.moving_window

#     def create_report(self):
#         response_dict = {}
#         response_dict["maxTemp"] = self.max
#         response_dict["minTemp"] = self.min
#         response_dict["avgTemp"] = self.avg
#         response_dict["startTime"] = (
#             datetime.now() - timedelta(0, self.moving_window * 8)
#         ).isoformat()
#         response_dict["endTime"] = datetime.now().isoformat()
#         return response_dict

# END COMMAND HANDLERS
#####################################################
#####################################################
# CREATE RESPONSES TO COMMANDS


#def create_max_min_report_response(thermostat_name):
    # """
    # An example function that can create a response to the "getMaxMinReport" command request the way the user wants it.
    # Most of the times response is created by a helper function which follows a generic pattern.
    # This should be only used when the user wants to give a detailed response back to the Hub.
    # :param values: The values that were received as part of the request.
    # """
    # if "Thermostat;1" in thermostat_name and THERMOSTAT_1:
    #     response_dict = THERMOSTAT_1.create_report()
    # elif THERMOSTAT_2:
    #     response_dict = THERMOSTAT_2.create_report()
    # else:  # This is done to pass certification.
    #     response_dict = {}
    #     response_dict["maxTemp"] = 0
    #     response_dict["minTemp"] = 0
    #     response_dict["avgTemp"] = 0
    #     response_dict["startTime"] = datetime.now().isoformat()
    #     response_dict["endTime"] = datetime.now().isoformat()

    # response_payload = json.dumps(response_dict, default=lambda o: o.__dict__, sort_keys=True)
    # print(response_payload)
    # return response_payload


# END CREATE RESPONSES TO COMMANDS
#####################################################

#####################################################
# TELEMETRY TASKS
async def send_telemetry_from_temp_controller(device_client, telemetry_msg, component_name=None):
    # from datetime import timezone
    # # dt_now = datetime.now(tz=timezone.utc)
    # dt_ts = datetime.fromtimestamp(1571595618.0, tz=timezone.utc)
    # utc = int(unix_time(dt_ts) * 1000)
    # # telemetry_msg[PROPERTYTIMESTAMP] = dt_now
    # print('now local time now {} {}'.format(dt_ts,utc))
    import time
    localtime = int(time.time()) 
    print('now local time now {} '.format(localtime))
    telemetry_msg[PROPERTYTIMESTAMP] = localtime

    msg = pnp_helper.create_telemetry(telemetry_msg, component_name)
    await device_client.send_message(msg)
    print("Sent message {} {}".format(component_name,msg))
    await asyncio.sleep(SLEEPTIME)

async def send_telemetry_configuration(rpcSensor, device_client, component_name=None):
    my_dict = {}
    my_dict[PROPERTY5THRESHOLE] = rpcSensor.um5Threshole
    my_dict[PROPERTY3THRESHOLE] = rpcSensor.um3Threshole
    my_dict[PROPERTY1THRESHOLE] = rpcSensor.um1Threshole
    my_dict[PROPERTY05THRESHOLE] = rpcSensor.um05Threshole
    my_dict[PROPERTYWATCHTIME] = rpcSensor.watchTime
    my_dict[PROPERTYSLEEPTIME] = rpcSensor.sleepTime
    my_dict[PROPERTYROOMID]= rpcSensor.roomId
    # from datetime import timezone
    # # //dt_now = datetime.now(tz=timezone.utc)
    # dt_ts = datetime.fromtimestamp(1571595618.0, tz=timezone.utc)
    # utc = int(unix_time(dt_ts) * 1000)
    # print('now local time now {} {}'.format(dt_ts,utc))
    import time
    localtime = int(time.time()) 
    print('now local time now {} '.format(localtime))
    my_dict[PROPERTYTIMESTAMP] = localtime
    

    msg = pnp_helper.create_telemetry(my_dict,component_name)
    await device_client.send_message(msg)
    print("Sent configuration message {} {}".format(component_name,msg))
    await asyncio.sleep(1)

def rpc_payload(rpcSensor):
    my_dict = {}
    my_dict[PROPERTY5UM] = 0
    my_dict[PROPERTY3UM] = 0
    my_dict[PROPERTY1UM] = 0
    my_dict[PROPERTY05UM] = 0
    my_dict[PROPERTYALARM] = -1
    my_dict[PROPERTYROOMID]= rpcSensor.roomId
    import time
    localtime = int(time.time()) 
    print('now local time now {} '.format(localtime))
    my_dict[PROPERTYTIMESTAMP] = localtime
    # from datetime import timezone
    # # dt_now = datetime.now(tz=timezone.utc)
    # dt_ts = datetime.fromtimestamp(1571595618.0, tz=timezone.utc)
    # utc = int(unix_time(dt_ts) * 1000)
    # # my_dict[PROPERTYTIMESTAMP] = dt_now
    # print('rpc _payload now local time now {} {}'.format(dt_ts,utc))
    return my_dict


#####################################################
# COMMAND TASKS
async def device_method_listener01(device_client):
   
    while True:
        my_dict = {}
        method_request = await device_client.receive_method_request()
        # print("receive command request {}".format(method_request))
        print (
            "\nMethod callback called with:\nmethodName = {method_name}\npayload = {payload}".format(
                method_name=method_request.name,
                payload=method_request.payload
            )
        )
        set_properytName = method_request.name 
        if set_properytName not in SET_PROPERTY:
            response_payload = {"Response": "{} not found property & command".format(set_properytName)}
            response_status = 403
            method_response = MethodResponse(method_request.request_id, response_status, payload=response_payload)
            await device_client.send_method_response(method_response)
            continue
        try:
            if set_properytName.startswith('threshole') :
                values = int(method_request.payload)
                THERMOSTAT_1.setThreshole(set_properytName, values)
                # print('threshole {} {}'.format(set_properytName,values))
            elif set_properytName.startswith('set'):
                values = int(method_request.payload)
                print('watch time {}'.format(values))
                THERMOSTAT_1.setTime(set_properytName,values)
            elif set_properytName.startswith('command'):
                if (set_properytName == COMMAND_DEL):
                    my_dict = rpc_payload(THERMOSTAT_1)
                    print("here is {}".format(my_dict))
                values = int(method_request.payload)
                print('set fun {}'.format(set_properytName))
                THERMOSTAT_1.setRunning(set_properytName,values)
            elif set_properytName.startswith('get'):
                pass
                # await send_telemetry_configuration(THERMOSTAT_1,device_client,THERMOSTAT_1.name)
        except ValueError:
            response_payload = {"Response": "Invalid parameter"}
            response_status = 400
        
        response_payload = {"Response": "Executed direct method {}".format(method_request.name)}
        response_status = 200
        method_response = MethodResponse(method_request.request_id, response_status, payload=response_payload)
        await device_client.send_method_response(method_response)
        if(set_properytName == COMMAND_DEL):
            print("here is againg {}".format(my_dict))
            await send_telemetry_from_temp_controller(device_client, my_dict, THERMOSTAT_1.name)
        else:
            await send_telemetry_configuration(THERMOSTAT_1,device_client,THERMOSTAT_1.name)

async def device_method_listener02(device_client):

    while True:
        my_dict = {}
        method_request = await device_client.receive_method_request()
        # print("receive command request {}".format(method_request))
        print (
            "\nMethod callback called with:\nmethodName = {method_name}\npayload = {payload}".format(
                method_name=method_request.name,
                payload=method_request.payload
            )
        )
        set_properytName = method_request.name 
        if set_properytName not in SET_PROPERTY:
            response_payload = {"Response": "{} not found property & command".format(set_properytName)}
            response_status = 403
            method_response = MethodResponse(method_request.request_id, response_status, payload=response_payload)
            await device_client.send_method_response(method_response)
            continue
        try:
            if set_properytName.startswith('threshole') :
                values = int(method_request.payload)
                THERMOSTAT_2.setThreshole(set_properytName, values)
                # print('threshole {} {}'.format(set_properytName,values))
            elif set_properytName.startswith('set'):
                values = int(method_request.payload)
                # print('watch time {}'.format(values))
                THERMOSTAT_2.setTime(set_properytName,values)
            elif set_properytName.startswith('command'):
                if (set_properytName == COMMAND_DEL):
                    my_dict = rpc_payload(THERMOSTAT_2)
                values = int(method_request.payload)
                THERMOSTAT_2.setRunning(set_properytName,values)
            elif set_properytName.startswith('get'):
                pass
                # await send_telemetry_configuration(THERMOSTAT_2,device_client,THERMOSTAT_2.name)
                

        except ValueError:
            response_payload = {"Response": "Invalid parameter"}
            response_status = 400
        
        response_payload = {"Response": "Executed direct method {}".format(method_request.name)}
        response_status = 200
        method_response = MethodResponse(method_request.request_id, response_status, payload=response_payload)
        await device_client.send_method_response(method_response)
        if(set_properytName == COMMAND_DEL):
            await send_telemetry_from_temp_controller(device_client, my_dict, THERMOSTAT_2.name)
        else:
            await send_telemetry_configuration(THERMOSTAT_2,device_client,THERMOSTAT_2.name)
                


async def device_method_listener03(device_client):
    while True:
        my_dict = {}
        method_request = await device_client.receive_method_request()
        # print("receive command request {}".format(method_request))
        print (
            "\nMethod callback called with:\nmethodName = {method_name}\npayload = {payload}".format(
                method_name=method_request.name,
                payload=method_request.payload
            )
        )
        set_properytName = method_request.name 
        if set_properytName not in SET_PROPERTY:
            response_payload = {"Response": "{} not found property & command".format(set_properytName)}
            response_status = 403
            method_response = MethodResponse(method_request.request_id, response_status, payload=response_payload)
            await device_client.send_method_response(method_response)
            continue
        try:
            if set_properytName.startswith('threshole') :
                values = int(method_request.payload)
                THERMOSTAT_3.setThreshole(set_properytName, values)
                # print('threshole {} {}'.format(set_properytName,values))
            elif set_properytName.startswith('set'):
                values = int(method_request.payload)
                # print('watch time {}'.format(values))
                THERMOSTAT_3.setTime(set_properytName,values)
            elif set_properytName.startswith('command'):
                values = int(method_request.payload)
                if (set_properytName == COMMAND_DEL):
                    my_dict = rpc_payload(THERMOSTAT_3)
                THERMOSTAT_3.setRunning(set_properytName,values)
            elif set_properytName.startswith('get'):
                pass
                # await send_telemetry_configuration(THERMOSTAT_3,device_client,THERMOSTAT_3.name)
        except ValueError:
            response_payload = {"Response": "Invalid parameter"}
            response_status = 400
        
        response_payload = {"Response": "Executed direct method {}".format(method_request.name)}
        response_status = 200
        method_response = MethodResponse(method_request.request_id, response_status, payload=response_payload)
        await device_client.send_method_response(method_response)
        if(set_properytName == COMMAND_DEL):
            await send_telemetry_from_temp_controller(device_client, my_dict, THERMOSTAT_3.name)
        else:
            await send_telemetry_configuration(THERMOSTAT_3,device_client,THERMOSTAT_3.name)

async def device_method_listener04(device_client):
    while True:
        my_dict = {}
        method_request = await device_client.receive_method_request()
        # print("receive command request {}".format(method_request))
        print (
            "\nMethod callback called with:\nmethodName = {method_name}\npayload = {payload}".format(
                method_name=method_request.name,
                payload=method_request.payload
            )
        )
        set_properytName = method_request.name 
        set_properytName = method_request.name 
        if set_properytName not in SET_PROPERTY:
            response_payload = {"Response": "{} not found property & command".format(set_properytName)}
            response_status = 403
            method_response = MethodResponse(method_request.request_id, response_status, payload=response_payload)
            await device_client.send_method_response(method_response)
            continue
        try:
            if set_properytName.startswith('threshole') :
                values = int(method_request.payload)
                THERMOSTAT_4.setThreshole(set_properytName, values)
                # print('threshole {} {}'.format(set_properytName,values))
            elif set_properytName.startswith('set'):
                values = int(method_request.payload)
                # print('watch time {}'.format(values))
                THERMOSTAT_4.setTime(set_properytName,values)
            elif set_properytName.startswith('command'):
                values = int(method_request.payload)
                if (set_properytName == COMMAND_DEL):
                    my_dict = rpc_payload(THERMOSTAT_4)
                THERMOSTAT_4.setRunning(set_properytName,values)
            elif set_properytName.startswith('get'):
                pass
                # await send_telemetry_configuration(THERMOSTAT_4,device_client,THERMOSTAT_4.name)
        except ValueError:
            response_payload = {"Response": "Invalid parameter"}
            response_status = 400
        
        response_payload = {"Response": "Executed direct method {}".format(method_request.name)}
        response_status = 200
        method_response = MethodResponse(method_request.request_id, response_status, payload=response_payload)
        await device_client.send_method_response(method_response)
        if(set_properytName == COMMAND_DEL):
            await send_telemetry_from_temp_controller(device_client, my_dict, THERMOSTAT_4.name)
        else:
            await send_telemetry_configuration(THERMOSTAT_4,device_client,THERMOSTAT_4.name)
#####################################################
# An # END KEYBOARD INPUT LISTENER to quit application

def stdin_listener():
    """
    Listener for quitting the sample
    """
    while True:
        selection = input("Press Q to quit\n")
        if selection == "Q" or selection == "q":
            print("Quitting...")
            break

#####################################################
# MAIN STARTS

async def main():
    switch = os.getenv("IOTHUB_DEVICE_SECURITY_TYPE")
    switch = IOTHUB_DEVICE_SECURITY_TYPE
    if switch == "connectionString":
        conn_str = IOTHUB_DEVICE_CONNECTION_STRING_DEV
        digital_twin_client = DigitalTwinClient(conn_str)
        digital_twin = digital_twin_client.get_digital_twin(rpc_component_name_01)
        if digital_twin:
            print(digital_twin)
            print("Model Id: " + digital_twin["$metadata"]["$model"])
        else :
            print('not digital twin found')
        device_client = IoTHubDeviceClient.create_from_connection_string(
             conn_str, product_info=model_id
        )
    else :
        raise RuntimeError(
            "At least one choice needs to be made for complete functioning of this sample."
        )
    # Connect the client.
    # await device_client.connect()

    if switch == "connectionString":
        conn_str =IOTHUB_DEVICE_CONNECTION_STRING_DEV2
        device_client2 = IoTHubDeviceClient.create_from_connection_string(
            conn_str, product_info=model_id
        )
    else :
        raise RuntimeError(
            "At least one choice needs to be made for complete functioning of this sample."
        )
    # Connect the client.
    await device_client2.connect()

    if switch == "connectionString":
        conn_str =IOTHUB_DEVICE_CONNECTION_STRING_DEV3
        device_client3 = IoTHubDeviceClient.create_from_connection_string(
            conn_str, product_info=model_id
        )
    else:
        raise RuntimeError(
            "At least one choice needs to be made for complete functioning of this sample."
        )
    await device_client3.connect()

    if switch == "connectionString":
        conn_str =IOTHUB_DEVICE_CONNECTION_STRING_DEV4
        device_client4 = IoTHubDeviceClient.create_from_connection_string(
            conn_str, product_info=model_id
        )
    else:
        raise RuntimeError(
            "At least one choice needs to be made for complete functioning of this sample."
        )

    # Connect the client.
    await device_client4.connect()

    ################################################
    # Get all the listeners running
    print("Listening for command requests and property updates")
    global THERMOSTAT_1
    global THERMOSTAT_2
    global THERMOSTAT_3
    global THERMOSTAT_4
    THERMOSTAT_1 = Thermostat(thermostat_1_component_name, 10,True)
    THERMOSTAT_2 = Thermostat(thermostat_2_component_name, 10,False)
    THERMOSTAT_3 = Thermostat(thermostat_3_component_name, 10,False)
    THERMOSTAT_4 = Thermostat(thermostat_4_component_name, 10,False)
    listeners = asyncio.gather(
        device_method_listener01(device_client),
        device_method_listener02(device_client2),
        device_method_listener03(device_client3),
        device_method_listener04(device_client4),
    )
    
    if THERMOSTAT_1.run :
        await send_telemetry_configuration(THERMOSTAT_1, device_client,thermostat_1_component_name)
    if THERMOSTAT_2.run :
        await send_telemetry_configuration(THERMOSTAT_2, device_client2,thermostat_2_component_name)
    if THERMOSTAT_3.run :
        await send_telemetry_configuration(THERMOSTAT_3, device_client3,thermostat_3_component_name)
    if THERMOSTAT_4.run :
        await send_telemetry_configuration(THERMOSTAT_4, device_client4,thermostat_4_component_name)
    
    ################################################
    # Function to send telemetry every 8 seconds

    async def send_telemetry():
        print("Sending telemetry from various components")
        while True:
            my_dict= {}
            if(THERMOSTAT_1.run):
                curr_temp_ext = random.randrange(0, 65535)
                THERMOSTAT_1.putRecord(curr_temp_ext,PARTICLE5umName)
                if(len(THERMOSTAT_1.records_5um) >= THERMOSTAT_1.watchTime):
                    avg = THERMOSTAT_1.calculate_rpc_average(PARTICLE5umName)
                    my_dict[PROPERTY5UM] = avg

                curr_temp_ext = random.randrange(0, 65535)
                THERMOSTAT_1.putRecord(curr_temp_ext,PARTICLE3umName)
                if(len(THERMOSTAT_1.records_3um) >= THERMOSTAT_1.watchTime):
                    avg = THERMOSTAT_1.calculate_rpc_average(PARTICLE3umName)
                    my_dict[PROPERTY3UM] = avg

                curr_temp_ext = random.randrange(0, 65535)
                THERMOSTAT_1.putRecord(curr_temp_ext,PARTICLE1umName)
                if(len(THERMOSTAT_1.records_1um) >= THERMOSTAT_1.watchTime):
                    avg = THERMOSTAT_1.calculate_rpc_average(PARTICLE1umName)
                    my_dict[PROPERTY1UM] = avg
                
                curr_temp_ext = random.randrange(0, 65535)
                THERMOSTAT_1.putRecord(curr_temp_ext,PARTICLE05umName)
                if(len(THERMOSTAT_1.records_05um) >= THERMOSTAT_1.watchTime):
                    avg = THERMOSTAT_1.calculate_rpc_average(PARTICLE05umName)
                    my_dict[PROPERTY05UM] = avg
                
                res = not bool(my_dict) 
                if not res :
                    if my_dict[PROPERTY5UM] > THERMOSTAT_1.um5Threshole or \
                        my_dict[PROPERTY3UM] > THERMOSTAT_1.um3Threshole or \
                        my_dict[PROPERTY1UM] > THERMOSTAT_1.um1Threshole or \
                        my_dict[PROPERTY05UM] > THERMOSTAT_1.um05Threshole :
                        my_dict[PROPERTYALARM] =  1
                    else :
                        my_dict[PROPERTYALARM] = 0

                    my_dict[PROPERTYROOMID]=THERMOSTAT_1.roomId

                    await send_telemetry_from_temp_controller(
                        device_client, my_dict, thermostat_1_component_name
                    )

            if(THERMOSTAT_2.run):
                curr_temp_ext = random.randrange(0, 65535)
                THERMOSTAT_2.putRecord(curr_temp_ext,PARTICLE5umName)
                if(len(THERMOSTAT_2.records_5um) >= THERMOSTAT_2.watchTime):
                    avg = THERMOSTAT_2.calculate_rpc_average(PARTICLE5umName)
                    my_dict[PROPERTY5UM] = avg

                curr_temp_ext = random.randrange(0, 65535)
                THERMOSTAT_2.putRecord(curr_temp_ext,PARTICLE3umName)
                if(len(THERMOSTAT_2.records_3um) >= THERMOSTAT_2.watchTime):
                    avg = THERMOSTAT_2.calculate_rpc_average(PARTICLE3umName)
                    my_dict[PROPERTY3UM] = avg

                curr_temp_ext = random.randrange(0, 65535)
                THERMOSTAT_2.putRecord(curr_temp_ext,PARTICLE1umName)
                if(len(THERMOSTAT_2.records_1um) >= THERMOSTAT_2.watchTime):
                    avg = THERMOSTAT_2.calculate_rpc_average(PARTICLE1umName)
                    my_dict[PROPERTY1UM] = avg
                
                curr_temp_ext = random.randrange(0, 65535)
                THERMOSTAT_2.putRecord(curr_temp_ext,PARTICLE05umName)
                if(len(THERMOSTAT_2.records_05um) >= THERMOSTAT_2.watchTime):
                    avg = THERMOSTAT_2.calculate_rpc_average(PARTICLE05umName)
                    my_dict[PROPERTY05UM] = avg

                res = not bool(my_dict) 

                if not res :
                    if my_dict[PROPERTY5UM] > THERMOSTAT_2.um5Threshole or  \
                    my_dict[PROPERTY3UM] > THERMOSTAT_2.um3Threshole or \
                    my_dict[PROPERTY1UM] > THERMOSTAT_2.um1Threshole or \
                    my_dict[PROPERTY05UM] > THERMOSTAT_2.um05Threshole :
                        my_dict[PROPERTYALARM] =  1
                    else :
                        my_dict[PROPERTYALARM] = 0

                    my_dict[PROPERTYROOMID]=THERMOSTAT_2.roomId

                    await send_telemetry_from_temp_controller(
                        device_client2, my_dict, thermostat_2_component_name
                    )
            
            if(THERMOSTAT_3.run):
                curr_temp_ext = random.randrange(0, 65535)
                THERMOSTAT_3.putRecord(curr_temp_ext,PARTICLE5umName)
                if(len(THERMOSTAT_3.records_5um) >= THERMOSTAT_3.watchTime):
                    avg = THERMOSTAT_3.calculate_rpc_average(PARTICLE5umName)
                    my_dict[PROPERTY5UM] = avg

                curr_temp_ext = random.randrange(0, 65535)
                THERMOSTAT_3.putRecord(curr_temp_ext,PARTICLE3umName)
                if(len(THERMOSTAT_3.records_3um) >= THERMOSTAT_3.watchTime):
                    avg = THERMOSTAT_3.calculate_rpc_average(PARTICLE3umName)
                    my_dict[PROPERTY3UM] = avg

                curr_temp_ext = random.randrange(0, 65535)
                THERMOSTAT_3.putRecord(curr_temp_ext,PARTICLE1umName)
                if(len(THERMOSTAT_3.records_1um) >= THERMOSTAT_3.watchTime):
                    avg = THERMOSTAT_3.calculate_rpc_average(PARTICLE1umName)
                    my_dict[PROPERTY1UM] = avg
                
                curr_temp_ext = random.randrange(0, 65535)
                THERMOSTAT_3.putRecord(curr_temp_ext,PARTICLE05umName)
                if(len(THERMOSTAT_3.records_05um) >= THERMOSTAT_3.watchTime):
                    avg = THERMOSTAT_3.calculate_rpc_average(PARTICLE05umName)
                    my_dict[PROPERTY05UM] = avg

                res = not bool(my_dict) 
                if not res :
                    if my_dict[PROPERTY5UM] > THERMOSTAT_3.um5Threshole or  \
                    my_dict[PROPERTY3UM] > THERMOSTAT_3.um3Threshole or \
                    my_dict[PROPERTY1UM] > THERMOSTAT_3.um1Threshole or \
                    my_dict[PROPERTY05UM] > THERMOSTAT_3.um05Threshole :
                        my_dict[PROPERTYALARM] =  1
                    else :
                        my_dict[PROPERTYALARM] = 0

                    my_dict[PROPERTYROOMID]=THERMOSTAT_3.roomId

                    await send_telemetry_from_temp_controller(
                        device_client3, my_dict, thermostat_3_component_name
                    )
            
            if(THERMOSTAT_4.run):
                curr_temp_ext = random.randrange(0, 65535)
                THERMOSTAT_4.putRecord(curr_temp_ext,PARTICLE5umName)
                if(len(THERMOSTAT_4.records_5um) >= THERMOSTAT_4.watchTime):
                    avg = THERMOSTAT_4.calculate_rpc_average(PARTICLE5umName)
                    my_dict[PROPERTY5UM] = avg

                curr_temp_ext = random.randrange(0, 65535)
                THERMOSTAT_4.putRecord(curr_temp_ext,PARTICLE3umName)
                if(len(THERMOSTAT_4.records_3um) >= THERMOSTAT_4.watchTime):
                    avg = THERMOSTAT_4.calculate_rpc_average(PARTICLE3umName)
                    my_dict[PROPERTY3UM] = avg

                curr_temp_ext = random.randrange(0, 65535)
                THERMOSTAT_4.putRecord(curr_temp_ext,PARTICLE1umName)
                if(len(THERMOSTAT_4.records_1um) >= THERMOSTAT_4.watchTime):
                    avg = THERMOSTAT_4.calculate_rpc_average(PARTICLE1umName)
                    my_dict[PROPERTY1UM] = avg
                
                curr_temp_ext = random.randrange(0, 65535)
                THERMOSTAT_4.putRecord(curr_temp_ext,PARTICLE05umName)
                if(len(THERMOSTAT_4.records_05um) >= THERMOSTAT_4.watchTime):
                    avg = THERMOSTAT_4.calculate_rpc_average(PARTICLE05umName)
                    my_dict[PROPERTY05UM] = avg

                res = not bool(my_dict) 
                if not res :
                    if my_dict[PROPERTY5UM] > THERMOSTAT_4.um5Threshole or  \
                    my_dict[PROPERTY3UM] > THERMOSTAT_4.um3Threshole or \
                    my_dict[PROPERTY1UM] > THERMOSTAT_4.um1Threshole or \
                    my_dict[PROPERTY05UM] > THERMOSTAT_4.um05Threshole :
                        my_dict[PROPERTYALARM] =  1
                    else :
                        my_dict[PROPERTYALARM] = 0

                    my_dict[PROPERTYROOMID]=THERMOSTAT_4.roomId

                    await send_telemetry_from_temp_controller(
                        device_client4, my_dict, thermostat_4_component_name
                    )
            await asyncio.sleep(1)
    send_telemetry_task = asyncio.ensure_future(send_telemetry())

    # Run the stdin listener in the event loop
    loop = asyncio.get_running_loop()
    user_finished = loop.run_in_executor(None, stdin_listener)
    # # Wait for user to indicate they are done listening for method calls
    await user_finished

    if not listeners.done():
        listeners.set_result("DONE")

    # # if not property_updates.done():
    # #     property_updates.set_result("DONE")

    listeners.cancel()
    # # property_updates.cancel()

    send_telemetry_task.cancel()

    # finally, disconnect
    await device_client.disconnect()


#####################################################
# EXECUTE MAIN

if __name__ == "__main__":
    asyncio.run(main())

    # If using Python 3.6 or below, use the following code instead of asyncio.run(main()):
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())
    # loop.close()
