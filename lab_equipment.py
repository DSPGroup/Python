##############################################################################################
## This module contains classes for working with Lab equipment                              ##
## In order to use this module, you need to install pyvisa library                          ##
## Author: Zvi Karp                                                                         ##
## Date: 15/11/16                                                                           ##
## Edited by: Bar Kristal, 18/12/16                                                         ##        
##############################################################################################

#Errors:

class Error_connecting_device():
    def __init__(self):
        write_to_log("Error: failed connecting to device" %(self.type))



#Lab equipment classes:

class Agillent34401A():
    def __init__(self,address,resource_manager):
        self.dev=resource_manager.open_resource(address)
        self.name=self.dev.query('*IDN?')[:-1]
        self.dev.timeout = 5000
        
    def close(self):
        self.dev.close()
        write_to_log ('The connection with: %s is now closed' %(self.name))
    
    def send_command(self, command):
    #Send a visa command to the device.
    #This function and the next one can be used in order to send a command that doesn't covered by this module.
        self.dev.write(command)
        
    def read_response(self, command):
    #read from the device. can be used after sending a query command to the device.
        return self.dev.read()[-1]
        
    def meas(self,meas):
        if  meas == 'DCV':
            self.dev.write('MEAS:VOLT:DC?')
            result = self.dev.read()[:-1]
            write_to_log ("DC Measurement: %s" %(result))
        elif meas == 'ACV':
            self.dev.write('MEAS:VOLT:AC?')
            result = self.dev.read()[:-1]
            write_to_log ("AC Measurement: %s" %(result))
        elif meas == 'frequency':
            self.dev.write('MEAS:FREQ?')
            result = self.dev.read()[:-1]
            write_to_log ("Frequency Measurement: %s" %(result))
        elif meas == 'resistance':
            self.dev.write('MEAS:REAS?')
            result = self.dev.read()[:-1]
            write_to_log ("Resistance Measurement: %s" %(result))
        elif meas == 'DCI':
            self.dev.write('MEAS:CURR:DC?')
            result = self.dev.read()[:-1]
            write_to_log ("DC Current Measurement: %s" %(result))
        elif meas == 'ACI':
            self.dev.write('MEAS:CURR:AC?')
            result = self.dev.read()[:-1]
            write_to_log ("AC Current Measurement: %s" %(result))
        return result



class QL355TPPwrSply():
    def __init__(self,address,resource_manager):
        self.dev=resource_manager.open_resource(address)
        self.dev.clear()
        self.name=self.dev.query('*IDN?')[:-1]
        self.dev.timeout = 5000
        

    def close(self):
        self.dev.close()
        write_to_log ('The connection with: %s is now closed' %(self.name))
    
    def set_timeout(self, time):
        time = int(time)
        self.dev.timeout = time
        
    def send_command(self, command):
    #Send a visa command to the device.
    #This function and the next one can be used in order to send a command that doesn't covered by this module.
        self.dev.write(command)
        
    def read_response(self, command):
    #read from the device. can be used after sending a query command to the device.
        return self.dev.read()[-1]
    
    def set_volt(self, channel, volt):
        #set the voltage output of the specified channel
        channel = str(channel)
        self.dev.write("V%s %s" %(channel , volt))
        time.sleep(0.5)
        res = self.dev.query("V%s?" %(channel))[:-1]
        write_to_log (res)
        
    def set_current_lim(self, channel, current):
        #set the current limit of the specified channel
        channel = str(channel)
        self.dev.write("I%s %s" %(channel ,current))
        time.sleep(0.1)
        res = self.dev.query("I%s?" %(channel))[:-1]
        write_to_log(res)
        
    def channel_on(self, channel):
        #set ON the specified channel
        channel = str(channel)
        self.dev.write('OP%s 1' %(channel))
        write_to_log('Channel %s is on' %(channel))
        
    def channel_off(self, channel):
        #set OFF the specified channel
        channel = str(channel)
        self.dev.write('OP%s 0' %(channel))
        write_to_log('Channel %s is off' %(channel))
        
    def increment_voltage(self, channel, step_size):
        #increment the channel's output voltage in a step_size voltage
        channel = str(channel)
        self.dev.write('DELTAV%s %s' %(channel ,step_size))
        self.dev.write('INCV%s' %(channel))
        write_to_log("Channel %s was incremented by %sV" %(channel ,step_size))
        self.dev.write('V%s?' %(channel))
        write_to_log("Channel %s volatge is now %sV" %(channel ,self.dev.read()[3:]))
        
    def all_off(self):
        #set ALL channels OFF
        self.dev.write('OPALL 0')
        write_to_log("All channels set OFF")
        
    def all_on(self):
        #set ALL channels ON
        self.dev.write('OPALL 1')
        write_to_log("All channels set ON")

    def read_current(self, channel):
        #reads the current flows right now through the channel
        self.dev.write('I%sO?' %(str(channel)))
        cur = self.dev.read()[:-1]
        write_to_log("The current at channel %s is: %s" %(channel, cur))
        return cur
        
    def sense(self, channel, mode):
    #mode=0: local, mode=1: remote
        self.dev.write('SENSE%s %s' %(channel, mode))
        mod="local" if mode == '0' else "remote"
        write_to_log("Activated %s sense on channel %s" %(mod, str(channel)))
                     
     
