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
thermostat_digital_twin_model_identifier = "dtmi:itri:cms:perceptor;1"
# device_info_digital_twin_model_identifier = "dtmi:azure:DeviceManagement:DeviceInformation;1"

# The device "TemperatureController" that is getting implemented using the above interfaces.
# This id can change according to the company the user is from
# and the name user wants to call this Plug and Play device
model_id = "dtmi:itri:cms:perceptor;1"

# the components inside this Plug and Play device.
# there can be multiple components from 1 interface
# component names according to interfaces following pascal case.
# device_information_component_name = "deviceInformation"

featureId = 17
randomMinValue = 0
randomMaxValue = 20
rpc_component_name_01 = 'percept-dt-001'
thermostat_1_component_name = rpc_component_name_01

SLEEPTIME = 30
PEOPLECOUNTName = 'pplcount'
PROPERTYALARM = 'CrowedAlarm' 
PROPERTYROOMID = 'featureId'
PROPERTYTIMESTAMP = 'timestamp'

COMMAND_WATCHTIME ="settimetowatch"
COMMAND_SLEEPTIME = "settimetosleep"

COMMAND_ADD = 'commandtoadd'
COMMAND_DEL = 'commandtodelete'
COMMAND_GET = 'getconfiguration'

SET_PROPERTY = [COMMAND_WATCHTIME,COMMAND_SLEEPTIME,COMMAND_ADD,COMMAND_DEL,COMMAND_GET]

# GLOBAL VARIABLES
THERMOSTAT_1 = None
THERMOSTAT_2 = None

IOTHUB_DEVICE_SECURITY_TYPE="connectionString"
IOTHUB_CONNECTION_STRING="HostName=your-iot-hub;SharedAccessKeyName=iothubowner;SharedAccessKey=your-iot-hub-key"
IOTHUB_DEVICE_CONNECTION_STRING_DEV="HostName=here-your-azure-iothub.net;DeviceId=your-device-id;SharedAccessKey=your-device-key;SharedAccessKeyName=iothubowner"

class Thermostat(object):
    def __init__(self, name, moving_win=10,running=False,roomid = 0):

        self.moving_window = moving_win
        self.records =[]# [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.records_ppl =[]
        self.index = 0
        self.pplThreshole = 5
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
        
    def putRecord(self,current_temp, particleid):
        if particleid == PEOPLECOUNTName:
            self.records_ppl.append(current_temp)
        
    
#####################################################
# TELEMETRY TASKS
async def send_telemetry_from_temp_controller(device_client, telemetry_msg, component_name=None):
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
    import time
    localtime = int(time.time()) 
    print('now local time now {} '.format(localtime))
    my_dict[PROPERTYTIMESTAMP] = localtime

    msg = pnp_helper.create_telemetry(my_dict,component_name)
    await device_client.send_message(msg)
    print("Sent configuration message {} {}".format(component_name,msg))
    await asyncio.sleep(1)

def rpc_payload(rpcSensor):
    # my_dict = {}
    # my_dict[PEOPLECOUNTName] = 0
    # my_dict[PROPERTYALARM] = -1
    # my_dict[PROPERTYROOMID]= rpcSensor.roomId
    import time
    localtime = int(time.time()) 
    print('now local time now {} '.format(localtime))
    # my_dict[PROPERTYTIMESTAMP] = localtime

    my_dict = {
                "NEURAL_NETWORK": [{
                    "label": "person",
                    "timestamp": localtime
                }]
            }
    print(my_dict)
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
                # THERMOSTAT_1.setThreshole(set_properytName, values)
                # print('threshole {} {}'.format(set_properytName,values))
            elif set_properytName.startswith('set'):
                values = int(method_request.payload)
                print('watch time {}'.format(values))
                # THERMOSTAT_1.setTime(set_properytName,values)
            elif set_properytName.startswith('command'):
                if (set_properytName == COMMAND_DEL):
                    my_dict = rpc_payload(THERMOSTAT_1)
                    print("here is {}".format(my_dict))
                values = int(method_request.payload)
                print('set fun {}'.format(set_properytName))
                # THERMOSTAT_1.setRunning(set_properytName,values)
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
        digital_twin_client = DigitalTwinClient(IOTHUB_CONNECTION_STRING)
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
    #await device_client.connect()
   
    ################################################
    # Get all the listeners running
    print("Listening for command requests and property updates")
    global THERMOSTAT_1
    THERMOSTAT_1 = Thermostat(thermostat_1_component_name, 10,True, featureId)
    listeners = asyncio.gather(
        device_method_listener01(device_client),
    )
    
    if THERMOSTAT_1.run :
        await send_telemetry_configuration(THERMOSTAT_1, device_client,thermostat_1_component_name)
    
    ################################################
    # Function to send telemetry every 8 seconds
    async def send_telemetry():
        print("Sending telemetry from various components")
        while True:
            my_dict= {}
            if(THERMOSTAT_1.run):
                # curr_temp_ext = random.randrange(randomMinValue, randomMaxValue)
                # THERMOSTAT_1.putRecord(curr_temp_ext,PEOPLECOUNTName)
                # my_dict[PEOPLECOUNTName] = curr_temp_ext
                randomNo = random.randrange(randomMinValue, randomMaxValue)
                print('randomNo %d' % randomNo)
                import time
                localtime = int(time.time()) 
                personList = []
                for i in range(0, randomNo):
                    personList.append({
                        "label": "person",
                        "timestamp": localtime
                    })
                my_dict = {
                        "NEURAL_NETWORK": personList
                    }
 
                res = not bool(my_dict) 
                if not res :
                    # my_dict[PROPERTYALARM] = 0
                    # my_dict[PROPERTYROOMID]=THERMOSTAT_1.roomId

                    await send_telemetry_from_temp_controller(
                        device_client, my_dict, thermostat_1_component_name
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

    listeners.cancel()

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
