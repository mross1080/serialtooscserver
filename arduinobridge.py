# -*- coding: utf-8 -*-

#pip install pyserial
#pip install python-osc

from pythonosc.udp_client import SimpleUDPClient

ip = "127.0.0.1"
port = 1337
import argparse
from time import sleep
import time
from serial import Serial
import os
import serial.tools.list_ports
from numpy import interp, clip
ip = "127.0.0.1"
port = 7400

client = SimpleUDPClient(ip, port)  # Create client

import subprocess
def init_serial_connection():
    global ser
    port_name = '/dev/cu.usbmodem143111'
     
    ports = serial.tools.list_ports.comports()
    print(ports)
    for port in ports:    
        print(port.description)
        print(port.device)
    for port in ports:
        try:
            print(port.description)
            print(port.device)
            if "COM" in port.description and "USB-SERIAL" in port.description:
                port_name = port.device
                print("Found an Arduino!! Using {} for specified port\n\n".format(port_name))
                ser = Serial(port_name, 115200)  # Establish the connection on a specific port
                return ser
        except Exception as e:
            print(e)
            print("Selecting a different arduino current selected in use ")
    

# Automated Method to find proper serial port
ser = init_serial_connection()



# print("Outputting Data to : " , output_file)
print("\n\n\n\nReading data ")
termination_status = False
first_line = True
while True:
    try:
        line = ser.readline().decode().strip(" ").strip("\n")

        if "ERROR" not in line and line != "":
            print(line)
            print("sending osc ")
            sensor_data = line.split(":")
            if (len(line.split(":"))) == 3:
                location_name = sensor_data[0]
                print("loc ", location_name)

                plant_state = sensor_data[3]
                touch_value = 0
                if plant_state == "TOUCH":
                    touch_value = 1
                distance_to_plant = sensor_data[2]
                distance_to_plant = clip(float(distance_to_plant), 0, 180)

                mapped_distance = interp(distance_to_plant, [0,180], [0,1])
                mapped_distance = float(format(mapped_distance, '.3f'))

                print("Distance mapped " , mapped_distance)
                combined_value = (str(mapped_distance) + " " + str(touch_value))
                client.send_message("/{}/value/".format(location_name),combined_value)   # Send float message



    except Exception as e:
        print(e)