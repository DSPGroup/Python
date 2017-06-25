########################################################################################################
# Script identification :: init Script                                                                ##
# This file makes all the initialization needed for the python environment to work properly.          ##
# This file contains addresses and defines compatible to each user, when the selection of the user is ##
# taking place in the test file, by declarating the USER_NAME variable.                               ##
# Author : Bar Kristal                                                                                ##
# Start Date : 18/12/16                                                                               ##
########################################################################################################



### standard modules:
#####################
import sys
import serial       # for the RS232 function
import time         # for the time and sleep command
import datetime     # for revived the windows time signature  
import binascii     # for convert from UART answer to bin
import os           # for the make dir option
import shlex
import shutil
import winsound     # for running audio files
import socket       # for tcp/ip connection with Termotron
import ctypes       # module for C data types
import enum         # module for C data types
import subprocess   # module to create an additional process
import psutil
import visa         # for controlling GPIB devices. (this module takes long time to load, so load it only if necessary)
import openpyxl     # Excel library.  (this module takes long time to load, so load it only if necessary)
import decimal
import platform     # for the Laurebach initialization
# import PyTektronixScope
# import saleae






############################################################################################
##### defines: 
#############

if USER_NAME == "Bar":
    execfile(r"C:\Users\bar.kristal\Documents\GitHub\Python\devices.py")
    execfile(r"C:\Users\bar.kristal\Documents\GitHub\Python\utilities.py")
    execfile(r"C:\Users\bar.kristal\Documents\GitHub\Python\lab_equipment.py")
    # execfile(r"C:\Users\bar.kristal\Documents\GitHub\Python\apx525_module.py")

    POWER_SUPLLY_ADDRESS = "GPIB0::29::INSTR"
    DMM_ADDRESS = "GPIB0::22::INSTR"
    FREQUENCY_COUNTER_ADDRESS = "GPIB0::27::INSTR"
    WAVE_GENERATOR_ADDRESS = "GPIB0::1::INSTR"
    ELECTRONIC_LOAD_ADDRESS = "GPIB0::3::INSTR"
    SCOPE_ADDRESS = "GPIB0::9::INSTR"
    OVEN_ADDRESS = 'COM17'

elif USER_NAME == "Sas":
    execfile(r"C:\GitHub\Python\devices.py")
    execfile(r"C:\GitHub\Python\utilities.py")
    execfile(r"C:\GitHub\Python\lab_equipment.py")

    POWER_SUPLLY_ADDRESS = "GPIB1::29::INSTR"
    DMM_ADDRESS = "GPIB0::22::INSTR"
    FREQUENCY_COUNTER_ADDRESS = "GPIB0::27::INSTR"
    WAVE_GENERATOR_ADDRESS = "GPIB0::1::INSTR"
    ELECTRONIC_LOAD_ADDRESS = "GPIB0::3::INSTR"
    SCOPE_ADDRESS = "GPIB0::9::INSTR"
    TERMOTRON_TCP_IP =  ("172.19.5.237" ,8080)  # (ip, port) , (Sas)



elif USER_NAME == "Bisset":
    execfile(r"C:\GitHub\Python\devices.py")
    execfile(r"C:\GitHub\Python\utilities.py")
    execfile(r"C:\GitHub\Python\lab_equipment.py")

    POWER_SUPLLY_ADDRESS = "GPIB1::29::INSTR"
    DMM_ADDRESS = "GPIB0::22::INSTR"
    FREQUENCY_COUNTER_ADDRESS = "GPIB0::27::INSTR"
    WAVE_GENERATOR_ADDRESS = "GPIB0::1::INSTR"
    ELECTRONIC_LOAD_ADDRESS = "GPIB0::3::INSTR"
    SCOPE_ADDRESS = "GPIB0::9::INSTR"
    TERMOTRON_TCP_IP = ("172.19.5.239", 8080)  # (ip, port) , (Bisset)

elif USER_NAME == "Ronny":
    execfile(r"C:\Users\ronnyi\Documents\GitHub\Python\devices.py")
    execfile(r"C:\Users\ronnyi\Documents\GitHub\Python\utilities.py")
    execfile(r"C:\Users\ronnyi\Documents\GitHub\Python\lab_equipment.py")

    # POWER_SUPLLY_ADDRESS = "GPIB1::29::INSTR"
    # DMM_ADDRESS = "GPIB0::22::INSTR"
    # FREQUENCY_COUNTER_ADDRESS = "GPIB0::27::INSTR"
    # WAVE_GENERATOR_ADDRESS = "GPIB0::1::INSTR"
    # ELECTRONIC_LOAD_ADDRESS = "GPIB0::3::INSTR"
    # SCOPE_ADDRESS = "GPIB0::9::INSTR"
    TERMOTRON_TCP_IP = ("172.19.5.240", 8080)  # (ip, port) , (Ronny)



##########################################################################################
##### Log:
'''This section is uniform for all users.
    This section creates the log files for every test,
    when the test name and folder name are declared in the test itself.'''
FOLDER_DATE = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
DIR_NAME = os.path.join(FOLDER_PATH , 'Log' , FOLDER_DATE)
TEST_DATE = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
TEST_TIME = datetime.datetime.strftime(datetime.datetime.now(), '%H-%M-%S')
LOG_NAME = TEST_NAME + r"_" + TEST_DATE + r"_" + TEST_TIME + r".txt"
LOG_NAME_EXCEL = TEST_NAME + r"_" + TEST_DATE + r"_" + TEST_TIME + r".xlsx"
#open a new log:
open_log(DIR_NAME, LOG_NAME)
############################################################################################