class HP53131aFreqCounter():
    def __init__(self,address,resource_manager):
        self.dev=resource_manager.open_resource(address)
        self.name=self.dev.query('*IDN?')[:-1]
        self.dev.timeout = 5000
    
    def close(self):
        self.dev.close()
        write_to_log ('The connection with: %s is now closed' %(self.name))

    def send_command(self, command):
    #Send a visa command to the device.
    #This function and the next one can be used in order to send a command that doesn't covered by this module.
        self.dev.write(command)
        
    def read_response(self, command):
    #read from the device. can be used after sending a query command to the device.
        return self.dev.read()[-1]

    #Take one of the following measurement options.
    #Notice that the 'channel' argument is an option, only for 'frequency' mesurement, when the default is "1"       
    def meas(self, meas, channel="1"):
        channel = str(channel)
        if ((meas != "frequency" and meas != "volt_max_peak" and  meas != "volt_min_peak") and (channel != "1")):
            write_to_log("Error: %s measurement can be taken only from channel 1" %(meas))
            return ""
        else:
            if (meas == "frequency"):
                self.dev.write('MEAS%s:FREQ?' %(channel))
                result = self.dev.read()[:-1]
                write_to_log ("%s measurement on channel %s: %s" %(meas, channel, result))
            elif (meas == "rise_time"):
                self.dev.write('MEAS:RTIME?')
                result = self.dev.read()[:-1]
                write_to_log ("%s measurement on channel %s: %s" %(meas, channel, result))
            elif (meas == "fall_time"):
                self.dev.write('MEAS:FTIME?')
                result = self.dev.read()[:-1]
                write_to_log ("%s measurement on channel %s: %s" %(meas, channel, result))
            elif (meas == "period"):
                self.dev.write('MEAS:PER?')
                result = self.dev.read()[:-1]
                write_to_log ("%s measurement on channel %s: %s" %(meas, channel, result))
            elif (meas == "pos_width"):
                self.dev.write('MEAS:PWID?')
                result = self.dev.read()[:-1]
                write_to_log ("%s measurement on channel %s: %s" %(meas, channel, result))
            elif (meas == "neg_width"):
                self.dev.write('MEAS:NWID?')
                result = self.dev.read()[:-1]
                write_to_log ("%s measurement on channel %s: %s" %(meas, channel, result))
            elif (meas == "duty_cycle"):
                self.dev.write('MEAS:DCYC?')
                result = self.dev.read()[:-1]
                write_to_log ("%s measurement on channel %s: %s" %(meas, channel, result))
            elif (meas == "volt_max_peak"):
                self.dev.write('MEAS%s:MAX?' %(channel))
                result = self.dev.read()[:-1]
                write_to_log ("%s measurement on channel %s: %s" %(meas, channel, result))
            elif (meas == "volt_min_peak"):
                self.dev.write('MEAS%s:MIN?' %(channel))
                result = self.dev.read()[:-1]
                write_to_log ("%s measurement on channel %s: %s" %(meas, channel, result)) 
            elif (meas == "ratio"):
                self.dev.write('MEAS:FREQ:RAT?')
                result = self.dev.read()[:-1]
                write_to_log ("Ratio %s to %s: %s" %("1", "2", result))
            elif (meas == "phase"):
                self.dev.write('MEAS:PHAS?')
                result = self.dev.read()[:-1]
                write_to_log ("Phase %s to %s: %s" %("1", "2", result))
            return result    

        
