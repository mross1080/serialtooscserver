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

ip = "127.0.0.1"
port = 7400

client = SimpleUDPClient(ip, port)  # Create client

import subprocess
def init_serial_connection():
     global ser
     port_name = '/dev/cu.usbmodem143111'
     try:
         ports = serial.tools.list_ports.comports()
         print(ports)
         for port in ports:
              print(port)
              if "COM" in port.device:
                   port_name = port.device
                   print("Found an Arduino!! Using {} for specified port\n\n".format(port_name))
         ser = Serial(port_name, 115200)  # Establish the connection on a specific port
         return ser
     except Exception as e:
         print(e)
         print("You've got the Arduino Editor Serial Monitor Open!!! Ya gotta close that puppy!")
         exit()

# Automated Method to find proper serial port
ser = init_serial_connection()



# print("Outputting Data to : " , output_file)
print("\n\n\n\nReading data ")
termination_status = False
first_line = True
while True:
    try:
        line = ser.readline().decode().strip(" ").strip("\n")
        print(line)
        print("sending osc ")
        if "ERROR" not in line:
            sensor_data = line.split(":")
            location_name = sensor_data[1]
            location_name = "plant1"
            plant_state = sensor_data[2]
            distance_to_plant = sensor_data[3]
            client.send_message("/{}/value/".format(location_name), "{} {}".format(plant_state,distance_to_plant))   # Send float message
            # client.send_message("/{}/value".format(location_name), distance_to_plant)   # Send float message



    except Exception as e:
        print(e)