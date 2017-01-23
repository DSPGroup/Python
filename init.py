########################################################################################################
# Script identification :: init Script                                                                ##
# This file makes all the initialization needed for the python environment to work properly.          ##
# This file is individual to every user, and should be changed for every test purpose, with mark on   ##
# the FOLRDER_NAME and TEST_NAME defines, LAB equipment addresses, modules being imported, etc.       ##
# Author : Bar Kristal                                                                                ##
# Start Date : 18/12/16                                                                               ##
########################################################################################################


#######################################################################################
### home-made modules:
######################
execfile(r"C:\new_python_infrastructure\devices.py")
execfile(r"C:\new_python_infrastructure\utilities.py")
execfile(r"C:\new_python_infrastructure\lab_equipment.py")


#######################################################################################
### standard modules:
#####################
import sys
import serial       # for the RS232 function
import time         # for the time and sleep command
import datetime     # for revived the windows time signature  
import binascii     # for convert from UART answer to bin
import os           #for the make dir option
import shlex
import shutil
import winsound     # for running audio files
import socket       # for tcp/ip connection with Termotron
import ctypes       # module for C data types
import enum         # module for C data types
import subprocess   # module to create an additional process
import psutil
import visa         # for controlling GPIB devices. (this module takes long time to load, so load it only if necessary)
#import openpyxl     # Excel library.  (this module takes long time to load, so load it only if necessary)
import decimal


#Test1 path:
FOLDER_PATH = r"C:\new_python_infrastructure\Tests\functionality_test"
FOLDER_NAME = "Log"
FOLDER_DATE = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
DIR_NAME = os.path.join(FOLDER_PATH , FOLDER_NAME , FOLDER_DATE)
TEST_NAME = "test1"


#########################################
#####     Log
#########################################

TEST_DATE = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
TEST_TIME = datetime.datetime.strftime(datetime.datetime.now(), '%H-%M-%S')
LOG_NAME = TEST_NAME + r"_" + TEST_DATE + r"_" + TEST_TIME + r".txt"
LOG_NAME_EXCEL = TEST_NAME + r"_" + TEST_DATE + r"_" + TEST_TIME + r".xlsx" 


#open a new log
open_log(DIR_NAME, LOG_NAME)
############################################################################################





# this variable need to be sent as an argument when defining a new Lab_Equipment device 
RESOURCE_MANAGER = visa.ResourceManager()

############################################################################################
##### defines: 
#############

T32_APP_CMM_PATH = r"T:\\Barkristal\DVF101\SPI\scripts\dvf101_app.cmm"
POWER_SUPPLY_FOR_RESET = ["GPIB0::29::INSTR", 2] #(addres, channel)

#lab_equipment GPIB addresses:
POWER_SUPLLY_ADDRESS = "GPIB0::29::INSTR"
DMM_ADDRESS = "GPIB0::22::INSTR"
FREQUENCY_COUNTER_ADDRESS = "GPIB0::27::INSTR"
WAVE_GENERATOR_ADDRESS = "GPIB0::1::INSTR"
ELECTRONIC_LOAD = "GPIB0::3::INSTR"

#TCP_IP addresses:
#TERMOTRON_TCP_IP =  ("172.19.5.237" ,8080)  # (ip, port) , (Sas)
TERMOTRON_TCP_IP =  ("172.19.5.240" ,8080)  # (ip, port) , (Ronny)
#############################################################################################