class HP33120aWaveGen():
    def __init__(self, address, resource_manager):
        self.dev=resource_manager.open_resource(address)
        self.name=self.dev.query('*IDN?')[:-1]
        self.dev.timeout = 5000
        
    def close(self):
        self.dev.close()
        write_to_log ('The connection with: %s is now closed' %(self.name))        
    
    def send_command(self, command):
    #Send a visa command to the device.
    #This function and the next one can be used in order to send a command that doesn't covered by this module.
        self.dev.write(command)
        
    def read_response(self, command):
    #read from the device. can be used after sending a query command to the device.
        return self.dev.read()[-1]
    
    #Generate a waveform in single command.
    #Example: self.generate("SIN", 3000, 1.5, -1) generates a sine wave, 3KHz, 1.5Vpp, -1V offset.    
    def generate(self, wave, frequency, amplitude, offset):
        self.dev.write("APPL:%s %s, %s, %s" %(wave, freqency, amplitude, offset))
    
    #Set specifiied shape : SINusoid|SQUare|TRIangle|RAMP|NOISe|DC|USER
    def set_shape(self, shape):
        self.dev.write("FUNC:SHAP %s" %(shape))
    
    #Set frequency    
    def set_frequency(self, frequency):
        self.dev.write("FREQ: %s" %(frequency))
    
    def set_amplitude(self, amplitude):
        self.dev.write("VOLT: %s" %(amplitude))
    
    #Set the units of the amplitude: VPP|VRMS|DBM|DEFault
    #Do not affect the offset units, which stays V.
    def set_amplitude_units(self, units):
        self.dev.write("VOLT:UNIT %s" %(amplitude))
        
    def set_offset(self, offset):
        self.dev.write("VOLT:OFFS %s" %(offset))
        
    def get_shape(self):
        result = self.dev.query("FUNC:SHAP?")[:-1]
        write_to_log("Signal's shape is: %s" %(result))
        return result
    
    def get_frequency(self):
        result = self.dev.query("FREQ?")[:-1]
        write_to_log("Frequency is: %s" %(result))
        return result
    
    def get_amplitude(self):
        result = self.dev.query("VOLT?")[:-1]
        write_to_log("Amplitude is: %s" %(result))
        return result    
    
    def get_amplitude_unit(self):
        result = self.dev.query("VOLT:UNIT?")[:-1]
        write_to_log("Amplitude units are: %s" %(result))
        return result
        
        
    def get_offset(self):
        result = self.dev.query("VOLT:OFFS?")[:-1]
        write_to_log("Offset is: %s" %(result))
        return result   
    

class KikusuiPLZ70UA():
    def __init__(self, address, resource_manager):
        self.dev=resource_manager.open_resource(address)
        self.name=self.dev.query('*IDN?')[:-1]
        self.dev.timeout = 5000
        
    #Close the connection with the device
    def close(self):
        self.dev.close()
        write_to_log ('The connection with: %s is now closed' %(self.name))
    
    def send_command(self, command):
    #Send a visa command to the device.
    #This function and the next one can be used in order to send a command that doesn't covered by this module.
        self.dev.write(command)
        
    def read_response(self, command):
    #read from the device. can be used after sending a query command to the device.
        return self.dev.read()[-1]
    
    #Reset the device to factory default settings.    
    def reset(self):
        self.dev.write("*RST")
        write_to_log ('%s configured to factory default settings' %(self.name[:-1]))
        
    def load_on(self):
        self.dev.write("INP ON")
        if (self.dev.query("INP?") != '0'):
            write_to_log("Load in on")
            
    def load_off(self):
        self.dev.write("INP OFF")
        if (self.dev.query("INP?") != '1'):
            write_to_log("Load in off")
    
    #mode=CC/CR/CV/CCCV/CRCV, when CC='constant current' CR='constant resistance' CV='constant voltage'
    def set_constant_mode(self, channel, mode):
        self.dev.write("INST CH%s" %channel)
        self.dev.write("FUNC %s" %mode)
    
    
    #Set the conductance (in units of [S]). This funciton sets both of the channels together  
    def set_conductance(self, conductance):
        self.dev.write("COND %s" %conductance)
    
    #Set the resistance (in unit of [ohm]) by first changing to conductance units.  This funciton sets both of the channels together    
    def set_resistance(self, resistance):
        if (float(resistance) != 0):
            conductance = str(1/float(resistance))    
            self.dev.write("COND %s" %conductance)
    
    #Set current. This funciton sets both of the channels together     
    def set_current(self, current):
        self.dev.write("CURR %s" %current)
    
    #Set voltage. This funciton sets both of the channels together      
    def set_voltage(self, channel, voltage):
        self.dev.write("INST CH%s" %channel)
        self.dev.write("VOLT %s" %voltage)
    
    #Read the conductance on the specified channel
    def read_conductance(self, channel):
        self.dev.write("INST CH%s" %channel)
        res = self.dev.query("MEAS:COND?")[:-1]
        write_to_log("The conductance on channel %s is: %sS" %(channel, res))
        return res
    
    #Read the conductance on the specified channel
    def read_current(self, channel):
        self.dev.write("INST CH%s" %channel)
        res = self.dev.query("MEAS:CURR?")[:-1]
        write_to_log("The current on channel %s is: %sA" %(channel, res))
        return res
            
    #Read the conductance on the specified channel
    def read_voltage(self, channel):
        self.dev.write("INST CH%s" %channel)
        res = self.dev.query("MEAS:VOLT?")[:-1]
        write_to_log("The voltage on channel %s is: %sV" %(channel, res))
        return res
        


# The connection with this oven is a serial connection - rs232 - which is done using a usb-to-RS232 connector.
# This connector appears as a virtual port with a specified 'COM'- this is the COM we need to enter when initializing the connection.
class VotschVT4002():
    def __init__(self, com):
        self.name="VotschVT4002"
        self.ser=serial.Serial()
        self.ser.close()
        self.ser.port = com
        self.ser.baudrate = 9600
        self.ser.bytesize = 8
        self.ser.parity = 'N'
        self.ser.stopbits = 1
        self.ser.timeout = 1
        self.ser.open()
        
    
    #Close the serial connection with the device
    def close(self):
        self.ser.close()
    
    #Changing the serial connection's parameters:
    def change_port(self, com):
        self.ser.port = com
        write_to_log("{} port changed to {}".format(self.name, com))  
    
    #Sets the temperature and STARTS the chamber. temp can be from type int, float of str
    def set_temp(self, temp):
        neg = '0'
        typ = type(temp) 
        if (typ == str):
            temp = float(temp)
        if (abs(temp) < 10):
            temp = neg + '00' + str(round(temp,1))
        elif (temp <= 100 and temp >= -50):   
            temp = neg + '0' +str(round(temp,1))
        else:
            write_to_log("Error: temperature should be between -50C to 100C")
        self.ser.write("$00E %s 0000.0 0000.0 0000.0 0000.0 010100000000111013" %temp)
        self.ser.write("$00I\r\n")
    
    #Return the temperature
    def read_temp(self):
        self.ser.write("$00I\r\n")
        res = self.ser.readline()
        res = res.split(" ")[1]
        if (res[0] == '1'): #negative
            res = '-' + res[2:]
        else:
            res = res[2:]  
        #write_to_log("Temperature is: %sC" %res)
        return res
    
    #Stops the function of the chamber    
    def stop_champer(self):
        self.ser.write("$00E 0000.0 0000.0 0000.0 0000.0 0000.0 000100000000111013")
     
    #Sets a temperature, and waits until it gets to the desirable temp.    
    def wait_for_temp(self,temp):
        self.set_temp(temp) 
        time.sleep(0.5)
        current_temp = float(self.read_temp())
        write_to_log("wait for the temperature to reach %sC" %temp)
        temp = float(temp)
        while (abs(current_temp) <= abs(temp*0.98) or abs(current_temp) >= abs(temp*1.02)):
            time.sleep(1)
            current_temp = float(self.read_temp())
        write_to_log("Temperature has reached the desirable value")
           
    def read_error(self):
        self.ser.write("$00F\r\n")
        time.sleep(1)
        return self.ser.readline()


class Termotron3800():
    def __init__(self,address):
        self.tcp_ip = address[0]
        self.port = address[1]
        self.buffer_size = 1024
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.tcp_ip, self.port))
        self.sock.send("IDEN?\r\n")    #ask for device identity
        self.name = self.sock.recv(23)
        self.sock.recv(10)
        self.sock.send("VRSN?\r\n")    #ask for software version
        self.version = self.sock.recv(16)
        self.sock.recv(5)
        
    #close connection with device
    def close(self):
        self.sock.close()
    
    #before reading the device's answer:
    def clear_buffer(self):
        self.sock.recv(10)
        time.sleep(0.1)
        
    def stop_chamber(self):
        err = "0"
        k = 0
        while (err != "5" and k<10):  #5 means that Termotron received the stop command
            self.sock.send("STOP\r\n")  #send the STOP command
            self.clear_buffer()
            self.sock.send("SCOD?\r\n")  #check if the command had been received
            err = self.sock.recv(1)
            
        if (k == 10): #5 means that Termotron received the stop command
            write_to_log("Error while sending STOP command to %s" %self.name)
            
    def run_chamber(self):
        self.sock.send("RUNM\r\n")
         
    def set_temp(self, temp):
        if type(temp != str):
            temp = str(temp)
        self.sock.send("SETP1,%s\r\n" %temp)
        time.sleep(0.1)
        self.run_chamber()
        
    #read the current temperature of the chamber.
    def read_temp(self):
        self.clear_buffer()
        self.sock.send("PVAR1?\r\n") #read the deviation from the configured value
        time.sleep(0.1)
        current_temp = float(self.sock.recv(4))
        return current_temp


    def wait_for_temp(self, temp):
        self.set_temp(temp)
        time.sleep(0.1)
        current_temp = float(self.read_temp())
        while (abs(current_temp) <= abs(temp*0.98) or abs(current_temp) >= abs(temp*1.02)):
            time.sleep(1)
            current_temp = float(self.read_temp())
        write_to_log("Temperature has reached the desirable value")

